from __future__ import annotations

from datetime import datetime
from hashlib import sha256
from typing import Any, Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AudioVoicePreviewModel
from app.services.audio_generation import audio_playback_url


DEFAULT_VOICE_PREVIEW_SAMPLE_TEXT = (
    "Hello, welcome to Conversease. Listen, repeat, and speak with clear confidence."
)


class AudioVoicePreviewRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(
        self,
        *,
        provider: str,
        model: str,
        voice_id: str,
        speed: float,
        sample_text_hash: str,
    ) -> Optional[AudioVoicePreviewModel]:
        return self.db.execute(
            select(AudioVoicePreviewModel).where(
                AudioVoicePreviewModel.provider == provider,
                AudioVoicePreviewModel.model == model,
                AudioVoicePreviewModel.voice_id == voice_id,
                AudioVoicePreviewModel.speed == speed,
                AudioVoicePreviewModel.sample_text_hash == sample_text_hash,
            )
        ).scalar_one_or_none()

    def list_previews(
        self,
        *,
        provider: str,
        model: Optional[str] = None,
        speed: Optional[float] = None,
        sample_text_hash: Optional[str] = None,
    ) -> list[AudioVoicePreviewModel]:
        query = select(AudioVoicePreviewModel).where(AudioVoicePreviewModel.provider == provider)
        if model:
            query = query.where(AudioVoicePreviewModel.model == model)
        if speed is not None:
            query = query.where(AudioVoicePreviewModel.speed == speed)
        if sample_text_hash:
            query = query.where(AudioVoicePreviewModel.sample_text_hash == sample_text_hash)
        return (
            self.db.execute(
                query.order_by(AudioVoicePreviewModel.model.asc(), AudioVoicePreviewModel.voice_id.asc())
            )
            .scalars()
            .all()
        )

    def upsert_from_generated(
        self,
        *,
        provider: str,
        generated: dict[str, Any],
        speed: float,
        sample_text_hash: str,
    ) -> AudioVoicePreviewModel:
        now = datetime.utcnow()
        existing = self.get(
            provider=provider,
            model=str(generated["model"]),
            voice_id=str(generated["voice_id"]),
            speed=speed,
            sample_text_hash=sample_text_hash,
        )
        if existing is None:
            existing = AudioVoicePreviewModel(
                id=f"voice-preview-{uuid4().hex[:16]}",
                provider=provider,
                model=str(generated["model"]),
                voice_id=str(generated["voice_id"]),
                speed=speed,
                sample_text_hash=sample_text_hash,
                sample_text=str(generated["sample_text"]),
                audio_url=str(generated["audio_url"]),
                object_key=str(generated["object_key"]),
                duration_seconds=float(generated["duration_seconds"]),
                audio_format=str(generated["audio_format"]),
                audio_size=int(generated["audio_size"]),
                trace_id=str(generated.get("trace_id") or ""),
                usage_characters=int(generated.get("usage_characters") or 0),
                generated_by=str(generated.get("generated_by") or "admin")[:160],
                created_at=now,
                updated_at=now,
            )
            self.db.add(existing)
        else:
            existing.sample_text = str(generated["sample_text"])
            existing.audio_url = str(generated["audio_url"])
            existing.object_key = str(generated["object_key"])
            existing.duration_seconds = float(generated["duration_seconds"])
            existing.audio_format = str(generated["audio_format"])
            existing.audio_size = int(generated["audio_size"])
            existing.trace_id = str(generated.get("trace_id") or "")
            existing.usage_characters = int(generated.get("usage_characters") or 0)
            existing.generated_by = str(generated.get("generated_by") or "admin")[:160]
            existing.updated_at = now

        self.db.commit()
        self.db.refresh(existing)
        return existing


def normalize_voice_preview_sample_text(sample_text: Optional[str]) -> str:
    return " ".join((sample_text or DEFAULT_VOICE_PREVIEW_SAMPLE_TEXT).strip().split())


def voice_preview_sample_hash(sample_text: str) -> str:
    return sha256(sample_text.encode("utf-8")).hexdigest()


def normalize_preview_speed(speed: float) -> float:
    return round(float(speed), 2)


def voice_preview_payload(preview: AudioVoicePreviewModel, *, cached: bool = True) -> dict[str, Any]:
    return {
        "id": preview.id,
        "provider": preview.provider,
        "audio_url": preview.audio_url,
        "playback_url": audio_playback_url(audio_url=preview.audio_url, storage_key=preview.object_key),
        "object_key": preview.object_key,
        "duration_seconds": preview.duration_seconds,
        "audio_format": preview.audio_format,
        "audio_size": preview.audio_size,
        "model": preview.model,
        "voice_id": preview.voice_id,
        "speed": preview.speed,
        "trace_id": preview.trace_id or "",
        "usage_characters": preview.usage_characters,
        "sample_text": preview.sample_text,
        "sample_text_hash": preview.sample_text_hash,
        "generated_by": preview.generated_by,
        "generated_at": preview.updated_at.isoformat(),
        "created_at": preview.created_at.isoformat(),
        "updated_at": preview.updated_at.isoformat(),
        "cached": cached,
    }
