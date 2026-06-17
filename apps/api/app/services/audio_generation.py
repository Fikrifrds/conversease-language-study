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

ELEVENLABS_TTS_MODELS = (
    "eleven_v3",
    "eleven_multilingual_v2",
    "eleven_turbo_v2_5",
    "eleven_flash_v2_5",
)

TTS_PROVIDER_MINIMAX = "minimax"
TTS_PROVIDER_ELEVENLABS = "elevenlabs"
TTS_PROVIDERS = (TTS_PROVIDER_MINIMAX, TTS_PROVIDER_ELEVENLABS)

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

CLEAR_ARABIC_FEMALE_DIALOGUE_VOICES = (
    "Arabic_CalmWoman",
)

CLEAR_ARABIC_MALE_DIALOGUE_VOICES = (
    "Arabic_FriendlyGuy",
)

ELEVENLABS_ARABIC_DEFAULT_MALE_VOICE_ID = "3nav5pHC1EYvWOd5LmnA"
ELEVENLABS_ARABIC_DEFAULT_FEMALE_VOICE_ID = "gVzwmdZzRgBrNjXaTmi5"
ELEVENLABS_ARABIC_MALE_DIALOGUE_VOICES = (
    "3nav5pHC1EYvWOd5LmnA",  # Saud
    "RjFuvnufLX42TYe37ekK",  # Adeeb
    "yXEnnEln9armDCyhkXcA",  # Jeddawi
    "t9akNmCDhz230CEXOYmn",  # Abdullah Saadoun
    "cFUFIbKkO2iZFwS8cRnY",  # Nasser AlJubaily
    "3GnbqfjaW8xI6hRTVx4Y",  # Nasser
    "OoE8swS3hImZANNOodf6",  # Ali Ahmed
    "kr4VZw8MSZMHE0y2m40n",  # Hasawi
)
ELEVENLABS_ARABIC_FEMALE_DIALOGUE_VOICES = (
    "gVzwmdZzRgBrNjXaTmi5",  # Layan
    "v7UCHHCrHj1KBa4E41gb",  # Heba Mansuri
    "kdUY91gH5xyDHapxlthT",  # Hana
)
ELEVENLABS_ARABIC_VOICE_METADATA = {
    "yXEnnEln9armDCyhkXcA": {
        "voice_name": "Jeddawi",
        "gender": "male",
        "description": "Calm, confident, and deep Saudi Arabic male voice.",
    },
    "t9akNmCDhz230CEXOYmn": {
        "voice_name": "Abdullah Saadoun",
        "gender": "male",
        "description": "Curated Arabic male voice.",
    },
    "3nav5pHC1EYvWOd5LmnA": {
        "voice_name": "Saud",
        "gender": "male",
        "description": "Deep, formal, and clear Arabic male voice.",
    },
    "RjFuvnufLX42TYe37ekK": {
        "voice_name": "Adeeb",
        "gender": "male",
        "description": "Clear, confident, and natural Arabic male voice.",
    },
    "cFUFIbKkO2iZFwS8cRnY": {
        "voice_name": "Nasser AlJubaily",
        "gender": "male",
        "description": "Authentic Saudi professional Arabic male voice.",
    },
    "OoE8swS3hImZANNOodf6": {
        "voice_name": "Ali Ahmed",
        "gender": "male",
        "description": "Authentic Saudi Arabic male voice.",
    },
    "kr4VZw8MSZMHE0y2m40n": {
        "voice_name": "Hasawi",
        "gender": "male",
        "description": "Conversational and energetic Arabic male voice.",
    },
    "3GnbqfjaW8xI6hRTVx4Y": {
        "voice_name": "Nasser",
        "gender": "male",
        "description": "Enterprise, professional, and clear Arabic male voice.",
    },
    "v7UCHHCrHj1KBa4E41gb": {
        "voice_name": "Heba Mansuri",
        "gender": "female",
        "description": "Gentle and calm Arabic female voice.",
    },
    "kdUY91gH5xyDHapxlthT": {
        "voice_name": "Hana",
        "gender": "female",
        "description": "Casual and relatable Arabic female voice.",
    },
    "gVzwmdZzRgBrNjXaTmi5": {
        "voice_name": "Layan",
        "gender": "female",
        "description": "Professional Arabic female voice.",
    },
}
ELEVENLABS_ARABIC_CURATED_VOICE_IDS = (
    *ELEVENLABS_ARABIC_MALE_DIALOGUE_VOICES,
    *ELEVENLABS_ARABIC_FEMALE_DIALOGUE_VOICES,
)

ARABIC_LANGUAGE_KEYS = {"arabic", "ar", "ar-sa", "ar-ae", "ar-eg"}
ENGLISH_LANGUAGE_KEYS = {"english", "en", "en-us", "en-gb"}
ARABIC_DEFAULT_VOICE_ID = "Arabic_FriendlyGuy"
ENGLISH_DEFAULT_VOICE_ID = "English_expressive_narrator"
ARABIC_TTS_LANGUAGE_BOOST = "Arabic"
ENGLISH_TTS_LANGUAGE_BOOST = "English"
ARABIC_DEFAULT_SPEED = 0.9
ARABIC_VOICE_PREVIEW_SAMPLE_TEXT = "مرحبًا. اسمي أحمد. أنا أتعلم العربية الفصحى بوضوح وهدوء."
ELEVENLABS_DIALOGUE_SAMPLE_RATE = 24000
ELEVENLABS_DIALOGUE_PAUSE_SECONDS = 0.38
TRAILING_AUDIO_PAUSE_TAG_RE = re.compile(r"\s*<#(\d+(?:\.\d+)?)#>\s*$")
AUDIO_PAUSE_TAG_RE = re.compile(r"<#\d+(?:\.\d+)?#>")
MAX_AUDIO_PAUSE_SECONDS = 3.0

DIALOGUE_TARGET_PEAK_RATIO = 0.82
ENGLISH_CURATED_MINIMAX_VOICE_IDS = (
    "English_expressive_narrator",
    *CLEAR_MALE_DIALOGUE_VOICES,
    *CLEAR_FEMALE_DIALOGUE_VOICES,
)

ARABIC_CURATED_MINIMAX_VOICE_IDS = (
    *CLEAR_ARABIC_MALE_DIALOGUE_VOICES,
    *CLEAR_ARABIC_FEMALE_DIALOGUE_VOICES,
)

CURATED_MINIMAX_VOICE_IDS = (
    *ENGLISH_CURATED_MINIMAX_VOICE_IDS,
    *ARABIC_CURATED_MINIMAX_VOICE_IDS,
)

CURATED_MINIMAX_VOICE_METADATA = {
    "English_expressive_narrator": {
        "voice_name": "Expressive Narrator",
        "gender": "neutral",
        "language": "English",
        "description": "Clear narrator voice for single-speaker lesson audio.",
    },
    "English_Gentle-voiced_man": {
        "voice_name": "Gentle-voiced Man",
        "gender": "male",
        "language": "English",
        "description": "Solid male voice for calm beginner dialogue.",
    },
    "English_Trustworth_Man": {
        "voice_name": "Trustworthy Man",
        "gender": "male",
        "language": "English",
        "description": "Solid male voice for steady instructional dialogue.",
    },
    "English_Diligent_Man": {
        "voice_name": "Diligent Man",
        "gender": "male",
        "language": "English",
        "description": "Solid male voice for clear learner or staff dialogue.",
    },
    "English_radiant_girl": {
        "voice_name": "Radiant Girl",
        "gender": "female",
        "language": "English",
        "description": "Solid female voice for friendly beginner dialogue.",
    },
    "English_CalmWoman": {
        "voice_name": "Calm Woman",
        "gender": "female",
        "language": "English",
        "description": "Solid female voice for teacher, helper, and examiner dialogue.",
    },
    "English_Upbeat_Woman": {
        "voice_name": "Upbeat Woman",
        "gender": "female",
        "language": "English",
        "description": "Solid female voice for light social dialogue.",
    },
    "Arabic_FriendlyGuy": {
        "voice_name": "Friendly Guy",
        "gender": "male",
        "language": "Arabic",
        "description": "Clear Arabic male voice for teacher, narrator, and student dialogue.",
    },
    "Arabic_CalmWoman": {
        "voice_name": "Calm Woman",
        "gender": "female",
        "language": "Arabic",
        "description": "Calm Arabic female voice for teacher, narrator, and student dialogue.",
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
    "male": "English_Trustworth_Man",
    "man": "English_Trustworth_Man",
    "maya": "English_radiant_girl",
    "mina": "English_Upbeat_Woman",
    "nina": "English_Upbeat_Woman",
    "officer": "English_CalmWoman",
    "omar": "English_Trustworth_Man",
    "raka": "English_Gentle-voiced_man",
    "sara": "English_CalmWoman",
    "staff": "English_CalmWoman",
    "female": "English_CalmWoman",
    "woman": "English_CalmWoman",
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
    # Arabic personas. MiniMax currently exposes two Arabic system
    # voices, so repeated male/female roles share these voices in beta.
    "ahmad": "Arabic_FriendlyGuy",
    "ahmed": "Arabic_FriendlyGuy",
    "ali": "Arabic_FriendlyGuy",
    "fatimah": "Arabic_CalmWoman",
    "fatima": "Arabic_CalmWoman",
    "maryam": "Arabic_CalmWoman",
    "muallim": "Arabic_FriendlyGuy",
    "muallimah": "Arabic_CalmWoman",
    "studentmale": "Arabic_FriendlyGuy",
    "studentfemale": "Arabic_CalmWoman",
    "teacherarabicmale": "Arabic_FriendlyGuy",
    "teacherarabicfemale": "Arabic_CalmWoman",
    "arabicteacher": "Arabic_FriendlyGuy",
    "arabicstudent": "Arabic_CalmWoman",
    "ustadh": "Arabic_FriendlyGuy",
    "ustadz": "Arabic_FriendlyGuy",
    "ustaz": "Arabic_FriendlyGuy",
    "teacherarabic": "Arabic_FriendlyGuy",
    "studentarabicmale": "Arabic_FriendlyGuy",
    "studentarabicfemale": "Arabic_CalmWoman",
    "talib": "Arabic_FriendlyGuy",
    "talibah": "Arabic_CalmWoman",
    "khalid": "Arabic_FriendlyGuy",
    "zayd": "Arabic_FriendlyGuy",
    "ziyad": "Arabic_FriendlyGuy",
    "aisha": "Arabic_CalmWoman",
    "khadijah": "Arabic_CalmWoman",
    "noura": "Arabic_CalmWoman",
    "nura": "Arabic_CalmWoman",
    "layla": "Arabic_CalmWoman",
}

ARABIC_MINIMAX_DIALOGUE_PERSONA_VOICES = {
    "barista": "Arabic_CalmWoman",
    "cafestaff": "Arabic_CalmWoman",
    "seller": "Arabic_FriendlyGuy",
    "shopkeeper": "Arabic_FriendlyGuy",
    "staff": "Arabic_CalmWoman",
}

ELEVENLABS_ARABIC_PERSONA_VOICES = {
    "ahmad": "RjFuvnufLX42TYe37ekK",
    "ahmed": "RjFuvnufLX42TYe37ekK",
    "ali": "OoE8swS3hImZANNOodf6",
    "arabicstudent": "kdUY91gH5xyDHapxlthT",
    "arabicteacher": "3nav5pHC1EYvWOd5LmnA",
    "aisha": "v7UCHHCrHj1KBa4E41gb",
    "barista": "gVzwmdZzRgBrNjXaTmi5",
    "cafestaff": "gVzwmdZzRgBrNjXaTmi5",
    "fatima": "v7UCHHCrHj1KBa4E41gb",
    "fatimah": "v7UCHHCrHj1KBa4E41gb",
    "khalid": "t9akNmCDhz230CEXOYmn",
    "khadijah": "gVzwmdZzRgBrNjXaTmi5",
    "layla": "kdUY91gH5xyDHapxlthT",
    "maryam": "gVzwmdZzRgBrNjXaTmi5",
    "muallim": "3nav5pHC1EYvWOd5LmnA",
    "muallimah": "gVzwmdZzRgBrNjXaTmi5",
    "narrator": "3GnbqfjaW8xI6hRTVx4Y",
    "noura": "kdUY91gH5xyDHapxlthT",
    "nura": "kdUY91gH5xyDHapxlthT",
    "seller": "3GnbqfjaW8xI6hRTVx4Y",
    "shopkeeper": "3GnbqfjaW8xI6hRTVx4Y",
    "staff": "gVzwmdZzRgBrNjXaTmi5",
    "studentarabicfemale": "kdUY91gH5xyDHapxlthT",
    "studentarabicmale": "kr4VZw8MSZMHE0y2m40n",
    "studentfemale": "kdUY91gH5xyDHapxlthT",
    "studentmale": "kr4VZw8MSZMHE0y2m40n",
    "talib": "kr4VZw8MSZMHE0y2m40n",
    "talibah": "kdUY91gH5xyDHapxlthT",
    "teacherarabic": "3nav5pHC1EYvWOd5LmnA",
    "teacherarabicfemale": "gVzwmdZzRgBrNjXaTmi5",
    "teacherarabicmale": "3nav5pHC1EYvWOd5LmnA",
    "ustadh": "yXEnnEln9armDCyhkXcA",
    "ustadz": "yXEnnEln9armDCyhkXcA",
    "ustaz": "yXEnnEln9armDCyhkXcA",
    "zayd": "cFUFIbKkO2iZFwS8cRnY",
    "ziyad": "3GnbqfjaW8xI6hRTVx4Y",
}

FALLBACK_MINIMAX_VOICES = tuple(
    {
        "voice_id": voice_id,
        "voice_name": metadata["voice_name"],
        "category": "curated",
        "gender": metadata["gender"],
        "language": metadata["language"],
        "provider": TTS_PROVIDER_MINIMAX,
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
    pause_after_seconds: float = 0.0


def audio_generation_settings_payload(voices: list[dict[str, Any]]) -> dict[str, Any]:
    default_provider = TTS_PROVIDER_MINIMAX
    return {
        "default_provider": default_provider,
        "minimax_configured": bool(settings.minimax_api_key),
        "elevenlabs_configured": bool(settings.elevenlabs_api_key),
        "s3_configured": s3_configured(),
        "default_model": default_minimax_tts_model(),
        "default_voice_id": settings.minimax_tts_voice_id,
        "default_language_boost": settings.minimax_tts_language_boost,
        "models": list(MINIMAX_TTS_MODELS),
        "providers": [
            {
                "key": TTS_PROVIDER_MINIMAX,
                "label": "MiniMax",
                "configured": bool(settings.minimax_api_key),
                "default_model": default_minimax_tts_model(),
                "default_voice_id": settings.minimax_tts_voice_id,
                "models": list(MINIMAX_TTS_MODELS),
            },
            {
                "key": TTS_PROVIDER_ELEVENLABS,
                "label": "ElevenLabs",
                "configured": bool(settings.elevenlabs_api_key),
                "default_model": default_elevenlabs_tts_model(),
                "default_voice_id": default_elevenlabs_voice_id_for_language("arabic"),
                "models": list(ELEVENLABS_TTS_MODELS),
            },
        ],
        "voices": voices,
    }


async def audio_generation_settings() -> dict[str, Any]:
    minimax_voices = await list_minimax_voices(language="all")
    elevenlabs_voices = await list_elevenlabs_voices()
    voices = [*minimax_voices, *elevenlabs_voices]
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
                    "language": inferred_voice_language(voice_id),
                    "provider": TTS_PROVIDER_MINIMAX,
                    "description": description_text,
                }
            )

    return voices


def filter_voice_options(voices: list[dict[str, Any]], *, language: str) -> list[dict[str, Any]]:
    by_id = {str(voice.get("voice_id") or ""): voice for voice in voices}
    voice_ids = curated_voice_ids_for_language(language)
    return [
        curated_voice_option(voice_id, by_id.get(voice_id))
        for voice_id in voice_ids
    ]


def curated_voice_ids_for_language(language: str) -> tuple[str, ...]:
    normalized = normalized_language_key(language)
    if normalized in {"all", "any", "*"}:
        return CURATED_MINIMAX_VOICE_IDS
    if normalized in ARABIC_LANGUAGE_KEYS:
        return ARABIC_CURATED_MINIMAX_VOICE_IDS
    return ENGLISH_CURATED_MINIMAX_VOICE_IDS


def curated_voice_option(voice_id: str, source: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    metadata = CURATED_MINIMAX_VOICE_METADATA[voice_id]
    source = source or {}
    return {
        "voice_id": voice_id,
        "voice_name": str(source.get("voice_name") or metadata["voice_name"]),
        "category": "curated",
        "gender": metadata["gender"],
        "language": metadata["language"],
        "provider": TTS_PROVIDER_MINIMAX,
        "description": str(source.get("description") or metadata["description"]),
    }


async def list_elevenlabs_voices(limit: int = 100) -> list[dict[str, Any]]:
    if not settings.elevenlabs_api_key:
        return fallback_elevenlabs_voices()

    try:
        response = await elevenlabs_client_get(
            "/v1/voices",
            timeout=min(settings.elevenlabs_tts_timeout_seconds, 30),
        )
    except AudioGenerationError:
        return fallback_elevenlabs_voices()

    voices = flatten_elevenlabs_voices(response)
    filtered = filter_elevenlabs_voice_options(voices)
    return filtered[:limit] or fallback_elevenlabs_voices()


def fallback_elevenlabs_voices() -> list[dict[str, Any]]:
    return [elevenlabs_curated_voice_option(voice_id) for voice_id in ELEVENLABS_ARABIC_CURATED_VOICE_IDS]


def flatten_elevenlabs_voices(payload: dict[str, Any]) -> list[dict[str, Any]]:
    voices: list[dict[str, Any]] = []
    for voice in payload.get("voices", []) or []:
        if not isinstance(voice, dict) or not voice.get("voice_id"):
            continue
        labels = voice.get("labels") if isinstance(voice.get("labels"), dict) else {}
        label_text = " ".join(str(value) for value in labels.values() if value)
        description = str(voice.get("description") or label_text or "")
        voice_id = str(voice["voice_id"])
        voices.append(
            {
                "voice_id": voice_id,
                "voice_name": str(voice.get("name") or readable_voice_name(voice_id)),
                "category": str(voice.get("category") or "elevenlabs"),
                "gender": infer_voice_gender(
                    voice_id=voice_id,
                    voice_name=str(voice.get("name") or ""),
                    description=f"{description} {label_text}",
                    raw_gender=labels.get("gender") or labels.get("sex"),
                ),
                "language": "Arabic",
                "provider": TTS_PROVIDER_ELEVENLABS,
                "description": description or "ElevenLabs multilingual voice.",
            }
        )
    return voices


def filter_elevenlabs_voice_options(voices: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {str(voice.get("voice_id") or ""): voice for voice in voices}
    return [
        elevenlabs_curated_voice_option(voice_id, by_id.get(voice_id))
        for voice_id in ELEVENLABS_ARABIC_CURATED_VOICE_IDS
    ]


def elevenlabs_curated_voice_option(voice_id: str, source: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    metadata = ELEVENLABS_ARABIC_VOICE_METADATA[voice_id]
    source = source or {}
    return {
        "voice_id": voice_id,
        "voice_name": str(source.get("voice_name") or metadata["voice_name"]),
        "category": "curated",
        "gender": str(source.get("gender") or metadata["gender"]),
        "language": "Arabic",
        "provider": TTS_PROVIDER_ELEVENLABS,
        "description": str(source.get("description") or metadata["description"]),
    }


def inferred_voice_language(voice_id: str) -> str:
    if is_arabic_voice_id(voice_id):
        return "Arabic"
    if is_english_voice_id(voice_id):
        return "English"
    return ""


def readable_voice_name(voice_id: str) -> str:
    name = voice_id
    if "_" in name:
        name = name.split("_", 1)[1]
    return name.replace("_", " ").replace("-", " ").strip().title() or voice_id


def normalized_language_key(language: str) -> str:
    return (language or "").strip().lower().replace("_", "-")


def is_arabic_language(language: str) -> bool:
    return normalized_language_key(language) in ARABIC_LANGUAGE_KEYS


def is_english_language(language: str) -> bool:
    return normalized_language_key(language) in ENGLISH_LANGUAGE_KEYS


def is_arabic_voice_id(voice_id: str) -> bool:
    value = (voice_id or "").strip()
    return value in ELEVENLABS_ARABIC_VOICE_METADATA or value.lower().startswith("arabic_")


def is_english_voice_id(voice_id: str) -> bool:
    return (voice_id or "").strip().lower().startswith("english_")


def normalized_tts_provider(value: Optional[str], *, language: str = "") -> str:
    provider = (value or "").strip().lower()
    if provider in TTS_PROVIDERS:
        return provider
    return default_tts_provider_for_language(language)


def ensure_tts_provider_configured(provider: str) -> None:
    if provider == TTS_PROVIDER_ELEVENLABS:
        if not settings.elevenlabs_api_key:
            raise AudioGenerationError("elevenlabs_api_key_missing")
        return
    if not settings.minimax_api_key:
        raise AudioGenerationError("minimax_api_key_missing")


def default_tts_provider_for_language(language: str) -> str:
    if is_arabic_language(language):
        return TTS_PROVIDER_ELEVENLABS
    return TTS_PROVIDER_MINIMAX


def models_for_provider(provider: str) -> tuple[str, ...]:
    if provider == TTS_PROVIDER_ELEVENLABS:
        return ELEVENLABS_TTS_MODELS
    return MINIMAX_TTS_MODELS


def tts_provider_for_model(model: str) -> str:
    value = (model or "").strip()
    if value in ELEVENLABS_TTS_MODELS:
        return TTS_PROVIDER_ELEVENLABS
    return TTS_PROVIDER_MINIMAX


def normalized_model_for_provider(provider: str, value: Optional[str]) -> str:
    model = (value or "").strip()
    models = models_for_provider(provider)
    if model and model in models:
        return model
    if provider == TTS_PROVIDER_ELEVENLABS:
        return default_elevenlabs_tts_model()
    return default_minimax_tts_model()


def default_voice_id_for_language(language: str) -> str:
    if is_arabic_language(language):
        return ARABIC_DEFAULT_VOICE_ID
    return settings.minimax_tts_voice_id.strip() or ENGLISH_DEFAULT_VOICE_ID


def voice_id_for_language(language: str, requested_voice_id: Optional[str]) -> str:
    selected_voice = (requested_voice_id or settings.minimax_tts_voice_id).strip()
    if is_arabic_language(language):
        return selected_voice if is_arabic_voice_id(selected_voice) else ARABIC_DEFAULT_VOICE_ID
    if is_english_language(language) and is_arabic_voice_id(selected_voice):
        return ENGLISH_DEFAULT_VOICE_ID
    return selected_voice or default_voice_id_for_language(language)


def default_elevenlabs_voice_id_for_language(language: str) -> str:
    if is_arabic_language(language):
        return (
            curated_elevenlabs_arabic_voice_id(settings.elevenlabs_arabic_male_voice_id, gender="male")
            or curated_elevenlabs_arabic_voice_id(settings.elevenlabs_tts_voice_id, gender="male")
            or ELEVENLABS_ARABIC_DEFAULT_MALE_VOICE_ID
        )
    return settings.elevenlabs_tts_voice_id.strip() or ELEVENLABS_ARABIC_DEFAULT_MALE_VOICE_ID


def elevenlabs_voice_id_for_language(language: str, requested_voice_id: Optional[str]) -> str:
    selected_voice = (requested_voice_id or "").strip()
    if is_arabic_language(language):
        return curated_elevenlabs_arabic_voice_id(selected_voice) or default_elevenlabs_voice_id_for_language(language)
    return selected_voice or default_elevenlabs_voice_id_for_language(language)


def voice_id_for_provider(provider: str, language: str, requested_voice_id: Optional[str]) -> str:
    if provider == TTS_PROVIDER_ELEVENLABS:
        return elevenlabs_voice_id_for_language(language, requested_voice_id)
    return voice_id_for_language(language, requested_voice_id)


def language_boost_for_language(language: str) -> str:
    if is_arabic_language(language):
        return ARABIC_TTS_LANGUAGE_BOOST
    if is_english_language(language):
        return ENGLISH_TTS_LANGUAGE_BOOST
    return settings.minimax_tts_language_boost or "auto"


def language_boost_for_voice(voice_id: str) -> str:
    if is_arabic_voice_id(voice_id):
        return ARABIC_TTS_LANGUAGE_BOOST
    if is_english_voice_id(voice_id):
        return ENGLISH_TTS_LANGUAGE_BOOST
    return settings.minimax_tts_language_boost or "auto"


def default_voice_preview_text(voice_id: str) -> str:
    if is_arabic_voice_id(voice_id) or voice_id in ELEVENLABS_ARABIC_VOICE_METADATA:
        return ARABIC_VOICE_PREVIEW_SAMPLE_TEXT
    return "Hello, welcome to Conversease. Listen, repeat, and speak with clear confidence."


def curated_elevenlabs_arabic_voice_id(value: Optional[str], *, gender: str = "") -> str:
    voice_id = (value or "").strip()
    if voice_id not in ELEVENLABS_ARABIC_VOICE_METADATA:
        return ""
    expected_gender = gender.strip().lower()
    if expected_gender and elevenlabs_voice_gender(voice_id) != expected_gender:
        return ""
    return voice_id


def speed_for_language(language: str, speed: float) -> float:
    if is_arabic_language(language) and abs(float(speed) - 1.0) < 0.001:
        return ARABIC_DEFAULT_SPEED
    return speed


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
    provider: Optional[str] = None,
    model: Optional[str] = None,
    voice_id: Optional[str] = None,
    speed: float = 1.0,
    generated_by: str = "admin",
) -> dict[str, Any]:
    if not s3_configured():
        raise AudioGenerationError("s3_config_missing")

    lesson = find_lesson_audio_reference(lesson_slug)
    selected_provider = normalized_tts_provider(provider, language=lesson.language)
    ensure_tts_provider_configured(selected_provider)
    dialogue_turns = listening_script_to_dialogue_turns(lesson.listening_script_path)
    selected_model = normalized_model_for_provider(selected_provider, model)
    selected_voice_id = voice_id_for_provider(selected_provider, lesson.language, voice_id)
    if not selected_voice_id:
        raise AudioGenerationError(f"{selected_provider}_voice_id_missing")
    selected_speed = speed_for_language(lesson.language, speed)

    if selected_provider == TTS_PROVIDER_ELEVENLABS and len(dialogue_turns) >= 2:
        generated = await synthesize_dialogue_elevenlabs_tts(
            turns=dialogue_turns,
            model=selected_model,
            fallback_voice_id=selected_voice_id,
            speed=selected_speed,
            language=lesson.language,
        )
    elif selected_provider == TTS_PROVIDER_ELEVENLABS:
        tts_text = listening_script_to_tts_text(lesson.listening_script_path)
        generated = await synthesize_elevenlabs_tts(
            text=tts_text,
            model=selected_model,
            voice_id=selected_voice_id,
            speed=selected_speed,
        )
    elif len(dialogue_turns) >= 2:
        selected_language_boost = language_boost_for_language(lesson.language)
        generated = await synthesize_dialogue_minimax_tts(
            turns=dialogue_turns,
            model=selected_model,
            fallback_voice_id=selected_voice_id,
            speed=selected_speed,
            language_boost=selected_language_boost,
            language=lesson.language,
        )
    else:
        selected_language_boost = language_boost_for_language(lesson.language)
        tts_text = listening_script_to_tts_text(lesson.listening_script_path)
        generated = await synthesize_minimax_tts(
            text=tts_text,
            model=selected_model,
            voice_id=selected_voice_id,
            speed=selected_speed,
            language_boost=selected_language_boost,
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
        provider=selected_provider,
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
        "provider": selected_provider,
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
    provider: Optional[str] = None,
    model: Optional[str] = None,
    voice_id: Optional[str] = None,
    speed: float = 1.0,
    generated_by: str = "admin",
    sample_text: Optional[str] = None,
) -> dict[str, Any]:
    if not s3_configured():
        raise AudioGenerationError("s3_config_missing")

    selected_provider = normalized_tts_provider(provider)
    ensure_tts_provider_configured(selected_provider)
    selected_model = normalized_model_for_provider(selected_provider, model)
    selected_voice_id = voice_id_for_provider(selected_provider, "", voice_id)
    if not selected_voice_id:
        raise AudioGenerationError(f"{selected_provider}_voice_id_missing")

    preview_text = (
        sample_text
        or default_voice_preview_text(selected_voice_id)
    ).strip()
    if len(preview_text) < 8:
        raise AudioGenerationError("voice_preview_text_empty")
    if len(preview_text) > 500:
        raise AudioGenerationError("voice_preview_text_too_long")

    if selected_provider == TTS_PROVIDER_ELEVENLABS:
        generated = await synthesize_elevenlabs_tts(
            text=preview_text,
            model=selected_model,
            voice_id=selected_voice_id,
            speed=speed,
        )
    else:
        generated = await synthesize_minimax_tts(
            text=preview_text,
            model=selected_model,
            voice_id=selected_voice_id,
            speed=speed,
            language_boost=language_boost_for_voice(selected_voice_id),
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
        "provider": selected_provider,
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
    provider: Optional[str] = None,
    model: Optional[str] = None,
    voice_id: Optional[str] = None,
    speed: float = 1.0,
    generated_by: str = "admin",
) -> dict[str, Any]:
    if not s3_configured():
        raise AudioGenerationError("s3_config_missing")
    if section.code.upper() not in EXAM_AUDIO_SECTION_CODES:
        raise AudioGenerationError("exam_item_section_not_supported")

    source_text = exam_item_audio_source_text(item)
    if len(source_text) < 8:
        raise AudioGenerationError("exam_item_audio_source_empty")
    if len(source_text) >= 10000:
        raise AudioGenerationError("exam_item_audio_source_too_long")

    selected_provider = normalized_tts_provider(provider)
    ensure_tts_provider_configured(selected_provider)
    selected_model = normalized_model_for_provider(selected_provider, model)
    selected_voice_id = voice_id_for_provider(selected_provider, "", voice_id)
    if not selected_voice_id:
        raise AudioGenerationError(f"{selected_provider}_voice_id_missing")

    dialogue_turns = dialogue_turns_from_text(source_text)
    if selected_provider == TTS_PROVIDER_ELEVENLABS and len(dialogue_turns) >= 2:
        generated = await synthesize_dialogue_elevenlabs_tts(
            turns=dialogue_turns,
            model=selected_model,
            fallback_voice_id=selected_voice_id,
            speed=speed,
        )
    elif selected_provider == TTS_PROVIDER_ELEVENLABS:
        generated = await synthesize_elevenlabs_tts(
            text=text_to_tts_text(source_text),
            model=selected_model,
            voice_id=selected_voice_id,
            speed=speed,
        )
    elif len(dialogue_turns) >= 2:
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
        "provider": selected_provider,
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
    language: str = "",
) -> MiniMaxAudioResult:
    speaker_voices = assign_dialogue_voices(turns, fallback_voice_id=fallback_voice_id, language=language)
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

    audio_bytes, duration_seconds = concatenate_wav_audio(
        chunks,
        pause_after_seconds=[turn.pause_after_seconds for turn in turns],
    )
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


async def synthesize_elevenlabs_tts(
    *,
    text: str,
    model: str,
    voice_id: str,
    speed: float,
    audio_format: str = "mp3",
) -> MiniMaxAudioResult:
    payload = {
        "text": text,
        "model_id": model,
        "voice_settings": {
            "stability": 0.62,
            "similarity_boost": 0.82,
            "style": 0.08,
            "use_speaker_boost": True,
            "speed": speed,
        },
    }
    output_format = elevenlabs_output_format(audio_format)
    audio_bytes, response_trace_id, response_content_type = await elevenlabs_client_post_audio(
        f"/v1/text-to-speech/{voice_id}",
        payload,
        timeout=settings.elevenlabs_tts_timeout_seconds,
        output_format=output_format,
    )
    resolved_format = elevenlabs_audio_format(output_format, response_content_type, audio_format)
    return MiniMaxAudioResult(
        audio_bytes=audio_bytes,
        duration_seconds=estimate_tts_duration_seconds(text),
        audio_format=resolved_format,
        audio_size=len(audio_bytes),
        trace_id=response_trace_id,
        usage_characters=len(text),
        voice_id=voice_id,
        speaker_voices={},
        line_count=1,
    )


async def synthesize_dialogue_elevenlabs_tts(
    *,
    turns: list[DialogueTurn],
    model: str,
    fallback_voice_id: str,
    speed: float,
    language: str = "",
) -> MiniMaxAudioResult:
    speaker_voices = assign_elevenlabs_dialogue_voices(
        turns,
        fallback_voice_id=fallback_voice_id,
        language=language,
    )
    chunks: list[bytes] = []
    trace_ids: list[str] = []
    total_usage = 0

    for turn in turns:
        text = naturalize_dialogue_turn_text(turn.text)
        generated = await synthesize_elevenlabs_tts(
            text=text,
            model=model,
            voice_id=speaker_voices.get(turn.speaker) or fallback_voice_id,
            speed=speed,
            audio_format="pcm",
        )
        chunks.append(generated.audio_bytes)
        if generated.trace_id:
            trace_ids.append(generated.trace_id)
        total_usage += generated.usage_characters

    if not chunks:
        raise AudioGenerationError("dialogue_audio_empty")

    audio_bytes, duration_seconds = concatenate_pcm16_audio(
        chunks,
        sample_rate=ELEVENLABS_DIALOGUE_SAMPLE_RATE,
        pause_seconds=ELEVENLABS_DIALOGUE_PAUSE_SECONDS,
        pause_after_seconds=[turn.pause_after_seconds for turn in turns],
    )
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


async def elevenlabs_client_get(path: str, *, timeout: int) -> dict[str, Any]:
    base_url = settings.elevenlabs_api_base_url.rstrip("/")
    headers = {"xi-api-key": settings.elevenlabs_api_key}
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(f"{base_url}{path}", headers=headers)
            response.raise_for_status()
            body = response.json()
    except httpx.HTTPStatusError as exc:
        raise AudioGenerationError(elevenlabs_http_error_detail(exc.response)) from exc
    except httpx.HTTPError as exc:
        raise AudioGenerationError("elevenlabs_request_failed") from exc
    except ValueError as exc:
        raise AudioGenerationError("elevenlabs_response_invalid_json") from exc
    return body


async def elevenlabs_client_post_audio(
    path: str,
    payload: dict[str, Any],
    *,
    timeout: int,
    output_format: str,
) -> tuple[bytes, str, str]:
    base_url = settings.elevenlabs_api_base_url.rstrip("/")
    headers = {
        "xi-api-key": settings.elevenlabs_api_key,
        "Content-Type": "application/json",
    }
    params = {"output_format": output_format}
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(f"{base_url}{path}", headers=headers, params=params, json=payload)
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise AudioGenerationError(elevenlabs_http_error_detail(exc.response)) from exc
    except httpx.HTTPError as exc:
        raise AudioGenerationError("elevenlabs_request_failed") from exc

    if not response.content:
        raise AudioGenerationError("elevenlabs_audio_empty")

    trace_id = (
        response.headers.get("request-id")
        or response.headers.get("x-request-id")
        or response.headers.get("history-item-id")
        or ""
    )
    content_type = response.headers.get("content-type") or ""
    return response.content, trace_id, content_type


def elevenlabs_http_error_detail(response: httpx.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        body = {}
    detail = ""
    if isinstance(body, dict):
        raw_detail = body.get("detail")
        if isinstance(raw_detail, dict):
            detail = str(raw_detail.get("message") or raw_detail.get("status") or "")
        elif raw_detail:
            detail = str(raw_detail)
    suffix = f":{detail}" if detail else ""
    return f"elevenlabs_error_{response.status_code}{suffix}"


def elevenlabs_audio_format(output_format: str, content_type: str, fallback: str) -> str:
    normalized_output = output_format.strip().lower()
    if normalized_output.startswith("mp3"):
        return "mp3"
    if normalized_output.startswith("wav") or "audio/wav" in content_type.lower():
        return "wav"
    if normalized_output.startswith("pcm"):
        return "pcm"
    return fallback or "mp3"


def elevenlabs_output_format(audio_format: str) -> str:
    requested = audio_format.lower().strip()
    if requested == "pcm":
        return f"pcm_{ELEVENLABS_DIALOGUE_SAMPLE_RATE}"
    configured = settings.elevenlabs_tts_output_format.strip() or "mp3_44100_128"
    if requested == "mp3" and not configured.lower().startswith("mp3"):
        return "mp3_44100_128"
    return configured


def estimate_tts_duration_seconds(text: str) -> float:
    words = [word for word in re.split(r"\s+", text.strip()) if word]
    word_estimate = len(words) / 2.35 if words else 0
    char_estimate = len(text.strip()) / 13.0 if text.strip() else 0
    return round(max(word_estimate, char_estimate, 0.5), 2)


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


def default_elevenlabs_tts_model() -> str:
    model = settings.elevenlabs_tts_model.strip()
    if model in ELEVENLABS_TTS_MODELS:
        return model
    return ELEVENLABS_TTS_MODELS[0]


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
        text, pause_after_seconds = clean_dialogue_turn_payload(match.group(2))
        if speaker and text:
            turns.append(
                DialogueTurn(
                    speaker=speaker,
                    text=text,
                    pause_after_seconds=pause_after_seconds,
                )
            )

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
        text, pause_after_seconds = clean_dialogue_turn_payload(match.group(2))
        if speaker and text:
            turns.append(
                DialogueTurn(
                    speaker=speaker,
                    text=text,
                    pause_after_seconds=pause_after_seconds,
                )
            )

    total_text = "\n".join(turn.text for turn in turns).strip()
    if turns and len(total_text) >= 10000:
        raise AudioGenerationError("exam_item_audio_source_too_long")
    return turns


EXAM_AUDIO_SECTION_CODES = {"LISTENING", "SPEAKING"}


def exam_item_source_text_hash(item: ExamItemModel) -> str:
    """Hash of the TTS source text, used to detect outdated generated audio."""
    return hashlib.sha256(exam_item_audio_source_text(item).encode("utf-8")).hexdigest()


def exam_item_audio_source_text(item: ExamItemModel) -> str:
    source_text = (item.stimulus_text or item.prompt_text or "").strip()
    if not source_text:
        return ""

    if item.item_type == "fill_blank" and "[BLANK]" in source_text:
        answers = []
        if isinstance(item.correct_answer, dict):
            raw_blanks = item.correct_answer.get("blanks")
            if isinstance(raw_blanks, list):
                answers = [str(value).strip() for value in raw_blanks]

        if answers:
            next_text = source_text
            for answer in answers:
                replacement = answer or "..."
                next_text = next_text.replace("[BLANK]", replacement, 1)
            return next_text

    return source_text


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


def clean_dialogue_turn_payload(value: str) -> tuple[str, float]:
    text = clean_dialogue_text(value)
    pause_after_seconds = 0.0
    while True:
        match = TRAILING_AUDIO_PAUSE_TAG_RE.search(text)
        if not match:
            break
        pause_after_seconds = max(pause_after_seconds, safe_audio_pause_seconds(match.group(1)))
        text = text[: match.start()].strip()
    return text, pause_after_seconds


def safe_audio_pause_seconds(value: str) -> float:
    try:
        return min(max(float(value), 0.0), MAX_AUDIO_PAUSE_SECONDS)
    except ValueError:
        return 0.0


def naturalize_dialogue_turn_text(value: str) -> str:
    cleaned = clean_dialogue_text(value)
    cleaned = AUDIO_PAUSE_TAG_RE.sub(" ", cleaned)
    cleaned = re.sub(r"^[A-Za-z][A-Za-z .'-]{0,47}[:：]\s*", "", cleaned).strip()
    return re.sub(r"\s+", " ", cleaned)


def assign_dialogue_voices(
    turns: list[DialogueTurn],
    *,
    fallback_voice_id: str,
    language: str = "",
) -> dict[str, str]:
    speaker_by_key: dict[str, str] = {}
    for turn in turns:
        key = normalized_speaker_key(turn.speaker)
        if key and key not in speaker_by_key:
            speaker_by_key[key] = turn.speaker

    speaker_voices: dict[str, str] = {}
    used_voices: set[str] = set()

    for key in sorted(speaker_by_key):
        voice_id = None
        if is_arabic_language(language) or is_arabic_voice_id(fallback_voice_id):
            voice_id = ARABIC_MINIMAX_DIALOGUE_PERSONA_VOICES.get(key)
        voice_id = voice_id or DIALOGUE_PERSONA_VOICES.get(key)
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

        if is_arabic_language(language) or is_arabic_voice_id(fallback_voice_id):
            voice_pool = (
                CLEAR_ARABIC_FEMALE_DIALOGUE_VOICES
                if gender == "female"
                else CLEAR_ARABIC_MALE_DIALOGUE_VOICES
            )
        else:
            voice_pool = CLEAR_FEMALE_DIALOGUE_VOICES if gender == "female" else CLEAR_MALE_DIALOGUE_VOICES
        voice_id = stable_voice_from_pool(key=key, voice_pool=voice_pool, used_voices=used_voices)
        speaker_voices[speaker] = voice_id or fallback_voice_id
        used_voices.add(speaker_voices[speaker])

    return speaker_voices


def assign_elevenlabs_dialogue_voices(
    turns: list[DialogueTurn],
    *,
    fallback_voice_id: str,
    language: str = "",
) -> dict[str, str]:
    speaker_by_key: dict[str, str] = {}
    for turn in turns:
        key = normalized_speaker_key(turn.speaker)
        if key and key not in speaker_by_key:
            speaker_by_key[key] = turn.speaker

    speaker_voices: dict[str, str] = {}
    used_voices: set[str] = set()

    if is_arabic_language(language):
        for key in sorted(speaker_by_key):
            voice_id = ELEVENLABS_ARABIC_PERSONA_VOICES.get(key)
            if not voice_id:
                continue
            speaker = speaker_by_key[key]
            if voice_id in used_voices:
                gender = elevenlabs_voice_gender(voice_id)
                if gender == "unknown":
                    gender = infer_speaker_gender(speaker)
                if gender == "unknown":
                    gender = stable_unknown_speaker_gender(key)
                voice_pool = elevenlabs_voice_pool_for_gender(
                    gender,
                    fallback_voice_id=fallback_voice_id,
                    language=language,
                )
                voice_id = stable_voice_from_pool(key=key, voice_pool=voice_pool, used_voices=used_voices) or voice_id
            speaker_voices[speaker] = voice_id
            used_voices.add(voice_id)

    for key in sorted(speaker_by_key):
        speaker = speaker_by_key[key]
        if speaker in speaker_voices:
            continue

        gender = infer_speaker_gender(speaker)
        if gender == "unknown":
            gender = stable_unknown_speaker_gender(key)
        voice_pool = elevenlabs_voice_pool_for_gender(gender, fallback_voice_id=fallback_voice_id, language=language)
        voice_id = stable_voice_from_pool(key=key, voice_pool=voice_pool, used_voices=used_voices)
        speaker_voices[speaker] = voice_id or fallback_voice_id
        used_voices.add(speaker_voices[speaker])

    return speaker_voices


def elevenlabs_voice_pool_for_gender(
    gender: str,
    *,
    fallback_voice_id: str,
    language: str = "",
) -> tuple[str, ...]:
    if is_arabic_language(language):
        env_voice = (
            settings.elevenlabs_arabic_female_voice_id.strip()
            if gender == "female"
            else settings.elevenlabs_arabic_male_voice_id.strip()
        )
        curated_pool = (
            ELEVENLABS_ARABIC_FEMALE_DIALOGUE_VOICES
            if gender == "female"
            else ELEVENLABS_ARABIC_MALE_DIALOGUE_VOICES
        )
        env_voice = curated_elevenlabs_arabic_voice_id(env_voice, gender=gender)
        fallback = curated_elevenlabs_arabic_voice_id(fallback_voice_id, gender=gender)
        return tuple(dict.fromkeys(voice for voice in [env_voice, *curated_pool, fallback] if voice).keys())

    default_voice = settings.elevenlabs_tts_voice_id.strip() or ELEVENLABS_ARABIC_DEFAULT_MALE_VOICE_ID
    fallback = fallback_voice_id.strip()
    return tuple(dict.fromkeys(voice for voice in [fallback, default_voice] if voice).keys())


def elevenlabs_voice_gender(voice_id: str) -> str:
    metadata = ELEVENLABS_ARABIC_VOICE_METADATA.get(voice_id)
    if metadata:
        gender = str(metadata.get("gender") or "").strip().lower()
        if gender in {"male", "female"}:
            return gender
    return infer_voice_gender(voice_id=voice_id)


def infer_speaker_gender(speaker: str) -> str:
    normalized = normalized_speaker_key(speaker)
    female_names = {
        "female",
        "woman",
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
        "barista",
        "cafestaff",
        "staff",
        "fatimah",
        "khadijah",
        "aisha",
        "noura",
        "nura",
        "layla",
    }
    male_names = {
        "male",
        "man",
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
        "seller",
        "shopkeeper",
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


def concatenate_wav_audio(
    chunks: list[bytes],
    *,
    pause_seconds: float = 0.25,
    pause_after_seconds: Optional[list[float]] = None,
) -> tuple[bytes, float]:
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
    output = io.BytesIO()

    with wave.open(output, "wb") as writer:
        writer.setnchannels(nchannels)
        writer.setsampwidth(sampwidth)
        writer.setframerate(framerate)
        writer.setcomptype(comptype, compname)
        for index, frame_bytes in enumerate(frames):
            writer.writeframes(frame_bytes)
            pause_for_turn = dialogue_pause_seconds_for_index(
                index=index,
                chunk_count=len(frames),
                default_pause_seconds=pause_seconds,
                pause_after_seconds=pause_after_seconds,
            )
            pause_frames = max(0, int(framerate * pause_for_turn))
            if index < len(frames) - 1 and pause_frames:
                pause_bytes = b"\x00" * pause_frames * nchannels * sampwidth
                writer.writeframes(pause_bytes)
                total_frames += pause_frames

    duration_seconds = round(total_frames / framerate, 2)
    return output.getvalue(), max(duration_seconds, 0.01)


def concatenate_pcm16_audio(
    chunks: list[bytes],
    *,
    sample_rate: int,
    pause_seconds: float,
    pause_after_seconds: Optional[list[float]] = None,
) -> tuple[bytes, float]:
    if not chunks:
        raise AudioGenerationError("dialogue_audio_empty")

    frames: list[bytes] = []
    total_frames = 0
    for chunk in chunks:
        if len(chunk) % 2 != 0:
            raise AudioGenerationError("dialogue_audio_pcm16_invalid")
        frame_bytes = normalize_wav_frame_volume(chunk, 2)
        frames.append(frame_bytes)
        total_frames += len(frame_bytes) // 2

    output = io.BytesIO()

    with wave.open(output, "wb") as writer:
        writer.setnchannels(1)
        writer.setsampwidth(2)
        writer.setframerate(sample_rate)
        for index, frame_bytes in enumerate(frames):
            writer.writeframes(frame_bytes)
            pause_for_turn = dialogue_pause_seconds_for_index(
                index=index,
                chunk_count=len(frames),
                default_pause_seconds=pause_seconds,
                pause_after_seconds=pause_after_seconds,
            )
            pause_frames = max(0, int(sample_rate * pause_for_turn))
            if index < len(frames) - 1 and pause_frames:
                pause_bytes = b"\x00" * pause_frames * 2
                writer.writeframes(pause_bytes)
                total_frames += pause_frames

    duration_seconds = round(total_frames / sample_rate, 2)
    return output.getvalue(), max(duration_seconds, 0.01)


def dialogue_pause_seconds_for_index(
    *,
    index: int,
    chunk_count: int,
    default_pause_seconds: float,
    pause_after_seconds: Optional[list[float]],
) -> float:
    if index >= chunk_count - 1:
        return 0.0
    override = 0.0
    if pause_after_seconds and index < len(pause_after_seconds):
        override = pause_after_seconds[index]
    return max(default_pause_seconds, override)


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
    provider: str,
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
        "provider": provider,
        "model": model,
        "voice_id": voice_id,
        "speaker_voices": speaker_voices,
        "line_count": line_count,
        "script_content_hash": file_sha256(lesson.listening_script_path),
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
    data["provider"] = provider
    data["assets"] = next_assets
    write_yaml_mapping(lesson.audio_manifest_path, data)
    return data


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
            production_tracker_level_matches(row.get("level", ""), lesson)
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


def production_tracker_level_matches(row_level: str, lesson: LessonAudioReference) -> bool:
    normalized_row_level = (row_level or "").strip().lower()
    level_code = lesson.level_code.strip()
    language = lesson.language.strip().lower()
    expected_levels = {
        level_code.lower(),
        f"{language}/{level_code}".lower(),
    }
    return normalized_row_level in expected_levels


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
