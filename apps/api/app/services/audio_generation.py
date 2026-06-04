from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import quote

import httpx
import yaml

from app.core.config import settings
from app.data.curriculum import curriculum_root, production_tracker_path


MINIMAX_TTS_MODELS = (
    "speech-2.8-hd",
    "speech-2.8-turbo",
    "speech-2.6-hd",
    "speech-2.6-turbo",
    "speech-02-hd",
    "speech-02-turbo",
    "speech-01-hd",
    "speech-01-turbo",
)

FALLBACK_MINIMAX_VOICES = (
    {
        "voice_id": "English_expressive_narrator",
        "voice_name": "Expressive Narrator",
        "category": "system",
        "description": "Clear narrator voice for lesson listening scripts.",
    },
    {
        "voice_id": "English_Trustworth_Man",
        "voice_name": "Trustworthy Man",
        "category": "system",
        "description": "Steady male voice for instructional dialogue.",
    },
    {
        "voice_id": "English_CalmWoman",
        "voice_name": "Calm Woman",
        "category": "system",
        "description": "Calm female voice for beginner listening practice.",
    },
    {
        "voice_id": "English_magnetic_voiced_man",
        "voice_name": "Magnetic-voiced Male",
        "category": "system",
        "description": "Confident male voice with good presence.",
    },
    {
        "voice_id": "English_Upbeat_Woman",
        "voice_name": "Upbeat Woman",
        "category": "system",
        "description": "Friendly female voice for light conversation.",
    },
    {
        "voice_id": "English_FriendlyPerson",
        "voice_name": "Friendly Guy",
        "category": "system",
        "description": "Warm, casual voice for social dialogue.",
    },
)


class AudioGenerationError(Exception):
    pass


@dataclass(frozen=True)
class LessonAudioReference:
    language: str
    level_code: str
    unit_key: str
    lesson_key: str
    lesson_slug: str
    title: str
    lesson_dir: Path
    listening_script_path: Path
    audio_manifest_path: Path


@dataclass(frozen=True)
class MiniMaxAudioResult:
    audio_bytes: bytes
    duration_seconds: float
    audio_format: str
    audio_size: int
    trace_id: str
    usage_characters: int


def audio_generation_settings_payload(voices: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "minimax_configured": bool(settings.minimax_api_key),
        "s3_configured": s3_configured(),
        "default_model": default_minimax_tts_model(),
        "default_voice_id": settings.minimax_tts_voice_id,
        "default_language_boost": settings.minimax_tts_language_boost,
        "models": list(MINIMAX_TTS_MODELS),
        "voices": voices,
    }


async def audio_generation_settings() -> dict[str, Any]:
    voices = await list_minimax_voices()
    return audio_generation_settings_payload(voices)


async def list_minimax_voices(
    *,
    voice_type: str = "all",
    language: str = "English",
    limit: int = 100,
) -> list[dict[str, Any]]:
    if not settings.minimax_api_key:
        return list(FALLBACK_MINIMAX_VOICES)

    try:
        response = await minimax_client_post(
            "/v1/get_voice",
            {"voice_type": voice_type},
            timeout=min(settings.minimax_tts_timeout_seconds, 30),
        )
    except AudioGenerationError:
        return list(FALLBACK_MINIMAX_VOICES)

    voices = flatten_minimax_voices(response)
    filtered = filter_voice_options(voices, language=language)
    return filtered[:limit] or list(FALLBACK_MINIMAX_VOICES)


def flatten_minimax_voices(payload: dict[str, Any]) -> list[dict[str, Any]]:
    voice_groups = (
        ("system_voice", "system"),
        ("voice_cloning", "voice_cloning"),
        ("voice_generation", "voice_generation"),
    )
    voices: list[dict[str, Any]] = []

    for source_key, category in voice_groups:
        for voice in payload.get(source_key, []) or []:
            if not isinstance(voice, dict) or not voice.get("voice_id"):
                continue
            description = voice.get("description") or []
            description_text = " ".join(str(item) for item in description if item)
            voice_id = str(voice["voice_id"])
            voices.append(
                {
                    "voice_id": voice_id,
                    "voice_name": str(voice.get("voice_name") or readable_voice_name(voice_id)),
                    "category": category,
                    "description": description_text,
                }
            )

    return voices


def filter_voice_options(voices: list[dict[str, Any]], *, language: str) -> list[dict[str, Any]]:
    language_prefix = f"{language}_"
    custom_categories = {"voice_cloning", "voice_generation"}
    preferred = [
        voice
        for voice in voices
        if str(voice.get("voice_id", "")).startswith(language_prefix)
        or voice.get("category") in custom_categories
    ]

    default_voice_id = settings.minimax_tts_voice_id
    if default_voice_id and all(voice.get("voice_id") != default_voice_id for voice in preferred):
        matched_default = next(
            (voice for voice in voices if voice.get("voice_id") == default_voice_id),
            None,
        )
        if matched_default:
            preferred.insert(0, matched_default)

    return preferred


def readable_voice_name(voice_id: str) -> str:
    name = voice_id
    if "_" in name:
        name = name.split("_", 1)[1]
    return name.replace("_", " ").replace("-", " ").strip().title() or voice_id


async def generate_lesson_listening_audio(
    *,
    lesson_slug: str,
    model: Optional[str] = None,
    voice_id: Optional[str] = None,
    speed: float = 1.0,
    generated_by: str = "admin",
) -> dict[str, Any]:
    if not settings.minimax_api_key:
        raise AudioGenerationError("minimax_api_key_missing")
    if not s3_configured():
        raise AudioGenerationError("s3_config_missing")

    lesson = find_lesson_audio_reference(lesson_slug)
    tts_text = listening_script_to_tts_text(lesson.listening_script_path)
    selected_model = normalized_model(model or settings.minimax_tts_model)
    selected_voice_id = (voice_id or settings.minimax_tts_voice_id).strip()
    if not selected_voice_id:
        raise AudioGenerationError("minimax_voice_id_missing")

    generated = await synthesize_minimax_tts(
        text=tts_text,
        model=selected_model,
        voice_id=selected_voice_id,
        speed=speed,
        language_boost=settings.minimax_tts_language_boost,
    )

    generated_at = datetime.now(timezone.utc)
    object_key = audio_object_key(
        lesson=lesson,
        voice_id=selected_voice_id,
        generated_at=generated_at,
        extension=generated.audio_format,
    )
    audio_url = upload_audio_to_s3(
        audio_bytes=generated.audio_bytes,
        object_key=object_key,
        content_type=content_type_for_audio_format(generated.audio_format),
    )
    playback_url = audio_playback_url(audio_url=audio_url, storage_key=object_key)

    manifest = update_audio_manifest(
        lesson=lesson,
        audio_url=audio_url,
        object_key=object_key,
        duration_seconds=generated.duration_seconds,
        audio_format=generated.audio_format,
        model=selected_model,
        voice_id=selected_voice_id,
        trace_id=generated.trace_id,
        generated_by=generated_by,
        generated_at=generated_at,
    )
    update_production_tracker_audio(lesson, status="done")

    return {
        "lesson_slug": lesson.lesson_slug,
        "lesson_key": lesson.lesson_key,
        "title": lesson.title,
        "audio_url": audio_url,
        "playback_url": playback_url,
        "object_key": object_key,
        "duration_seconds": generated.duration_seconds,
        "audio_format": generated.audio_format,
        "audio_size": generated.audio_size,
        "model": selected_model,
        "voice_id": selected_voice_id,
        "trace_id": generated.trace_id,
        "usage_characters": generated.usage_characters,
        "manifest": manifest,
    }


async def generate_voice_preview_audio(
    *,
    model: Optional[str] = None,
    voice_id: Optional[str] = None,
    speed: float = 1.0,
    generated_by: str = "admin",
    sample_text: Optional[str] = None,
) -> dict[str, Any]:
    if not settings.minimax_api_key:
        raise AudioGenerationError("minimax_api_key_missing")
    if not s3_configured():
        raise AudioGenerationError("s3_config_missing")

    selected_model = normalized_model(model or settings.minimax_tts_model)
    selected_voice_id = (voice_id or settings.minimax_tts_voice_id).strip()
    if not selected_voice_id:
        raise AudioGenerationError("minimax_voice_id_missing")

    preview_text = (
        sample_text
        or "Hello, welcome to Conversease. Listen, repeat, and speak with clear confidence."
    ).strip()
    if len(preview_text) < 8:
        raise AudioGenerationError("voice_preview_text_empty")
    if len(preview_text) > 500:
        raise AudioGenerationError("voice_preview_text_too_long")

    generated = await synthesize_minimax_tts(
        text=preview_text,
        model=selected_model,
        voice_id=selected_voice_id,
        speed=speed,
        language_boost=settings.minimax_tts_language_boost,
    )

    generated_at = datetime.now(timezone.utc)
    object_key = voice_preview_object_key(
        voice_id=selected_voice_id,
        generated_at=generated_at,
        extension=generated.audio_format,
    )
    audio_url = upload_audio_to_s3(
        audio_bytes=generated.audio_bytes,
        object_key=object_key,
        content_type=content_type_for_audio_format(generated.audio_format),
    )
    playback_url = audio_playback_url(audio_url=audio_url, storage_key=object_key)

    return {
        "audio_url": audio_url,
        "playback_url": playback_url,
        "object_key": object_key,
        "duration_seconds": generated.duration_seconds,
        "audio_format": generated.audio_format,
        "audio_size": generated.audio_size,
        "model": selected_model,
        "voice_id": selected_voice_id,
        "trace_id": generated.trace_id,
        "usage_characters": generated.usage_characters,
        "sample_text": preview_text,
        "generated_by": generated_by,
        "generated_at": generated_at.isoformat(),
    }


async def synthesize_minimax_tts(
    *,
    text: str,
    model: str,
    voice_id: str,
    speed: float,
    language_boost: str,
) -> MiniMaxAudioResult:
    payload = {
        "model": model,
        "text": text,
        "stream": False,
        "language_boost": language_boost or "auto",
        "output_format": "hex",
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": 1,
            "pitch": 0,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
    }
    body = await minimax_client_post(
        "/v1/t2a_v2",
        payload,
        timeout=settings.minimax_tts_timeout_seconds,
    )

    data = body.get("data") or {}
    audio_hex = data.get("audio")
    if not isinstance(audio_hex, str) or not audio_hex:
        raise AudioGenerationError("minimax_audio_empty")

    try:
        audio_bytes = bytes.fromhex(audio_hex)
    except ValueError as exc:
        raise AudioGenerationError("minimax_audio_invalid_hex") from exc

    extra_info = body.get("extra_info") or {}
    duration_seconds = duration_from_extra_info(extra_info)
    audio_format = str(extra_info.get("audio_format") or "mp3")

    return MiniMaxAudioResult(
        audio_bytes=audio_bytes,
        duration_seconds=duration_seconds,
        audio_format=audio_format,
        audio_size=int(extra_info.get("audio_size") or len(audio_bytes)),
        trace_id=str(body.get("trace_id") or ""),
        usage_characters=int(extra_info.get("usage_characters") or len(text)),
    )


async def minimax_client_post(path: str, payload: dict[str, Any], *, timeout: int) -> dict[str, Any]:
    base_url = settings.minimax_api_base_url.rstrip("/")
    headers = {
        "Authorization": f"Bearer {settings.minimax_api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(f"{base_url}{path}", headers=headers, json=payload)
            response.raise_for_status()
            body = response.json()
    except httpx.HTTPError as exc:
        raise AudioGenerationError("minimax_request_failed") from exc
    except ValueError as exc:
        raise AudioGenerationError("minimax_response_invalid_json") from exc

    base_resp = body.get("base_resp") or {}
    if int(base_resp.get("status_code") or 0) != 0:
        message = str(base_resp.get("status_msg") or "minimax_error")
        raise AudioGenerationError(f"minimax_error:{message}")

    return body


def duration_from_extra_info(extra_info: dict[str, Any]) -> float:
    raw_duration = extra_info.get("audio_length")
    try:
        duration = float(raw_duration)
    except (TypeError, ValueError):
        duration = 0

    if duration > 1000:
        duration = duration / 1000

    return round(max(duration, 0.01), 2)


def normalized_model(value: str) -> str:
    model = value.strip()
    if model not in MINIMAX_TTS_MODELS:
        raise AudioGenerationError("invalid_minimax_tts_model")
    return model


def default_minimax_tts_model() -> str:
    model = settings.minimax_tts_model.strip()
    if model in MINIMAX_TTS_MODELS:
        return model
    return MINIMAX_TTS_MODELS[0]


def find_lesson_audio_reference(lesson_slug: str) -> LessonAudioReference:
    for lesson_yaml_path in sorted(curriculum_root().glob("*/*/units/*/*/lesson.yaml")):
        try:
            data = read_yaml_mapping(lesson_yaml_path)
        except AudioGenerationError:
            continue

        if data.get("slug") != lesson_slug:
            continue

        lesson_dir = lesson_yaml_path.parent
        listening_script_path = lesson_dir / "listening_script.md"
        audio_manifest_path = lesson_dir / "audio_manifest.yaml"
        if not listening_script_path.exists():
            raise AudioGenerationError("listening_script_missing")
        if not audio_manifest_path.exists():
            raise AudioGenerationError("audio_manifest_missing")

        return LessonAudioReference(
            language=lesson_yaml_path.parents[4].name,
            level_code=lesson_yaml_path.parents[3].name,
            unit_key=lesson_yaml_path.parents[1].name,
            lesson_key=lesson_yaml_path.parent.name,
            lesson_slug=str(data.get("slug") or ""),
            title=str(data.get("title") or ""),
            lesson_dir=lesson_dir,
            listening_script_path=listening_script_path,
            audio_manifest_path=audio_manifest_path,
        )

    raise AudioGenerationError("lesson_not_found")


def listening_script_to_tts_text(path: Path) -> str:
    raw_text = path.read_text(encoding="utf-8")
    dialogue_text = raw_text.split("## Audio Direction", 1)[0]
    lines = []
    for raw_line in dialogue_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        line = re.sub(r"^\*{0,2}([^:*]+):\*{0,2}\s*", r"\1: ", line)
        line = line.replace("**", "").replace("*", "").replace("  ", " ").strip()
        if line:
            lines.append(line)

    text = "\n".join(lines).strip()
    if len(text) < 8:
        raise AudioGenerationError("listening_script_empty")
    if len(text) >= 10000:
        raise AudioGenerationError("listening_script_too_long_for_sync_tts")
    return text


def upload_audio_to_s3(*, audio_bytes: bytes, object_key: str, content_type: str) -> str:
    client = s3_client()
    client.put_object(
        Bucket=settings.s3_bucket,
        Key=object_key,
        Body=audio_bytes,
        ContentType=content_type,
    )
    return public_s3_url(object_key)


def s3_client():
    try:
        import boto3
    except ImportError as exc:
        raise AudioGenerationError("boto3_missing") from exc

    return boto3.client(
        "s3",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )


def public_s3_url(object_key: str) -> str:
    if settings.s3_public_base_url:
        return f"{settings.s3_public_base_url.rstrip('/')}/{quote(object_key)}"
    bucket = settings.s3_bucket
    region = settings.aws_region
    return f"https://{bucket}.s3.{region}.amazonaws.com/{quote(object_key)}"


def audio_playback_url(*, audio_url: str = "", storage_key: str = "") -> str:
    if storage_key and settings.s3_public_base_url:
        return public_s3_url(storage_key)
    if storage_key and s3_configured():
        try:
            return presigned_s3_url(storage_key)
        except AudioGenerationError:
            return audio_url or public_s3_url(storage_key)
    return audio_url


def presigned_s3_url(object_key: str) -> str:
    client = s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.s3_bucket, "Key": object_key},
        ExpiresIn=settings.s3_presigned_url_expires_seconds,
    )


def update_audio_manifest(
    *,
    lesson: LessonAudioReference,
    audio_url: str,
    object_key: str,
    duration_seconds: float,
    audio_format: str,
    model: str,
    voice_id: str,
    trace_id: str,
    generated_by: str,
    generated_at: datetime,
) -> dict[str, Any]:
    data = read_yaml_mapping(lesson.audio_manifest_path)
    assets = data.get("assets")
    if not isinstance(assets, list):
        assets = []

    dialogue_asset = {
        "key": "dialogue_main",
        "type": "dialogue",
        "script_file": "listening_script.md",
        "audio_url": audio_url,
        "duration_seconds": duration_seconds,
        "provider": "minimax",
        "model": model,
        "voice_id": voice_id,
        "audio_format": audio_format,
        "storage_key": object_key,
        "trace_id": trace_id,
        "generated_by": generated_by,
        "generated_at": generated_at.isoformat(),
    }

    replaced = False
    next_assets = []
    for asset in assets:
        if isinstance(asset, dict) and asset.get("key") == "dialogue_main":
            next_assets.append(dialogue_asset)
            replaced = True
        else:
            next_assets.append(asset)
    if not replaced:
        next_assets.insert(0, dialogue_asset)

    data["lesson_key"] = lesson.lesson_key
    data["status"] = "generated"
    data["provider"] = "minimax"
    data["assets"] = next_assets
    write_yaml_mapping(lesson.audio_manifest_path, data)
    return data


def update_production_tracker_audio(lesson: LessonAudioReference, *, status: str) -> None:
    tracker_path = production_tracker_path()
    if not tracker_path.exists():
        raise AudioGenerationError("production_tracker_missing")

    with tracker_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    if "audio_generated" not in fieldnames:
        raise AudioGenerationError("production_tracker_audio_column_missing")

    updated = False
    for row in rows:
        if (
            row.get("level") == lesson.level_code
            and row.get("unit") == lesson.unit_key
            and row.get("lesson") == lesson.lesson_key
        ):
            row["audio_generated"] = status
            updated = True
            break

    if not updated:
        raise AudioGenerationError("production_tracker_row_missing")

    with tracker_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def audio_object_key(
    *,
    lesson: LessonAudioReference,
    voice_id: str,
    generated_at: datetime,
    extension: str,
) -> str:
    safe_voice_id = re.sub(r"[^A-Za-z0-9_.-]+", "-", voice_id).strip("-")
    timestamp = generated_at.strftime("%Y%m%dT%H%M%SZ")
    extension = re.sub(r"[^a-z0-9]+", "", extension.lower()) or "mp3"
    return (
        "conversease/audio/"
        f"{lesson.language}/{lesson.level_code}/{lesson.unit_key}/{lesson.lesson_key}/"
        f"listening-{safe_voice_id}-{timestamp}.{extension}"
    )


def voice_preview_object_key(*, voice_id: str, generated_at: datetime, extension: str) -> str:
    safe_voice_id = re.sub(r"[^A-Za-z0-9_.-]+", "-", voice_id).strip("-")
    timestamp = generated_at.strftime("%Y%m%dT%H%M%SZ")
    extension = re.sub(r"[^a-z0-9]+", "", extension.lower()) or "mp3"
    return f"conversease/audio/previews/{safe_voice_id}/sample-{timestamp}.{extension}"


def content_type_for_audio_format(audio_format: str) -> str:
    normalized = audio_format.lower()
    if normalized == "wav":
        return "audio/wav"
    if normalized == "flac":
        return "audio/flac"
    return "audio/mpeg"


def s3_configured() -> bool:
    return bool(
        settings.s3_bucket
        and settings.aws_access_key_id
        and settings.aws_secret_access_key
        and settings.aws_region
    )


def read_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise AudioGenerationError(f"invalid_yaml:{path.name}") from exc
    if not isinstance(data, dict):
        raise AudioGenerationError(f"invalid_yaml:{path.name}")
    return data


def write_yaml_mapping(path: Path, data: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(data, allow_unicode=False, sort_keys=False, width=100),
        encoding="utf-8",
    )
