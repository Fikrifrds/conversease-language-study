from __future__ import annotations

import asyncio
import base64
import binascii
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from io import BytesIO
import ipaddress
import json
import logging
import os
from pathlib import Path
import re
import shutil
import socket
import tempfile
import time
from typing import Dict, Optional, Tuple
from urllib.parse import quote, urljoin, urlsplit
from uuid import uuid4

import httpx
from PIL import Image, ImageOps, UnidentifiedImageError
from sqlalchemy.orm import Session
import yaml

from app.core.config import settings
from app.db.models import LessonVisualAssetModel
from app.repositories.lesson_visual_library import (
    activate_visual_asset,
    assign_visual_placement,
    get_active_visual_asset,
    get_visual_asset,
    get_visual_asset_by_hash,
    get_visual_placement,
    list_visual_assets,
    list_visual_placements,
    register_visual_asset,
)


REPO_ROOT = Path(__file__).resolve().parents[4]
CURRICULUM_ROOT = REPO_ROOT / "content" / "curriculum" / "english"
PROMPT_ROOT = REPO_ROOT / "content" / "visual-prompts" / "english"
VALID_SLOTS = ("hero", "card-1", "card-2", "card-3")
VALID_PLACEMENT_OWNER_TYPES = ("course", "unit")
VALID_PLACEMENT_SLOTS = ("cover", "detail-hero", "thumbnail")
PLACEMENT_PROMPT_PATH = REPO_ROOT / "content" / "visual-prompts" / "PLACEMENT.md"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_IMAGE_BYTES = 30 * 1024 * 1024
PNG_PALETTE_COLORS = 256
VISUAL_THUMBNAIL_MAX_WIDTH = 384
VISUAL_THUMBNAIL_WEBP_QUALITY = 70
REMOTE_IMAGE_CONTENT_TYPES = {"image/png", "image/jpeg", "image/webp", "application/octet-stream"}
MAX_REMOTE_IMAGE_REDIRECTS = 4

logger = logging.getLogger(__name__)


class LessonVisualRegenerationError(Exception):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class RegeneratedLessonVisual:
    slug: str
    slot: str
    model: str
    version: str
    byte_count: int
    library_asset_id: str = ""
    library_relative_path: str = ""


class TogetherImageClient:
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        model: str,
        timeout_seconds: int,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout_seconds = timeout_seconds

    async def generate_png(self, *, prompt: str, slot: str) -> bytes:
        if not self._api_key:
            raise LessonVisualRegenerationError("together_api_key_missing")

        width, height = image_generation_dimensions(slot)
        payload = {
            "model": self._model,
            "prompt": prompt,
            "width": width,
            "height": height,
            "n": 1,
            # Together-hosted URLs avoid inflating the API response by roughly
            # one third with base64 and keep peak memory lower for 1K images.
            "response_format": "url",
            "output_format": "png",
        }
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        timeout = httpx.Timeout(self._timeout_seconds)
        request_url = f"{self._base_url}/v1/images/generations"
        started = time.monotonic()

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(request_url, headers=headers, json=payload)
                response.raise_for_status()
                body = response.json()
                image_bytes = await image_bytes_from_response(body, client=client)
        except httpx.HTTPStatusError as exc:
            logger.warning(
                "lesson_visual_together_status_error model=%s slot=%s status=%s",
                self._model,
                slot,
                exc.response.status_code,
            )
            raise LessonVisualRegenerationError(
                f"together_image_status_{exc.response.status_code}"
            ) from exc
        except httpx.HTTPError as exc:
            logger.warning(
                "lesson_visual_together_request_error model=%s slot=%s",
                self._model,
                slot,
            )
            raise LessonVisualRegenerationError("together_image_request_failed") from exc
        except ValueError as exc:
            raise LessonVisualRegenerationError("together_image_invalid_json") from exc

        validate_png(image_bytes)
        logger.info(
            "lesson_visual_together_ok model=%s slot=%s bytes=%s duration_ms=%s",
            self._model,
            slot,
            len(image_bytes),
            int((time.monotonic() - started) * 1000),
        )
        return image_bytes


async def image_bytes_from_response(
    body: object,
    *,
    client: Optional[httpx.AsyncClient],
) -> bytes:
    if not isinstance(body, dict):
        raise LessonVisualRegenerationError("together_image_response_invalid")
    data = body.get("data")
    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        raise LessonVisualRegenerationError("together_image_response_empty")

    item = data[0]
    encoded = item.get("b64_json")
    if isinstance(encoded, str) and encoded.strip():
        value = encoded.strip()
        if value.startswith("data:") and "," in value:
            value = value.split(",", 1)[1]
        try:
            return base64.b64decode(value, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise LessonVisualRegenerationError("together_image_base64_invalid") from exc

    image_url = item.get("url")
    if isinstance(image_url, str) and image_url.startswith(("https://", "http://")):
        if client is None:
            raise LessonVisualRegenerationError("together_image_response_invalid")
        response = await client.get(image_url)
        response.raise_for_status()
        return response.content

    raise LessonVisualRegenerationError("together_image_response_empty")


async def regenerate_lesson_visual(
    *,
    slug: str,
    slot: str,
    image_client: Optional[TogetherImageClient] = None,
    overrides_dir: Optional[Path] = None,
    db: Optional[Session] = None,
) -> RegeneratedLessonVisual:
    prompt_path, prompt = resolve_lesson_visual_prompt(slug=slug, slot=slot)
    client = image_client or TogetherImageClient(
        api_key=settings.together_api_key,
        base_url=settings.together_api_base_url,
        model=settings.together_image_model,
        timeout_seconds=settings.together_image_timeout_seconds,
    )
    image_bytes = await client.generate_png(prompt=prompt, slot=slot)
    validate_png(image_bytes)
    optimized_image_bytes = await asyncio.to_thread(optimize_png, image_bytes)

    return await asyncio.to_thread(
        store_lesson_visual,
        slug=slug,
        slot=slot,
        prompt_path=prompt_path,
        prompt=prompt,
        image_bytes=optimized_image_bytes,
        model=settings.together_image_model,
        archive_reason="new_generation",
        overrides_dir=overrides_dir,
        db=db,
    )


def upload_lesson_visual(
    *,
    slug: str,
    slot: str,
    image_bytes: bytes,
    overrides_dir: Optional[Path] = None,
    db: Optional[Session] = None,
) -> RegeneratedLessonVisual:
    return store_uploaded_lesson_visual(
        slug=slug,
        slot=slot,
        image_bytes=image_bytes,
        model="manual-upload",
        archive_reason="manual_upload",
        overrides_dir=overrides_dir,
        db=db,
    )


def store_uploaded_lesson_visual(
    *,
    slug: str,
    slot: str,
    image_bytes: bytes,
    model: str,
    archive_reason: str,
    overrides_dir: Optional[Path] = None,
    db: Optional[Session] = None,
    activate: bool = True,
) -> RegeneratedLessonVisual:
    prompt_path, prompt = resolve_lesson_visual_prompt(slug=slug, slot=slot)
    normalized_image_bytes = normalize_uploaded_image(image_bytes=image_bytes, slot=slot)
    return store_lesson_visual(
        slug=slug,
        slot=slot,
        prompt_path=prompt_path,
        prompt=prompt,
        image_bytes=normalized_image_bytes,
        model=model,
        archive_reason=archive_reason,
        overrides_dir=overrides_dir,
        db=db,
        activate=activate,
    )


async def import_lesson_visual_from_url(
    *,
    slug: str,
    slot: str,
    url: str,
    overrides_dir: Optional[Path] = None,
    db: Optional[Session] = None,
) -> RegeneratedLessonVisual:
    image_bytes = await download_remote_image(url)
    return await asyncio.to_thread(
        store_uploaded_lesson_visual,
        slug=slug,
        slot=slot,
        image_bytes=image_bytes,
        model="url-import",
        archive_reason="url_import",
        overrides_dir=overrides_dir,
        db=db,
    )


def store_lesson_visual(
    *,
    slug: str,
    slot: str,
    prompt_path: Path,
    prompt: str,
    image_bytes: bytes,
    model: str,
    archive_reason: str,
    overrides_dir: Optional[Path],
    db: Optional[Session] = None,
    activate: bool = True,
) -> RegeneratedLessonVisual:
    if overrides_dir is None:
        return store_lesson_visual_s3(
            slug=slug,
            slot=slot,
            prompt_path=prompt_path,
            prompt=prompt,
            image_bytes=image_bytes,
            model=model,
            archive_reason=archive_reason,
            db=db,
            activate=activate,
        )
    return store_lesson_visual_local(
        slug=slug,
        slot=slot,
        prompt_path=prompt_path,
        prompt=prompt,
        image_bytes=image_bytes,
        model=model,
        archive_reason=archive_reason,
        overrides_dir=overrides_dir,
    )


def store_lesson_visual_local(
    *,
    slug: str,
    slot: str,
    prompt_path: Path,
    prompt: str,
    image_bytes: bytes,
    model: str,
    archive_reason: str,
    overrides_dir: Path,
) -> RegeneratedLessonVisual:

    root = overrides_dir
    target_path = override_path(root=root, slug=slug, slot=slot)
    library_root = root / "_library"
    archive_existing_override_if_needed(
        target_path=target_path,
        library_root=library_root,
        slug=slug,
        slot=slot,
        prompt_path=prompt_path,
        prompt=prompt,
    )
    library_asset_id, library_relative_path = archive_lesson_visual(
        library_root=library_root,
        slug=slug,
        slot=slot,
        prompt_path=prompt_path,
        prompt=prompt,
        image_bytes=image_bytes,
        model=model,
        archive_reason=archive_reason,
    )
    atomic_write(target_path, image_bytes)
    atomic_write(archive_marker_path(target_path), library_asset_id.encode("utf-8"))
    version = str(target_path.stat().st_mtime_ns)

    logger.info(
        "lesson_visual_stored slug=%s slot=%s source=%s bytes=%s",
        slug,
        slot,
        archive_reason,
        len(image_bytes),
    )

    return RegeneratedLessonVisual(
        slug=slug,
        slot=slot,
        model=model,
        version=version,
        byte_count=len(image_bytes),
        library_asset_id=library_asset_id,
        library_relative_path=library_relative_path,
    )


def resolve_lesson_visual_prompt(*, slug: str, slot: str) -> Tuple[Path, str]:
    if slot not in VALID_SLOTS:
        raise LessonVisualRegenerationError("invalid_visual_slot")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise LessonVisualRegenerationError("invalid_lesson_slug")

    prompt_path = lesson_prompt_index().get(slug)
    if prompt_path is None:
        raise LessonVisualRegenerationError("lesson_visual_prompt_not_found")
    return prompt_path, extract_visual_prompt(prompt_path, slot)


@lru_cache(maxsize=1)
def lesson_prompt_index() -> Dict[str, Path]:
    index: Dict[str, Path] = {}
    for lesson_yaml in CURRICULUM_ROOT.glob("*/units/*/*/lesson.yaml"):
        lesson = read_yaml(lesson_yaml)
        slug = str(lesson.get("slug") or "").strip()
        if not slug:
            continue
        lesson_dir = lesson_yaml.parent
        parts = lesson_dir.relative_to(CURRICULUM_ROOT).parts
        level, unit_key, lesson_key = parts[0], parts[2], parts[3]
        prompt_path = PROMPT_ROOT / level / unit_key / lesson_key / "PROMPT.md"
        if prompt_path.exists():
            index[slug] = prompt_path
    return index


def extract_visual_prompt(prompt_path: Path, slot: str) -> str:
    if slot == "hero":
        heading = "Hero prompt"
    else:
        heading = f"Card {slot.split('-', 1)[1]} prompt"

    text = prompt_path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}[^\n]*\n\s*```text\n(?P<prompt>.*?)\n```",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if match is None:
        raise LessonVisualRegenerationError("lesson_visual_prompt_section_not_found")

    prompt = match.group("prompt").strip()
    if not prompt or len(prompt) > 30_000:
        raise LessonVisualRegenerationError("lesson_visual_prompt_invalid")
    width, height = image_generation_dimensions(slot)
    return re.sub(
        r"\bat \d+[×x]\d+ pixels\b",
        f"at {width}×{height} pixels",
        prompt,
        count=1,
    )


def image_generation_dimensions(slot: str) -> Tuple[int, int]:
    if slot == "hero":
        return (1024, 576)
    return (1024, 1024)


def override_path(*, root: Path, slug: str, slot: str) -> Path:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise LessonVisualRegenerationError("invalid_lesson_slug")
    if slot not in VALID_SLOTS:
        raise LessonVisualRegenerationError("invalid_visual_slot")
    return root / slug / f"{slot}.png"


def validate_png(image_bytes: bytes) -> None:
    if not image_bytes or len(image_bytes) > MAX_IMAGE_BYTES:
        raise LessonVisualRegenerationError("generated_image_size_invalid")
    if not image_bytes.startswith(PNG_SIGNATURE):
        raise LessonVisualRegenerationError("generated_image_not_png")


async def download_remote_image(
    url: str,
    *,
    client: Optional[httpx.AsyncClient] = None,
) -> bytes:
    if client is None:
        timeout = httpx.Timeout(connect=10, read=30, write=10, pool=10)
        async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=False,
            trust_env=False,
        ) as owned_client:
            return await download_remote_image(url, client=owned_client)

    current_url = url
    for _ in range(MAX_REMOTE_IMAGE_REDIRECTS + 1):
        safe_url = await asyncio.to_thread(validate_remote_image_url, current_url)
        try:
            async with client.stream(
                "GET",
                safe_url,
                headers={"Accept": "image/png,image/jpeg,image/webp"},
            ) as response:
                if response.is_redirect:
                    location = response.headers.get("location")
                    if not location:
                        raise LessonVisualRegenerationError("remote_image_download_failed")
                    current_url = urljoin(safe_url, location)
                    continue

                if response.status_code in {401, 403}:
                    raise LessonVisualRegenerationError("remote_image_auth_required")
                response.raise_for_status()
                content_type = response.headers.get("content-type", "").split(";", 1)[0].lower()
                if content_type not in REMOTE_IMAGE_CONTENT_TYPES:
                    raise LessonVisualRegenerationError("remote_image_content_type_invalid")
                content_length = response.headers.get("content-length")
                if content_length and int(content_length) > MAX_IMAGE_BYTES:
                    raise LessonVisualRegenerationError("uploaded_image_size_invalid")

                chunks = bytearray()
                async for chunk in response.aiter_bytes():
                    chunks.extend(chunk)
                    if len(chunks) > MAX_IMAGE_BYTES:
                        raise LessonVisualRegenerationError("uploaded_image_size_invalid")
                return bytes(chunks)
        except LessonVisualRegenerationError:
            raise
        except (httpx.HTTPError, ValueError) as exc:
            raise LessonVisualRegenerationError("remote_image_download_failed") from exc

    raise LessonVisualRegenerationError("remote_image_too_many_redirects")


def validate_remote_image_url(url: str) -> str:
    if len(url) > 4096:
        raise LessonVisualRegenerationError("remote_image_url_invalid")
    parsed = urlsplit(url)
    try:
        port = parsed.port
    except ValueError as exc:
        raise LessonVisualRegenerationError("remote_image_url_invalid") from exc
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or port not in {None, 443}
    ):
        raise LessonVisualRegenerationError("remote_image_url_invalid")

    try:
        addresses = socket.getaddrinfo(parsed.hostname, 443, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise LessonVisualRegenerationError("remote_image_url_invalid") from exc
    if not addresses:
        raise LessonVisualRegenerationError("remote_image_url_invalid")

    for address in addresses:
        raw_address = address[4][0].split("%", 1)[0]
        try:
            if not ipaddress.ip_address(raw_address).is_global:
                raise LessonVisualRegenerationError("remote_image_url_forbidden")
        except ValueError as exc:
            raise LessonVisualRegenerationError("remote_image_url_invalid") from exc
    return url


def normalize_uploaded_image(*, image_bytes: bytes, slot: str) -> bytes:
    if not image_bytes or len(image_bytes) > MAX_IMAGE_BYTES:
        raise LessonVisualRegenerationError("uploaded_image_size_invalid")

    try:
        with Image.open(BytesIO(image_bytes)) as source:
            source.load()
            if source.format not in {"PNG", "JPEG", "WEBP"}:
                raise LessonVisualRegenerationError("uploaded_image_format_invalid")

            source = ImageOps.exif_transpose(source)
            target_width, target_height = image_generation_dimensions(slot)
            target_ratio = target_width / target_height
            source_ratio = source.width / source.height
            if abs(source_ratio - target_ratio) / target_ratio > 0.05:
                raise LessonVisualRegenerationError("uploaded_image_aspect_ratio_invalid")

            mode = "RGBA" if "A" in source.getbands() else "RGB"
            normalized = ImageOps.fit(
                source.convert(mode),
                (target_width, target_height),
                method=Image.Resampling.LANCZOS,
            )
            output = BytesIO()
            normalized.save(output, format="PNG", optimize=True, compress_level=9)
    except LessonVisualRegenerationError:
        raise
    except (OSError, UnidentifiedImageError, ValueError, ZeroDivisionError) as exc:
        raise LessonVisualRegenerationError("uploaded_image_format_invalid") from exc

    return optimize_png(output.getvalue())


def optimize_png(image_bytes: bytes) -> bytes:
    """Lossily palette-optimize generated PNGs while preserving their dimensions."""
    try:
        with Image.open(BytesIO(image_bytes)) as source:
            source.load()
            if source.format != "PNG":
                raise LessonVisualRegenerationError("generated_image_not_png")

            if source.mode in {"RGBA", "LA"} and source.getchannel("A").getextrema()[0] < 255:
                optimized = source.convert("RGBA").quantize(
                    colors=PNG_PALETTE_COLORS,
                    method=Image.Quantize.FASTOCTREE,
                )
            else:
                optimized = source.convert("RGB").quantize(
                    colors=PNG_PALETTE_COLORS,
                    method=Image.Quantize.MEDIANCUT,
                )

            output = BytesIO()
            optimized.save(output, format="PNG", optimize=True, compress_level=9)
    except LessonVisualRegenerationError:
        raise
    except (OSError, UnidentifiedImageError, ValueError) as exc:
        raise LessonVisualRegenerationError("generated_image_not_png") from exc

    optimized_bytes = output.getvalue()
    validate_png(optimized_bytes)
    return optimized_bytes if len(optimized_bytes) < len(image_bytes) else image_bytes


def create_visual_thumbnail(image_bytes: bytes) -> bytes:
    """Create a small WebP used only by the visual-library picker."""
    try:
        with Image.open(BytesIO(image_bytes)) as source:
            source.load()
            source = ImageOps.exif_transpose(source)
            thumbnail = source.convert("RGB")
            thumbnail.thumbnail(
                (VISUAL_THUMBNAIL_MAX_WIDTH, VISUAL_THUMBNAIL_MAX_WIDTH),
                Image.Resampling.LANCZOS,
            )
            output = BytesIO()
            thumbnail.save(
                output,
                format="WEBP",
                quality=VISUAL_THUMBNAIL_WEBP_QUALITY,
                method=6,
            )
    except (OSError, UnidentifiedImageError, ValueError) as exc:
        raise LessonVisualRegenerationError("generated_image_not_png") from exc
    return output.getvalue()


def store_lesson_visual_s3(
    *,
    slug: str,
    slot: str,
    prompt_path: Path,
    prompt: str,
    image_bytes: bytes,
    model: str,
    archive_reason: str,
    db: Optional[Session] = None,
    activate: bool = True,
) -> RegeneratedLessonVisual:
    ensure_visual_s3_configured()
    created_at = datetime.now(timezone.utc)
    content_hash = hashlib.sha256(image_bytes).hexdigest()
    if db is not None:
        existing = get_visual_asset_by_hash(db, content_hash=content_hash)
        if existing is not None:
            if activate:
                activate_visual_asset(
                    db,
                    lesson_slug=slug,
                    slot=slot,
                    asset_id=existing.id,
                )
                db.commit()
                entry = visual_asset_entry(existing)
                visual_s3_put_json(
                    visual_s3_client(),
                    visual_active_manifest_key(slug=slug, slot=slot),
                    entry,
                )
            return regenerated_visual_from_asset(existing, slug=slug, slot=slot)
    asset_id = f"{created_at.strftime('%Y%m%dT%H%M%S%fZ')}-{uuid4().hex[:8]}"
    asset_prefix = f"lesson-visuals/library/{slug}/{slot}/{asset_id}"
    image_key = f"{asset_prefix}/image.png"
    thumbnail_key = f"{asset_prefix}/thumbnail.webp"
    metadata_key = f"{asset_prefix}/metadata.yaml"
    readme_key = f"{asset_prefix}/README.md"
    description = visual_description(prompt_path=prompt_path, prompt=prompt, slot=slot)
    width, height = image_dimensions(image_bytes)
    canonical_url = f"s3://{settings.s3_bucket}/{image_key}"
    entry = {
        "asset_id": asset_id,
        "content_hash": content_hash,
        "created_at": created_at.isoformat(),
        "slug": slug,
        "slot": slot,
        "model": model,
        "archive_reason": archive_reason,
        "width": width,
        "height": height,
        "byte_count": len(image_bytes),
        "storage_key": image_key,
        "preview_storage_key": thumbnail_key,
        "url": canonical_url,
        "description": description,
    }
    metadata = {
        **entry,
        "source_prompt": prompt_source_path(prompt_path),
        "description_basis": "reviewed_generation_prompt",
        "generation_prompt": prompt,
    }
    client = visual_s3_client()
    thumbnail_bytes = create_visual_thumbnail(image_bytes)
    visual_s3_put(
        client,
        image_key,
        image_bytes,
        "image/png",
        cache_control="public, max-age=31536000, immutable",
    )
    visual_s3_put(
        client,
        thumbnail_key,
        thumbnail_bytes,
        "image/webp",
        cache_control="public, max-age=31536000, immutable",
    )
    visual_s3_put(
        client,
        metadata_key,
        yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).encode("utf-8"),
        "application/yaml; charset=utf-8",
    )
    visual_s3_put(
        client,
        readme_key,
        render_library_readme(
            asset_id=asset_id,
            created_at=created_at.isoformat(),
            slug=slug,
            slot=slot,
            model=model,
            archive_reason=archive_reason,
            width=width,
            height=height,
            byte_count=len(image_bytes),
            description=description,
        ).encode("utf-8"),
        "text/markdown; charset=utf-8",
    )

    library_key = visual_library_manifest_key(slug=slug, slot=slot)
    library = visual_s3_get_json(client, library_key) or {
        "slug": slug,
        "slot": slot,
        "assets": [],
    }
    assets = [item for item in library.get("assets", []) if item.get("asset_id") != asset_id]
    library["assets"] = [entry, *assets]
    library["updated_at"] = created_at.isoformat()
    visual_s3_put_json(client, library_key, library)
    if activate:
        visual_s3_put_json(
            client, visual_active_manifest_key(slug=slug, slot=slot), entry
        )
    if db is not None:
        asset = register_visual_asset(
            db,
            asset_id=asset_id,
            content_hash=content_hash,
            storage_key=image_key,
            preview_storage_key=thumbnail_key,
            source_lesson_slug=slug,
            source_slot=slot,
            model=model,
            archive_reason=archive_reason,
            width=width,
            height=height,
            byte_count=len(image_bytes),
            description=description,
            prompt_text=prompt,
            created_at=created_at,
        )
        if activate:
            activate_visual_asset(db, lesson_slug=slug, slot=slot, asset_id=asset.id)
        db.commit()

    logger.info(
        "lesson_visual_s3_stored slug=%s slot=%s source=%s asset_id=%s bytes=%s",
        slug,
        slot,
        archive_reason,
        asset_id,
        len(image_bytes),
    )
    return RegeneratedLessonVisual(
        slug=slug,
        slot=slot,
        model=model,
        version=asset_id,
        byte_count=len(image_bytes),
        library_asset_id=asset_id,
        library_relative_path=asset_prefix,
    )


def list_lesson_visual_library(
    *, slug: str, slot: str, db: Optional[Session] = None
) -> dict:
    resolve_lesson_visual_prompt(slug=slug, slot=slot)
    ensure_visual_s3_configured()
    client = visual_s3_client()
    if db is not None:
        active = get_active_visual_asset(db, lesson_slug=slug, slot=slot)
        assets = [
            {
                **visual_asset_entry(asset),
                "is_active": active is not None and asset.id == active.id,
                "preview_url": visual_s3_playback_url(
                    asset.preview_storage_key, client=client
                ),
            }
            for asset in list_visual_assets(db, slot=slot)
        ]
        return {
            "slug": slug,
            "slot": slot,
            "active_asset_id": active.id if active is not None else None,
            "assets": assets,
        }
    library = visual_s3_get_json(client, visual_library_manifest_key(slug=slug, slot=slot)) or {
        "slug": slug,
        "slot": slot,
        "assets": [],
    }
    active = visual_s3_get_json(client, visual_active_manifest_key(slug=slug, slot=slot))
    active_id = active.get("asset_id") if active else None
    assets = []
    for item in library.get("assets", []):
        storage_key = str(item.get("storage_key") or "")
        if not storage_key:
            continue
        preview_storage_key = str(item.get("preview_storage_key") or storage_key)
        assets.append(
            {
                **item,
                "is_active": item.get("asset_id") == active_id,
                "preview_url": visual_s3_playback_url(preview_storage_key, client=client),
            }
        )
    return {"slug": slug, "slot": slot, "active_asset_id": active_id, "assets": assets}


def select_lesson_visual_asset(
    *, slug: str, slot: str, asset_id: str, db: Optional[Session] = None
) -> RegeneratedLessonVisual:
    if db is not None:
        resolve_lesson_visual_prompt(slug=slug, slot=slot)
        asset = get_visual_asset(db, asset_id=asset_id)
        if asset is None or not visual_asset_compatible(asset, slot=slot):
            raise LessonVisualRegenerationError("lesson_visual_library_asset_not_found")
        activate_visual_asset(db, lesson_slug=slug, slot=slot, asset_id=asset.id)
        db.commit()
        active = visual_asset_entry(asset)
        visual_s3_put_json(
            visual_s3_client(),
            visual_active_manifest_key(slug=slug, slot=slot),
            active,
        )
        return regenerated_visual_from_asset(asset, slug=slug, slot=slot)

    library = list_lesson_visual_library(slug=slug, slot=slot)
    selected = next((item for item in library["assets"] if item.get("asset_id") == asset_id), None)
    if selected is None:
        raise LessonVisualRegenerationError("lesson_visual_library_asset_not_found")
    active = {key: value for key, value in selected.items() if key not in {"is_active", "preview_url"}}
    visual_s3_put_json(
        visual_s3_client(),
        visual_active_manifest_key(slug=slug, slot=slot),
        active,
    )
    return RegeneratedLessonVisual(
        slug=slug,
        slot=slot,
        model=str(active.get("model") or "library"),
        version=asset_id,
        byte_count=int(active.get("byte_count") or 0),
        library_asset_id=asset_id,
        library_relative_path=str(active.get("storage_key") or ""),
    )


def get_active_lesson_visual(
    *, slug: str, slot: str, db: Optional[Session] = None
) -> Optional[dict]:
    resolve_lesson_visual_prompt(slug=slug, slot=slot)
    ensure_visual_s3_configured()
    client = visual_s3_client()
    if db is not None:
        asset = get_active_visual_asset(db, lesson_slug=slug, slot=slot)
        if asset is not None:
            return {
                **visual_asset_entry(asset),
                "asset_url": visual_s3_playback_url(asset.storage_key, client=client),
                "version": asset.id,
            }
    active = visual_s3_get_json(
        client,
        visual_active_manifest_key(slug=slug, slot=slot),
    )
    if not active or not active.get("storage_key"):
        return None
    return {
        **active,
        "asset_url": visual_s3_playback_url(str(active["storage_key"]), client=client),
        "version": str(active.get("asset_id") or ""),
    }


def visual_asset_entry(asset: LessonVisualAssetModel) -> dict:
    return {
        "asset_id": asset.id,
        "content_hash": asset.content_hash,
        "created_at": asset.created_at.isoformat(),
        "slug": asset.source_lesson_slug or "",
        "slot": asset.source_slot,
        "model": asset.model,
        "archive_reason": asset.archive_reason,
        "width": asset.width,
        "height": asset.height,
        "byte_count": asset.byte_count,
        "storage_key": asset.storage_key,
        "preview_storage_key": asset.preview_storage_key,
        "url": f"s3://{settings.s3_bucket}/{asset.storage_key}",
        "description": asset.description_json,
    }


def visual_asset_compatible(asset: LessonVisualAssetModel, *, slot: str) -> bool:
    return (slot == "hero" and asset.source_slot == "hero") or (
        slot != "hero" and asset.source_slot.startswith("card-")
    )


def regenerated_visual_from_asset(
    asset: LessonVisualAssetModel, *, slug: str, slot: str
) -> RegeneratedLessonVisual:
    return RegeneratedLessonVisual(
        slug=slug,
        slot=slot,
        model=asset.model,
        version=asset.id,
        byte_count=asset.byte_count,
        library_asset_id=asset.id,
        library_relative_path=asset.storage_key.rsplit("/image.png", 1)[0],
    )


def get_public_visual_asset(*, asset_id: str, db: Session) -> Optional[dict]:
    asset = get_visual_asset(db, asset_id=asset_id)
    if asset is None:
        return None
    client = visual_s3_client()
    return {
        **visual_asset_entry(asset),
        "version": asset.id,
        "asset_url": visual_s3_playback_url(asset.storage_key, client=client),
        "preview_url": visual_s3_playback_url(
            asset.preview_storage_key, client=client
        ),
    }


def get_visual_placement_manifest(*, db: Session) -> dict:
    placements: dict[str, dict[str, dict[str, dict]]] = {}
    latest_version = ""
    for placement, asset in list_visual_placements(db):
        latest_version = max(latest_version, placement.updated_at.isoformat())
        owner = placements.setdefault(placement.owner_type, {}).setdefault(
            placement.owner_key, {}
        )
        owner[placement.slot] = {
            "asset_id": asset.id,
            "width": asset.width,
            "height": asset.height,
            "alt": str(
                asset.description_json.get("subject")
                or "Conversease course visual"
            ),
        }
    return {"version": latest_version or "empty", "placements": placements}


def validate_visual_placement(*, owner_type: str, owner_key: str, slot: str) -> None:
    if owner_type not in VALID_PLACEMENT_OWNER_TYPES:
        raise LessonVisualRegenerationError("invalid_visual_placement_owner")
    if slot not in VALID_PLACEMENT_SLOTS:
        raise LessonVisualRegenerationError("invalid_visual_placement_slot")
    if not re.fullmatch(r"[a-z0-9]+(?:[a-z0-9:-]*[a-z0-9])?", owner_key):
        raise LessonVisualRegenerationError("invalid_visual_placement_owner")


def placement_storage_slug(*, owner_type: str, owner_key: str, slot: str) -> str:
    digest = hashlib.sha256(f"{owner_type}:{owner_key}:{slot}".encode("utf-8")).hexdigest()[:20]
    return f"placement-{digest}"


def placement_visual_entry(
    asset: LessonVisualAssetModel,
    *,
    owner_type: str,
    owner_key: str,
    slot: str,
    current: bool = True,
) -> dict:
    client = visual_s3_client()
    return {
        **visual_asset_entry(asset),
        "owner_type": owner_type,
        "owner_key": owner_key,
        "placement_slot": slot,
        "is_current": current,
        "asset_url": visual_s3_playback_url(asset.storage_key, client=client),
        "preview_url": visual_s3_playback_url(asset.preview_storage_key, client=client),
    }


def pin_visual_placement_asset(
    *,
    owner_type: str,
    owner_key: str,
    slot: str,
    asset_id: str,
    db: Session,
) -> dict:
    validate_visual_placement(owner_type=owner_type, owner_key=owner_key, slot=slot)
    asset = get_visual_asset(db, asset_id=asset_id)
    if asset is None or asset.source_slot != "hero":
        raise LessonVisualRegenerationError("visual_placement_asset_not_found")
    assign_visual_placement(
        db,
        owner_type=owner_type,
        owner_key=owner_key,
        slot=slot,
        asset_id=asset.id,
        mode="pinned",
        source_lesson_slug=None,
        source_slot=None,
    )
    db.commit()
    return placement_visual_entry(
        asset,
        owner_type=owner_type,
        owner_key=owner_key,
        slot=slot,
    )


def store_visual_placement_image(
    *,
    owner_type: str,
    owner_key: str,
    slot: str,
    prompt: str,
    image_bytes: bytes,
    model: str,
    archive_reason: str,
    db: Session,
) -> dict:
    validate_visual_placement(owner_type=owner_type, owner_key=owner_key, slot=slot)
    prompt = prompt.strip()
    if not prompt or len(prompt) > 30_000:
        raise LessonVisualRegenerationError("visual_placement_prompt_invalid")
    normalized_image = normalize_uploaded_image(image_bytes=image_bytes, slot="hero")
    result = store_lesson_visual(
        slug=placement_storage_slug(owner_type=owner_type, owner_key=owner_key, slot=slot),
        slot="hero",
        prompt_path=PLACEMENT_PROMPT_PATH,
        prompt=prompt,
        image_bytes=normalized_image,
        model=model,
        archive_reason=archive_reason,
        overrides_dir=None,
        db=db,
        activate=False,
    )
    return pin_visual_placement_asset(
        owner_type=owner_type,
        owner_key=owner_key,
        slot=slot,
        asset_id=result.library_asset_id,
        db=db,
    )


async def regenerate_visual_placement(
    *,
    owner_type: str,
    owner_key: str,
    slot: str,
    prompt: str,
    db: Session,
    image_client: Optional[TogetherImageClient] = None,
) -> dict:
    validate_visual_placement(owner_type=owner_type, owner_key=owner_key, slot=slot)
    prompt = prompt.strip()
    if not prompt or len(prompt) > 30_000:
        raise LessonVisualRegenerationError("visual_placement_prompt_invalid")
    client = image_client or TogetherImageClient(
        api_key=settings.together_api_key,
        base_url=settings.together_image_base_url,
        model=settings.together_image_model,
        timeout_seconds=settings.together_image_timeout_seconds,
    )
    generated = await client.generate_png(prompt=prompt, slot="hero")
    optimized = await asyncio.to_thread(optimize_png, generated)
    return await asyncio.to_thread(
        store_visual_placement_image,
        owner_type=owner_type,
        owner_key=owner_key,
        slot=slot,
        prompt=prompt,
        image_bytes=optimized,
        model=settings.together_image_model,
        archive_reason="placement_generation",
        db=db,
    )


async def import_visual_placement_from_url(
    *,
    owner_type: str,
    owner_key: str,
    slot: str,
    prompt: str,
    url: str,
    db: Session,
) -> dict:
    image_bytes = await download_remote_image(url)
    return await asyncio.to_thread(
        store_visual_placement_image,
        owner_type=owner_type,
        owner_key=owner_key,
        slot=slot,
        prompt=prompt,
        image_bytes=image_bytes,
        model="url-import",
        archive_reason="placement_url_import",
        db=db,
    )


def list_visual_placement_library(
    *, owner_type: str, owner_key: str, slot: str, db: Session
) -> dict:
    validate_visual_placement(owner_type=owner_type, owner_key=owner_key, slot=slot)
    placement = get_visual_placement(
        db, owner_type=owner_type, owner_key=owner_key, slot=slot
    )
    current_id = placement.asset_id if placement is not None else None
    assets = [
        placement_visual_entry(
            asset,
            owner_type=owner_type,
            owner_key=owner_key,
            slot=slot,
            current=asset.id == current_id,
        )
        for asset in list_visual_assets(db, slot="hero")
    ]
    return {"current_asset_id": current_id, "assets": assets}


def visual_library_manifest_key(*, slug: str, slot: str) -> str:
    return f"lesson-visuals/library/{slug}/{slot}/library.json"


def visual_active_manifest_key(*, slug: str, slot: str) -> str:
    return f"lesson-visuals/active/{slug}/{slot}.json"


def ensure_visual_s3_configured() -> None:
    if not (
        settings.s3_bucket
        and settings.aws_access_key_id
        and settings.aws_secret_access_key
        and settings.aws_region
    ):
        raise LessonVisualRegenerationError("s3_config_missing")


@lru_cache(maxsize=1)
def visual_s3_client():
    try:
        import boto3
    except ImportError as exc:
        raise LessonVisualRegenerationError("boto3_missing") from exc
    return boto3.client(
        "s3",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )


def visual_s3_put(
    client,
    key: str,
    body: bytes,
    content_type: str,
    *,
    cache_control: str = "no-cache",
) -> None:
    try:
        client.put_object(
            Bucket=settings.s3_bucket,
            Key=key,
            Body=body,
            ContentType=content_type,
            CacheControl=cache_control,
        )
    except Exception as exc:
        raise LessonVisualRegenerationError("s3_visual_write_failed") from exc


def visual_s3_put_json(client, key: str, value: dict) -> None:
    visual_s3_put(
        client,
        key,
        json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
        "application/json",
    )


def visual_s3_get_json(client, key: str) -> Optional[dict]:
    try:
        response = client.get_object(Bucket=settings.s3_bucket, Key=key)
    except Exception as exc:
        code = str(getattr(exc, "response", {}).get("Error", {}).get("Code", ""))
        if code in {"NoSuchKey", "404", "NotFound"}:
            return None
        raise LessonVisualRegenerationError("s3_visual_read_failed") from exc
    try:
        value = json.loads(response["Body"].read().decode("utf-8"))
    except (KeyError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LessonVisualRegenerationError("s3_visual_manifest_invalid") from exc
    if not isinstance(value, dict):
        raise LessonVisualRegenerationError("s3_visual_manifest_invalid")
    return value


def visual_s3_playback_url(storage_key: str, *, client=None) -> str:
    if settings.s3_public_base_url:
        return f"{settings.s3_public_base_url.rstrip('/')}/{quote(storage_key)}"
    try:
        signer = client or visual_s3_client()
        return signer.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.s3_bucket, "Key": storage_key},
            ExpiresIn=settings.s3_presigned_url_expires_seconds,
        )
    except Exception as exc:
        raise LessonVisualRegenerationError("s3_visual_url_failed") from exc


def archive_lesson_visual(
    *,
    library_root: Path,
    slug: str,
    slot: str,
    prompt_path: Path,
    prompt: str,
    image_bytes: bytes,
    model: str,
    archive_reason: str,
) -> Tuple[str, str]:
    """Preserve every generated visual with searchable human-readable context."""
    created_at = datetime.now(timezone.utc)
    asset_id = f"{created_at.strftime('%Y%m%dT%H%M%S%fZ')}-{uuid4().hex[:8]}"
    relative_dir = Path(slug) / slot / asset_id
    destination = library_root / relative_dir
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_dir = Path(tempfile.mkdtemp(dir=destination.parent, prefix=f".{asset_id}."))

    description = visual_description(prompt_path=prompt_path, prompt=prompt, slot=slot)
    width, height = image_dimensions(image_bytes)
    try:
        atomic_write(temporary_dir / "image.png", image_bytes)
        atomic_write(
            temporary_dir / "metadata.yaml",
            yaml.safe_dump(
                {
                    "asset_id": asset_id,
                    "created_at": created_at.isoformat(),
                    "slug": slug,
                    "slot": slot,
                    "model": model,
                    "archive_reason": archive_reason,
                    "width": width,
                    "height": height,
                    "byte_count": len(image_bytes),
                    "source_prompt": prompt_source_path(prompt_path),
                    "description_basis": "reviewed_generation_prompt",
                    "description": description,
                    "generation_prompt": prompt,
                },
                allow_unicode=True,
                sort_keys=False,
            ).encode("utf-8"),
        )
        atomic_write(
            temporary_dir / "README.md",
            render_library_readme(
                asset_id=asset_id,
                created_at=created_at.isoformat(),
                slug=slug,
                slot=slot,
                model=model,
                archive_reason=archive_reason,
                width=width,
                height=height,
                byte_count=len(image_bytes),
                description=description,
            ).encode("utf-8"),
        )
        os.replace(temporary_dir, destination)
    except Exception:
        shutil.rmtree(temporary_dir, ignore_errors=True)
        raise

    return asset_id, relative_dir.as_posix()


def archive_existing_override_if_needed(
    *,
    target_path: Path,
    library_root: Path,
    slug: str,
    slot: str,
    prompt_path: Path,
    prompt: str,
) -> None:
    """Backfill an override created before library tracking without duplicating tracked assets."""
    marker_path = archive_marker_path(target_path)
    if not target_path.exists() or marker_path.exists():
        return

    existing_bytes = target_path.read_bytes()
    validate_png(existing_bytes)
    asset_id, _ = archive_lesson_visual(
        library_root=library_root,
        slug=slug,
        slot=slot,
        prompt_path=prompt_path,
        prompt=prompt,
        image_bytes=existing_bytes,
        model="unknown-pre-library",
        archive_reason="preserved_existing_override",
    )
    atomic_write(marker_path, asset_id.encode("utf-8"))


def archive_marker_path(target_path: Path) -> Path:
    return target_path.with_suffix(".library-asset-id")


def visual_description(*, prompt_path: Path, prompt: str, slot: str) -> dict:
    document = prompt_path.read_text(encoding="utf-8")
    people = []
    cast_match = re.search(
        r"^Cast and continuity:\s*\n(?P<cast>(?:- .*\n?)+)",
        prompt,
        re.MULTILINE,
    )
    if cast_match:
        for line in cast_match.group("cast").splitlines():
            match = re.match(r"-\s+([^:]+):\s*(.+)", line)
            if match:
                people.append({"name": match.group(1).strip(), "description": match.group(2).strip()})

    return {
        "lesson": markdown_numbered_metadata(document, "Lesson") or prompt_value(prompt, "Lesson"),
        "unit": markdown_numbered_metadata(document, "Unit"),
        "level": markdown_metadata(document, "Level"),
        "subject": prompt_value(prompt, "Card focus") or prompt_value(prompt, "Lesson"),
        "conversation_goal": prompt_value(prompt, "Conversation goal"),
        "context": prompt_value(prompt, "Situation") or prompt_value(prompt, "Conversation moment"),
        "setting": prompt_list_value(prompt, "Actual conversation location"),
        "background": prompt_list_value(prompt, "Required background cues"),
        "context_guardrail": prompt_list_value(prompt, "Context guardrail"),
        "people": people,
        "slot_purpose": "Main lesson image" if slot == "hero" else f"Lesson companion {slot}",
    }


def markdown_metadata(document: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}:\s+\*\*(.+?)\*\*\s*$", document, re.MULTILINE)
    return match.group(1).strip() if match else ""


def markdown_numbered_metadata(document: str, label: str) -> str:
    match = re.search(
        rf"^- {re.escape(label)} \d+:\s+\*\*(.+?)\*\*\s*$",
        document,
        re.MULTILINE,
    )
    return match.group(1).strip() if match else ""


def prompt_value(prompt: str, label: str) -> str:
    match = re.search(rf"^{re.escape(label)}:\s*(.+)$", prompt, re.MULTILINE)
    return match.group(1).strip().strip("“”\"") if match else ""


def prompt_list_value(prompt: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}:\s*(.+)$", prompt, re.MULTILINE)
    return match.group(1).strip() if match else ""


def prompt_source_path(prompt_path: Path) -> str:
    try:
        return prompt_path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(prompt_path)


def image_dimensions(image_bytes: bytes) -> Tuple[int, int]:
    with Image.open(BytesIO(image_bytes)) as image:
        return image.size


def render_library_readme(
    *,
    asset_id: str,
    created_at: str,
    slug: str,
    slot: str,
    model: str,
    archive_reason: str,
    width: int,
    height: int,
    byte_count: int,
    description: dict,
) -> str:
    people = description.get("people") or []
    people_lines = "\n".join(
        f"- **{person['name']}** — {person['description']}" for person in people
    ) or "- Tidak ada karakter bernama yang tercatat."
    return f"""# Generated lesson visual

![Generated visual](./image.png)

- Asset ID: `{asset_id}`
- Generated: `{created_at}`
- Lesson: **{description.get('lesson') or slug}**
- Slot: `{slot}` ({description.get('slot_purpose')})
- Model: `{model}`
- Archive reason: `{archive_reason}`
- Dimensions: `{width}×{height}`
- File size: `{byte_count}` bytes

## Tentang gambar

- **Subjek:** {description.get('subject') or '-'}
- **Konteks percakapan:** {description.get('context') or description.get('conversation_goal') or '-'}
- **Latar:** {description.get('setting') or '-'}
- **Elemen latar:** {description.get('background') or '-'}
- **Batas konteks:** {description.get('context_guardrail') or '-'}

## Siapa saja di dalam gambar

{people_lines}

Lihat `metadata.yaml` untuk metadata terstruktur dan prompt generasi lengkap.
Keterangan isi gambar disusun dari prompt generasi yang telah direview.
"""


def atomic_write(target_path: Path, image_bytes: bytes) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=target_path.parent,
        prefix=f".{target_path.name}.",
        suffix=".tmp",
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as output:
            output.write(image_bytes)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary_path, target_path)
    finally:
        temporary_path.unlink(missing_ok=True)


def read_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}
