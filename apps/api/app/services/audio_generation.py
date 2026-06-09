from __future__ import annotations

import base64
import csv
import hashlib
import io
import logging
import re
import sys
import wave
from array import array
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import quote

import httpx
import yaml

from app.core.config import settings
from app.data.curriculum import curriculum_root, production_tracker_path
from app.db.exam_models import ExamItemModel, ExamSectionModel, ExamTemplateModel


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

CLEAR_FEMALE_DIALOGUE_VOICES = (
    "English_radiant_girl",
    "English_CalmWoman",
    "English_Upbeat_Woman",
)

CLEAR_MALE_DIALOGUE_VOICES = (
    "English_Gentle-voiced_man",
    "English_Trustworth_Man",
    "English_Diligent_Man",
)

DIALOGUE_TARGET_PEAK_RATIO = 0.82
CURATED_MINIMAX_VOICE_IDS = (
    "English_expressive_narrator",
    *CLEAR_MALE_DIALOGUE_VOICES,
    *CLEAR_FEMALE_DIALOGUE_VOICES,
)
CURATED_MINIMAX_VOICE_METADATA = {
    "English_expressive_narrator": {
        "voice_name": "Expressive Narrator",
        "gender": "neutral",
        "description": "Clear narrator voice for single-speaker lesson audio.",
    },
    "English_Gentle-voiced_man": {
        "voice_name": "Gentle-voiced Man",
        "gender": "male",
        "description": "Solid male voice for calm beginner dialogue.",
    },
    "English_Trustworth_Man": {
        "voice_name": "Trustworthy Man",
        "gender": "male",
        "description": "Solid male voice for steady instructional dialogue.",
    },
    "English_Diligent_Man": {
        "voice_name": "Diligent Man",
        "gender": "male",
        "description": "Solid male voice for clear learner or staff dialogue.",
    },
    "English_radiant_girl": {
        "voice_name": "Radiant Girl",
        "gender": "female",
        "description": "Solid female voice for friendly beginner dialogue.",
    },
    "English_CalmWoman": {
        "voice_name": "Calm Woman",
        "gender": "female",
        "description": "Solid female voice for teacher, helper, and examiner dialogue.",
    },
    "English_Upbeat_Woman": {
        "voice_name": "Upbeat Woman",
        "gender": "female",
        "description": "Solid female voice for light social dialogue.",
    },
}

DIALOGUE_PERSONA_VOICES = {
    "alya": "English_radiant_girl",
    "arif": "English_Trustworth_Man",
    "andi": "English_Gentle-voiced_man",
    "adi": "English_Diligent_Man",
    "ben": "English_Gentle-voiced_man",
    "budi": "English_Diligent_Man",
    "david": "English_Diligent_Man",
    "dimas": "English_Diligent_Man",
    "john": "English_Trustworth_Man",
    "lina": "English_Upbeat_Woman",
    "maya": "English_radiant_girl",
    "mina": "English_Upbeat_Woman",
    "nina": "English_Upbeat_Woman",
    "officer": "English_CalmWoman",
    "omar": "English_Trustworth_Man",
    "raka": "English_Gentle-voiced_man",
    "sara": "English_CalmWoman",
    "staff": "English_CalmWoman",
    # A2-C1 lead characters (paired with Mina, so male for contrast).
    "faris": "English_Trustworth_Man",
    "ilham": "English_Gentle-voiced_man",
    "hilmi": "English_Diligent_Man",
    # Generic roles used across A2-C1 dialogues.
    "coach": "English_Trustworth_Man",
    "driver": "English_Diligent_Man",
    "friend": "English_Gentle-voiced_man",
    "learner": "English_radiant_girl",
    "nurse": "English_CalmWoman",
    "receptionist": "English_radiant_girl",
}

FALLBACK_MINIMAX_VOICES = tuple(
    {
        "voice_id": voice_id,
        "voice_name": metadata["voice_name"],
        "category": "curated",
        "gender": metadata["gender"],
        "description": metadata["description"],
    }
    for voice_id, metadata in CURATED_MINIMAX_VOICE_METADATA.items()
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
    voice_id: str
    speaker_voices: dict[str, str]
    line_count: int


@dataclass(frozen=True)
class DialogueTurn:
    speaker: str
    text: str


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
                    "gender": infer_voice_gender(
                        voice_id=voice_id,
                        voice_name=str(voice.get("voice_name") or ""),
                        description=description_text,
                        raw_gender=voice.get("gender") or voice.get("voice_gender") or voice.get("sex"),
                    ),
                    "description": description_text,
                }
            )

    return voices


def filter_voice_options(voices: list[dict[str, Any]], *, language: str) -> list[dict[str, Any]]:
    del language
    by_id = {str(voice.get("voice_id") or ""): voice for voice in voices}
    return [
        curated_voice_option(voice_id, by_id.get(voice_id))
        for voice_id in CURATED_MINIMAX_VOICE_IDS
    ]


def curated_voice_option(voice_id: str, source: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    metadata = CURATED_MINIMAX_VOICE_METADATA[voice_id]
    source = source or {}
    return {
        "voice_id": voice_id,
        "voice_name": str(source.get("voice_name") or metadata["voice_name"]),
        "category": "curated",
        "gender": metadata["gender"],
        "description": str(source.get("description") or metadata["description"]),
    }


def readable_voice_name(voice_id: str) -> str:
    name = voice_id
    if "_" in name:
        name = name.split("_", 1)[1]
    return name.replace("_", " ").replace("-", " ").strip().title() or voice_id


def infer_voice_gender(
    *,
    voice_id: str,
    voice_name: str = "",
    description: str = "",
    raw_gender: Any = None,
) -> str:
    raw_value = str(raw_gender or "").strip().lower()
    if raw_value in {"male", "man", "masculine"}:
        return "male"
    if raw_value in {"female", "woman", "feminine"}:
        return "female"
    if raw_value in {"neutral", "nonbinary", "unknown"}:
        return "neutral" if raw_value == "neutral" else "unknown"

    searchable = re.sub(r"([a-z])([A-Z])", r"\1 \2", f"{voice_id} {voice_name} {description}").lower()
    tokens = {token for token in re.split(r"[^a-z]+", searchable) if token}
    female_tokens = {
        "female",
        "feminine",
        "woman",
        "women",
        "girl",
        "lady",
        "madam",
        "mother",
        "wife",
    }
    male_tokens = {
        "male",
        "masculine",
        "man",
        "men",
        "guy",
        "boy",
        "bloke",
        "gentleman",
        "father",
        "husband",
    }
    if tokens & female_tokens:
        return "female"
    if tokens & male_tokens:
        return "male"
    return "unknown"


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
    dialogue_turns = listening_script_to_dialogue_turns(lesson.listening_script_path)
    selected_model = normalized_model(model or settings.minimax_tts_model)
    selected_voice_id = (voice_id or settings.minimax_tts_voice_id).strip()
    if not selected_voice_id:
        raise AudioGenerationError("minimax_voice_id_missing")

    if len(dialogue_turns) >= 2:
        generated = await synthesize_dialogue_minimax_tts(
            turns=dialogue_turns,
            model=selected_model,
            fallback_voice_id=selected_voice_id,
            speed=speed,
            language_boost=settings.minimax_tts_language_boost,
        )
    else:
        tts_text = listening_script_to_tts_text(lesson.listening_script_path)
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
        voice_id=generated.voice_id,
        speaker_voices=generated.speaker_voices,
        line_count=generated.line_count,
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
        "voice_id": generated.voice_id,
        "speaker_voices": generated.speaker_voices,
        "line_count": generated.line_count,
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


async def generate_exam_item_listening_audio(
    *,
    item: ExamItemModel,
    exam_template: ExamTemplateModel,
    section: ExamSectionModel,
    model: Optional[str] = None,
    voice_id: Optional[str] = None,
    speed: float = 1.0,
    generated_by: str = "admin",
) -> dict[str, Any]:
    if not settings.minimax_api_key:
        raise AudioGenerationError("minimax_api_key_missing")
    if not s3_configured():
        raise AudioGenerationError("s3_config_missing")
    if section.code.upper() != "LISTENING":
        raise AudioGenerationError("exam_item_not_listening")

    source_text = (item.stimulus_text or item.prompt_text or "").strip()
    if len(source_text) < 8:
        raise AudioGenerationError("exam_item_audio_source_empty")
    if len(source_text) >= 10000:
        raise AudioGenerationError("exam_item_audio_source_too_long")

    selected_model = normalized_model(model or settings.minimax_tts_model)
    selected_voice_id = (voice_id or settings.minimax_tts_voice_id).strip()
    if not selected_voice_id:
        raise AudioGenerationError("minimax_voice_id_missing")

    dialogue_turns = dialogue_turns_from_text(source_text)
    if len(dialogue_turns) >= 2:
        generated = await synthesize_dialogue_minimax_tts(
            turns=dialogue_turns,
            model=selected_model,
            fallback_voice_id=selected_voice_id,
            speed=speed,
            language_boost=settings.minimax_tts_language_boost,
        )
    else:
        generated = await synthesize_minimax_tts(
            text=text_to_tts_text(source_text),
            model=selected_model,
            voice_id=selected_voice_id,
            speed=speed,
            language_boost=settings.minimax_tts_language_boost,
        )

    generated_at = datetime.now(timezone.utc)
    object_key = exam_audio_object_key(
        exam_template=exam_template,
        section=section,
        item=item,
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
        "item_id": item.id,
        "template_id": exam_template.id,
        "template_code": exam_template.code,
        "section_id": section.id,
        "section_code": section.code,
        "prompt_text": item.prompt_text,
        "audio_url": audio_url,
        "playback_url": playback_url,
        "object_key": object_key,
        "duration_seconds": generated.duration_seconds,
        "audio_format": generated.audio_format,
        "audio_size": generated.audio_size,
        "model": selected_model,
        "voice_id": generated.voice_id,
        "speaker_voices": generated.speaker_voices,
        "line_count": generated.line_count,
        "trace_id": generated.trace_id,
        "usage_characters": generated.usage_characters,
        "generated_by": generated_by,
        "generated_at": generated_at.isoformat(),
    }


async def synthesize_partner_reply_audio(
    *,
    text: str,
    voice_id: Optional[str] = None,
    speed: float = 1.0,
) -> Optional[str]:
    """Synthesize a short spoken reply and return it as a base64 data-URL.

    Returns None (instead of raising) when TTS is not configured or fails, so a
    conversation turn always succeeds with at least the text reply.
    """
    cleaned = (text or "").strip()
    if not cleaned or not settings.minimax_api_key:
        return None

    selected_voice = (voice_id or settings.minimax_tts_voice_id).strip()
    if not selected_voice:
        return None

    try:
        generated = await synthesize_minimax_tts(
            text=cleaned,
            model=default_minimax_tts_model(),
            voice_id=selected_voice,
            speed=speed,
            language_boost=settings.minimax_tts_language_boost,
            audio_format="mp3",
        )
    except AudioGenerationError as exc:
        logging.getLogger(__name__).error("partner_tts_failed voice=%s: %s", selected_voice, exc)
        return None

    encoded = base64.b64encode(generated.audio_bytes).decode("ascii")
    content_type = content_type_for_audio_format(generated.audio_format)
    return f"data:{content_type};base64,{encoded}"


async def synthesize_minimax_tts(
    *,
    text: str,
    model: str,
    voice_id: str,
    speed: float,
    language_boost: str,
    audio_format: str = "mp3",
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
            "format": audio_format,
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
        voice_id=voice_id,
        speaker_voices={},
        line_count=1,
    )


async def synthesize_dialogue_minimax_tts(
    *,
    turns: list[DialogueTurn],
    model: str,
    fallback_voice_id: str,
    speed: float,
    language_boost: str,
) -> MiniMaxAudioResult:
    speaker_voices = assign_dialogue_voices(turns, fallback_voice_id=fallback_voice_id)
    chunks: list[bytes] = []
    trace_ids: list[str] = []
    total_usage = 0

    for turn in turns:
        generated = await synthesize_minimax_tts(
            text=turn.text,
            model=model,
            voice_id=speaker_voices.get(turn.speaker) or fallback_voice_id,
            speed=speed,
            language_boost=language_boost,
            audio_format="wav",
        )
        chunks.append(generated.audio_bytes)
        if generated.trace_id:
            trace_ids.append(generated.trace_id)
        total_usage += generated.usage_characters

    audio_bytes, duration_seconds = concatenate_wav_audio(chunks)
    return MiniMaxAudioResult(
        audio_bytes=audio_bytes,
        duration_seconds=duration_seconds,
        audio_format="wav",
        audio_size=len(audio_bytes),
        trace_id=",".join(trace_ids),
        usage_characters=total_usage,
        voice_id="multi_speaker",
        speaker_voices=speaker_voices,
        line_count=len(turns),
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
    turns = listening_script_to_dialogue_turns(path)
    if turns:
        text = "\n".join(turn.text for turn in turns).strip()
        if len(text) < 8:
            raise AudioGenerationError("listening_script_empty")
        if len(text) >= 10000:
            raise AudioGenerationError("listening_script_too_long_for_sync_tts")
        return text

    raw_text = path.read_text(encoding="utf-8")
    dialogue_text = raw_text.split("## Audio Direction", 1)[0]
    lines = []
    for raw_line in dialogue_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        line = re.sub(r"^\*{0,2}([^:*]+):\*{0,2}\s*", "", line)
        line = line.replace("**", "").replace("*", "").replace("  ", " ").strip()
        if line:
            lines.append(line)

    text = "\n".join(lines).strip()
    if len(text) < 8:
        raise AudioGenerationError("listening_script_empty")
    if len(text) >= 10000:
        raise AudioGenerationError("listening_script_too_long_for_sync_tts")
    return text


def listening_script_to_dialogue_turns(path: Path) -> list[DialogueTurn]:
    raw_text = path.read_text(encoding="utf-8")
    dialogue_text = raw_text.split("## Audio Direction", 1)[0]
    turns: list[DialogueTurn] = []

    for raw_line in dialogue_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        match = re.match(r"^\*{0,2}([^:*]{1,80}):\*{0,2}\s*(.+)$", line)
        if not match:
            continue

        speaker = clean_speaker_name(match.group(1))
        text = clean_dialogue_text(match.group(2))
        if speaker and text:
            turns.append(DialogueTurn(speaker=speaker, text=text))

    total_text = "\n".join(turn.text for turn in turns).strip()
    if turns and len(total_text) >= 10000:
        raise AudioGenerationError("listening_script_too_long_for_sync_tts")
    return turns


def dialogue_turns_from_text(value: str) -> list[DialogueTurn]:
    raw_text = value.strip()
    turns: list[DialogueTurn] = []
    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = re.match(r"^\*{0,2}([^:*]{1,80}):\*{0,2}\s*(.+)$", line)
        if not match:
            continue
        speaker = clean_speaker_name(match.group(1))
        text = clean_dialogue_text(match.group(2))
        if speaker and text:
            turns.append(DialogueTurn(speaker=speaker, text=text))

    total_text = "\n".join(turn.text for turn in turns).strip()
    if turns and len(total_text) >= 10000:
        raise AudioGenerationError("exam_item_audio_source_too_long")
    return turns


def text_to_tts_text(value: str) -> str:
    text = value.strip()
    if len(text) < 8:
        raise AudioGenerationError("exam_item_audio_source_empty")
    if len(text) >= 10000:
        raise AudioGenerationError("exam_item_audio_source_too_long")
    return text


def clean_speaker_name(value: str) -> str:
    return value.replace("*", "").strip()


def clean_dialogue_text(value: str) -> str:
    return value.replace("**", "").replace("*", "").replace("  ", " ").strip()


def assign_dialogue_voices(turns: list[DialogueTurn], *, fallback_voice_id: str) -> dict[str, str]:
    speaker_by_key: dict[str, str] = {}
    for turn in turns:
        key = normalized_speaker_key(turn.speaker)
        if key and key not in speaker_by_key:
            speaker_by_key[key] = turn.speaker

    speaker_voices: dict[str, str] = {}
    used_voices: set[str] = set()

    for key in sorted(speaker_by_key):
        voice_id = DIALOGUE_PERSONA_VOICES.get(key)
        if not voice_id:
            continue
        speaker = speaker_by_key[key]
        speaker_voices[speaker] = voice_id
        used_voices.add(voice_id)

    for key in sorted(speaker_by_key):
        speaker = speaker_by_key[key]
        if speaker in speaker_voices:
            continue

        gender = infer_speaker_gender(speaker)
        if gender == "unknown":
            gender = stable_unknown_speaker_gender(key)

        voice_pool = CLEAR_FEMALE_DIALOGUE_VOICES if gender == "female" else CLEAR_MALE_DIALOGUE_VOICES
        voice_id = stable_voice_from_pool(key=key, voice_pool=voice_pool, used_voices=used_voices)
        speaker_voices[speaker] = voice_id or fallback_voice_id
        used_voices.add(speaker_voices[speaker])

    return speaker_voices


def infer_speaker_gender(speaker: str) -> str:
    normalized = normalized_speaker_key(speaker)
    female_names = {
        "alya",
        "sara",
        "mina",
        "anna",
        "emma",
        "lisa",
        "lina",
        "maria",
        "mary",
        "siti",
        "nina",
        "maya",
        "rani",
        "fatimah",
        "khadijah",
        "aisha",
    }
    male_names = {
        "ben",
        "john",
        "adi",
        "andi",
        "david",
        "dimas",
        "daniel",
        "james",
        "robert",
        "michael",
        "tom",
        "ali",
        "arif",
        "omar",
        "rama",
        "raka",
        "ahmad",
        "budi",
        "umar",
        "yusuf",
    }
    if normalized in female_names:
        return "female"
    if normalized in male_names:
        return "male"
    return "unknown"


def normalized_speaker_key(speaker: str) -> str:
    return re.sub(r"[^a-z]", "", speaker.lower())


def stable_unknown_speaker_gender(speaker_key: str) -> str:
    return "female" if stable_speaker_index(speaker_key, modulo=2) == 0 else "male"


def stable_voice_from_pool(
    *,
    key: str,
    voice_pool: tuple[str, ...],
    used_voices: set[str],
) -> str:
    if not voice_pool:
        return ""
    start_index = stable_speaker_index(key, modulo=len(voice_pool))
    for offset in range(len(voice_pool)):
        voice_id = voice_pool[(start_index + offset) % len(voice_pool)]
        if voice_id not in used_voices:
            return voice_id
    return voice_pool[start_index]


def stable_speaker_index(speaker_key: str, *, modulo: int) -> int:
    if modulo <= 0:
        return 0
    digest = hashlib.sha256(speaker_key.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % modulo


def concatenate_wav_audio(chunks: list[bytes], *, pause_seconds: float = 0.25) -> tuple[bytes, float]:
    if not chunks:
        raise AudioGenerationError("dialogue_audio_empty")

    wav_params = None
    frames: list[bytes] = []
    total_frames = 0

    for chunk in chunks:
        with wave.open(io.BytesIO(chunk), "rb") as reader:
            current_params = reader.getparams()
            comparable_params = (
                current_params.nchannels,
                current_params.sampwidth,
                current_params.framerate,
                current_params.comptype,
                current_params.compname,
            )
            if wav_params is None:
                wav_params = comparable_params
            elif comparable_params != wav_params:
                raise AudioGenerationError("dialogue_audio_wav_params_mismatch")

            frame_bytes = normalize_wav_frame_volume(reader.readframes(current_params.nframes), current_params.sampwidth)
            frames.append(frame_bytes)
            total_frames += current_params.nframes

    if wav_params is None:
        raise AudioGenerationError("dialogue_audio_empty")

    nchannels, sampwidth, framerate, comptype, compname = wav_params
    pause_frames = max(0, int(framerate * pause_seconds))
    pause_bytes = b"\x00" * pause_frames * nchannels * sampwidth
    output = io.BytesIO()

    with wave.open(output, "wb") as writer:
        writer.setnchannels(nchannels)
        writer.setsampwidth(sampwidth)
        writer.setframerate(framerate)
        writer.setcomptype(comptype, compname)
        for index, frame_bytes in enumerate(frames):
            writer.writeframes(frame_bytes)
            if index < len(frames) - 1 and pause_bytes:
                writer.writeframes(pause_bytes)
                total_frames += pause_frames

    duration_seconds = round(total_frames / framerate, 2)
    return output.getvalue(), max(duration_seconds, 0.01)


def normalize_wav_frame_volume(frame_bytes: bytes, sampwidth: int) -> bytes:
    if sampwidth != 2 or not frame_bytes:
        return frame_bytes

    samples = array("h")
    samples.frombytes(frame_bytes)
    if sys.byteorder != "little":
        samples.byteswap()

    peak = max((abs(sample) for sample in samples), default=0)
    if peak <= 0:
        return frame_bytes

    max_peak = (1 << (sampwidth * 8 - 1)) - 1
    target_peak = max(1, int(max_peak * DIALOGUE_TARGET_PEAK_RATIO))
    gain = target_peak / peak
    normalized = array(
        "h",
        (
            max(-max_peak - 1, min(max_peak, int(sample * gain)))
            for sample in samples
        ),
    )
    if sys.byteorder != "little":
        normalized.byteswap()
    return normalized.tobytes()


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
    speaker_voices: dict[str, str],
    line_count: int,
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
        "speaker_voices": speaker_voices,
        "line_count": line_count,
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


def exam_audio_object_key(
    *,
    exam_template: ExamTemplateModel,
    section: ExamSectionModel,
    item: ExamItemModel,
    voice_id: str,
    generated_at: datetime,
    extension: str,
) -> str:
    safe_voice_id = re.sub(r"[^A-Za-z0-9_.-]+", "-", voice_id).strip("-")
    safe_template_code = re.sub(r"[^A-Za-z0-9_.-]+", "-", exam_template.code).strip("-")
    safe_section_code = re.sub(r"[^A-Za-z0-9_.-]+", "-", section.code).strip("-")
    timestamp = generated_at.strftime("%Y%m%dT%H%M%SZ")
    extension = re.sub(r"[^a-z0-9]+", "", extension.lower()) or "mp3"
    return (
        "conversease/exams/audio/"
        f"{exam_template.level_code}/{safe_template_code}/{safe_section_code}/"
        f"item-{item.sequence_order:03d}-{safe_voice_id}-{timestamp}.{extension}"
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
