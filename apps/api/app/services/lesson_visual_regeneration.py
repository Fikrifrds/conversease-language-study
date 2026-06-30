from __future__ import annotations

import base64
import binascii
from io import BytesIO
from dataclasses import dataclass
from functools import lru_cache
import logging
import os
from pathlib import Path
import re
import tempfile
import time
from typing import Dict, Optional, Tuple

import httpx
from PIL import Image, UnidentifiedImageError
import yaml

from app.core.config import settings


REPO_ROOT = Path(__file__).resolve().parents[4]
CURRICULUM_ROOT = REPO_ROOT / "content" / "curriculum" / "english"
PROMPT_ROOT = REPO_ROOT / "content" / "visual-prompts" / "english"
VALID_SLOTS = ("hero", "card-1", "card-2", "card-3")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_IMAGE_BYTES = 30 * 1024 * 1024
PNG_PALETTE_COLORS = 256

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
            "response_format": "base64",
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
) -> RegeneratedLessonVisual:
    if slot not in VALID_SLOTS:
        raise LessonVisualRegenerationError("invalid_visual_slot")

    prompt_path = lesson_prompt_index().get(slug)
    if prompt_path is None:
        raise LessonVisualRegenerationError("lesson_visual_prompt_not_found")

    prompt = extract_visual_prompt(prompt_path, slot)
    client = image_client or TogetherImageClient(
        api_key=settings.together_api_key,
        base_url=settings.together_api_base_url,
        model=settings.together_image_model,
        timeout_seconds=settings.together_image_timeout_seconds,
    )
    image_bytes = await client.generate_png(prompt=prompt, slot=slot)
    validate_png(image_bytes)
    optimized_image_bytes = optimize_png(image_bytes)

    root = overrides_dir or Path(settings.lesson_visual_overrides_dir)
    target_path = override_path(root=root, slug=slug, slot=slot)
    atomic_write(target_path, optimized_image_bytes)
    version = str(target_path.stat().st_mtime_ns)

    logger.info(
        "lesson_visual_optimized slug=%s slot=%s original_bytes=%s stored_bytes=%s",
        slug,
        slot,
        len(image_bytes),
        len(optimized_image_bytes),
    )

    return RegeneratedLessonVisual(
        slug=slug,
        slot=slot,
        model=settings.together_image_model,
        version=version,
        byte_count=len(optimized_image_bytes),
    )


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
    return prompt


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
