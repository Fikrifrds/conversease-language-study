from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Optional

import httpx

from app.core.config import settings
from app.domain.conversation_practice import TurnTranscription


class SpeechToTextError(Exception):
    pass


@dataclass(frozen=True)
class SpeechToTextResult:
    text: str
    transcription: TurnTranscription


async def transcribe_recorded_audio(
    *,
    audio_bytes: bytes,
    filename: str,
    content_type: Optional[str],
) -> SpeechToTextResult:
    if not settings.assemblyai_api_key:
        raise SpeechToTextError("assemblyai_api_key_missing")

    if not audio_bytes:
        raise SpeechToTextError("audio_file_empty")

    if len(audio_bytes) > settings.assemblyai_max_audio_bytes:
        raise SpeechToTextError("audio_file_too_large")

    base_url = settings.assemblyai_api_base_url.rstrip("/")
    headers = {"authorization": settings.assemblyai_api_key}

    async with httpx.AsyncClient(timeout=settings.assemblyai_transcript_timeout_seconds) as client:
        upload_url = await upload_audio_to_assemblyai(
            client=client,
            base_url=base_url,
            headers=headers,
            audio_bytes=audio_bytes,
            content_type=content_type,
        )
        transcript = await request_transcript(
            client=client,
            base_url=base_url,
            headers=headers,
            audio_url=upload_url,
        )
        completed = await poll_transcript_until_completed(
            client=client,
            base_url=base_url,
            headers=headers,
            transcript_id=str(transcript["id"]),
        )

    text = str(completed.get("text") or "").strip()
    if not text:
        raise SpeechToTextError("transcript_empty")

    model = ",".join(settings.assemblyai_speech_models)
    transcript_id = str(completed.get("id") or transcript.get("id") or "")
    return SpeechToTextResult(
        text=text,
        transcription=TurnTranscription(
            input_source="audio",
            provider="assemblyai",
            model=model,
            transcript_id=transcript_id,
            confidence=float(completed["confidence"]) if completed.get("confidence") is not None else None,
            audio_duration_seconds=duration_seconds(completed),
            metadata={
                "filename": filename,
                "content_type": content_type or "",
                "status": completed.get("status"),
                "language_code": completed.get("language_code"),
                "audio_url": upload_url,
            },
        ),
    )


async def upload_audio_to_assemblyai(
    *,
    client: httpx.AsyncClient,
    base_url: str,
    headers: dict[str, str],
    audio_bytes: bytes,
    content_type: Optional[str],
) -> str:
    request_headers = dict(headers)
    if content_type:
        request_headers["Content-Type"] = content_type

    try:
        response = await client.post(f"{base_url}/v2/upload", headers=request_headers, content=audio_bytes)
        response.raise_for_status()
        body = response.json()
    except httpx.HTTPError as exc:
        raise SpeechToTextError("assemblyai_upload_failed") from exc
    except ValueError as exc:
        raise SpeechToTextError("assemblyai_upload_invalid_json") from exc

    upload_url = body.get("upload_url")
    if not isinstance(upload_url, str) or not upload_url:
        raise SpeechToTextError("assemblyai_upload_url_missing")
    return upload_url


async def request_transcript(
    *,
    client: httpx.AsyncClient,
    base_url: str,
    headers: dict[str, str],
    audio_url: str,
) -> dict[str, Any]:
    payload = {
        "audio_url": audio_url,
        "speech_models": settings.assemblyai_speech_models,
        "language_detection": True,
    }
    try:
        response = await client.post(
            f"{base_url}/v2/transcript",
            headers={**headers, "Content-Type": "application/json"},
            json=payload,
        )
        response.raise_for_status()
        body = response.json()
    except httpx.HTTPError as exc:
        raise SpeechToTextError("assemblyai_transcript_request_failed") from exc
    except ValueError as exc:
        raise SpeechToTextError("assemblyai_transcript_invalid_json") from exc

    if not body.get("id"):
        raise SpeechToTextError("assemblyai_transcript_id_missing")
    return body


async def poll_transcript_until_completed(
    *,
    client: httpx.AsyncClient,
    base_url: str,
    headers: dict[str, str],
    transcript_id: str,
) -> dict[str, Any]:
    deadline = asyncio.get_running_loop().time() + settings.assemblyai_transcript_timeout_seconds
    polling_url = f"{base_url}/v2/transcript/{transcript_id}"

    while True:
        try:
            response = await client.get(polling_url, headers=headers)
            response.raise_for_status()
            body = response.json()
        except httpx.HTTPError as exc:
            raise SpeechToTextError("assemblyai_transcript_poll_failed") from exc
        except ValueError as exc:
            raise SpeechToTextError("assemblyai_transcript_poll_invalid_json") from exc

        status = body.get("status")
        if status == "completed":
            return body
        if status == "error":
            raise SpeechToTextError(f"assemblyai_transcript_error:{body.get('error') or 'unknown'}")

        if asyncio.get_running_loop().time() >= deadline:
            raise SpeechToTextError("assemblyai_transcript_timeout")

        await asyncio.sleep(settings.assemblyai_poll_interval_seconds)


def duration_seconds(transcript: dict[str, Any]) -> Optional[float]:
    audio_duration = transcript.get("audio_duration")
    if audio_duration is None:
        return None

    try:
        return round(float(audio_duration), 2)
    except (TypeError, ValueError):
        return None
