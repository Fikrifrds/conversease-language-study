from __future__ import annotations

from typing import Any, Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.repositories.audio_voice_previews import (
    AudioVoicePreviewRepository,
    normalize_preview_speed,
    normalize_voice_preview_sample_text,
    voice_preview_payload,
    voice_preview_sample_hash,
)
from app.services.audio_generation import (
    AudioGenerationError,
    generate_voice_preview_audio,
    normalized_model,
)


VOICE_PREVIEW_PROVIDER = "minimax"


async def get_or_generate_voice_preview(
    db: Session,
    *,
    model: Optional[str] = None,
    voice_id: Optional[str] = None,
    speed: float = 1.0,
    sample_text: Optional[str] = None,
    generated_by: str = "admin",
    force: bool = False,
) -> dict[str, Any]:
    selected_model = normalized_model(model or settings.minimax_tts_model)
    selected_voice_id = (voice_id or settings.minimax_tts_voice_id).strip()
    if not selected_voice_id:
        raise AudioGenerationError("minimax_voice_id_missing")

    normalized_speed = normalize_preview_speed(speed)
    preview_text = normalized_preview_text(sample_text)
    sample_text_hash = voice_preview_sample_hash(preview_text)
    repository = AudioVoicePreviewRepository(db)

    if not force:
        existing = repository.get(
            provider=VOICE_PREVIEW_PROVIDER,
            model=selected_model,
            voice_id=selected_voice_id,
            speed=normalized_speed,
            sample_text_hash=sample_text_hash,
        )
        if existing is not None:
            return voice_preview_payload(existing, cached=True)

    generated = await generate_voice_preview_audio(
        model=selected_model,
        voice_id=selected_voice_id,
        speed=normalized_speed,
        sample_text=preview_text,
        generated_by=generated_by,
    )
    saved = repository.upsert_from_generated(
        provider=VOICE_PREVIEW_PROVIDER,
        generated=generated,
        speed=normalized_speed,
        sample_text_hash=sample_text_hash,
    )
    return voice_preview_payload(saved, cached=False)


def list_voice_preview_cache(
    db: Session,
    *,
    model: Optional[str] = None,
    speed: Optional[float] = None,
    sample_text: Optional[str] = None,
) -> list[dict[str, Any]]:
    selected_model = normalized_model(model) if model else None
    normalized_speed = normalize_preview_speed(speed) if speed is not None else None
    sample_text_hash = voice_preview_sample_hash(normalized_preview_text(sample_text))
    repository = AudioVoicePreviewRepository(db)
    previews = repository.list_previews(
        provider=VOICE_PREVIEW_PROVIDER,
        model=selected_model,
        speed=normalized_speed,
        sample_text_hash=sample_text_hash,
    )
    return [voice_preview_payload(preview, cached=True) for preview in previews]


def normalized_preview_text(sample_text: Optional[str]) -> str:
    preview_text = normalize_voice_preview_sample_text(sample_text)
    if len(preview_text) < 8:
        raise AudioGenerationError("voice_preview_text_empty")
    if len(preview_text) > 500:
        raise AudioGenerationError("voice_preview_text_too_long")
    return preview_text
