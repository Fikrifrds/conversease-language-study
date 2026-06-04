import re
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.domain.users import User
from app.domain.conversation_practice import (
    session_payload,
    session_summary,
    turn_payload,
)
from app.repositories.billing import BillingRepository, InsufficientMinutesError
from app.repositories.conversation_practice import ConversationPracticeRepository
from app.services.speech_to_text import SpeechToTextError, transcribe_recorded_audio


router = APIRouter()


class CreateConversationSessionPayload(BaseModel):
    language_code: str = Field(default="en")
    level_code: str = Field(default="A1")
    mode: str = Field(default="lesson_practice_coach")
    scenario_key: str = Field(default="greeting_intro")
    lesson_slug: str = Field(default="saying-hello-and-goodbye")


class CreateConversationTurnPayload(BaseModel):
    transcript: str


def get_repository(db: Session = Depends(get_db)) -> ConversationPracticeRepository:
    return ConversationPracticeRepository(db)


@router.post("/conversation-sessions")
async def create_conversation_session(
    payload: CreateConversationSessionPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    repository: ConversationPracticeRepository = Depends(get_repository),
) -> dict:
    BillingRepository(db).ensure_free_access(current_user.id)
    session = repository.create_session(
        demo_user_id=current_user.id,
        user_id=current_user.id,
        language_code=payload.language_code,
        level_code=payload.level_code,
        mode=payload.mode,
        scenario_key=payload.scenario_key,
        lesson_slug=payload.lesson_slug,
    )
    return {
        "data": session_payload(session)
    }


@router.post("/conversation-sessions/{session_id}/turns")
async def create_conversation_turn(
    session_id: str,
    payload: CreateConversationTurnPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    repository: ConversationPracticeRepository = Depends(get_repository),
) -> dict:
    session = repository.get_session(session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="Conversation session not found")

    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Conversation session user mismatch")

    if not payload.transcript.strip():
        raise HTTPException(status_code=422, detail="Transcript is required")

    if session.completed:
        raise HTTPException(status_code=409, detail="conversation_session_completed")

    try:
        BillingRepository(db).consume_minutes(
            user_id=current_user.id,
            requested_minutes=1,
            related_session_id=session_id,
        )
    except InsufficientMinutesError as exc:
        raise HTTPException(status_code=402, detail="Conversation Coach minutes are empty") from exc

    try:
        session, turn = repository.add_turn(session_id=session_id, transcript=payload.transcript)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return {"data": turn_payload(session, turn)}


@router.post("/conversation-sessions/{session_id}/turns/audio")
async def create_conversation_audio_turn(
    session_id: str,
    audio: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    repository: ConversationPracticeRepository = Depends(get_repository),
) -> dict:
    session = repository.get_session(session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="Conversation session not found")

    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Conversation session user mismatch")

    if session.completed:
        raise HTTPException(status_code=409, detail="conversation_session_completed")

    if not allowed_recorded_audio_content_type(audio.content_type):
        raise HTTPException(status_code=422, detail="unsupported_audio_content_type")

    audio_bytes = await audio.read()
    try:
        transcription = await transcribe_recorded_audio(
            audio_bytes=audio_bytes,
            filename=audio.filename or "conversation-turn.webm",
            content_type=audio.content_type,
        )
    except SpeechToTextError as exc:
        raise speech_to_text_http_error(exc) from exc

    try:
        BillingRepository(db).consume_minutes(
            user_id=current_user.id,
            requested_minutes=1,
            related_session_id=session_id,
        )
    except InsufficientMinutesError as exc:
        raise HTTPException(status_code=402, detail="Conversation Coach minutes are empty") from exc

    try:
        session, turn = repository.add_turn(
            session_id=session_id,
            transcript=transcription.text,
            transcription=transcription.transcription,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return {"data": turn_payload(session, turn)}


@router.post("/pronunciation-checks")
async def check_pronunciation(
    audio: UploadFile = File(...),
    target_phrase: str = Form(...),
    current_user: User = Depends(get_current_user),
) -> dict:
    target = target_phrase.strip()
    if not target:
        raise HTTPException(status_code=422, detail="target_phrase_required")

    if not allowed_recorded_audio_content_type(audio.content_type):
        raise HTTPException(status_code=422, detail="unsupported_audio_content_type")

    audio_bytes = await audio.read()
    try:
        transcription = await transcribe_recorded_audio(
            audio_bytes=audio_bytes,
            filename=audio.filename or "pronunciation.webm",
            content_type=audio.content_type,
        )
    except SpeechToTextError as exc:
        raise speech_to_text_http_error(exc) from exc

    match_ratio = phrase_match_ratio(target, transcription.text)
    return {
        "data": {
            "target_phrase": target,
            "transcript": transcription.text,
            "match_ratio": match_ratio,
            "provider": transcription.transcription.provider,
            "model": transcription.transcription.model,
            "confidence": transcription.transcription.confidence,
        }
    }


@router.get("/conversation-practice/latest")
async def get_latest_conversation_practice(
    lesson_slug: str = "saying-hello-and-goodbye",
    current_user: User = Depends(get_current_user),
    repository: ConversationPracticeRepository = Depends(get_repository),
) -> dict:
    session = repository.latest_session_for_user(
        demo_user_id=current_user.id,
        user_id=current_user.id,
        lesson_slug=lesson_slug,
    )
    return {"data": session_summary(session) if session else None}


@router.delete("/conversation-practice/latest")
async def reset_latest_conversation_practice(
    lesson_slug: str = "saying-hello-and-goodbye",
    current_user: User = Depends(get_current_user),
    repository: ConversationPracticeRepository = Depends(get_repository),
) -> dict:
    reset = repository.reset_latest_for_user(
        demo_user_id=current_user.id,
        user_id=current_user.id,
        lesson_slug=lesson_slug,
    )
    return {"data": {"reset": reset}}


def phrase_match_ratio(target_phrase: str, transcript: str) -> float:
    target_words = _normalize_words(target_phrase)
    if not target_words:
        return 0.0

    heard_words = _normalize_words(transcript)
    heard_counts: dict[str, int] = {}
    for word in heard_words:
        heard_counts[word] = heard_counts.get(word, 0) + 1

    matched = 0
    for word in target_words:
        if heard_counts.get(word, 0) > 0:
            matched += 1
            heard_counts[word] -= 1

    return round(matched / len(target_words), 2)


def _normalize_words(value: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", value.lower())


def allowed_recorded_audio_content_type(content_type: Optional[str]) -> bool:
    if not content_type:
        return True
    normalized = content_type.split(";", 1)[0].strip().lower()
    return (
        normalized.startswith("audio/")
        or normalized in {"video/webm", "application/octet-stream"}
    )


def speech_to_text_http_error(exc: SpeechToTextError) -> HTTPException:
    detail = str(exc)
    if "api_key_missing" in detail:
        return HTTPException(status_code=503, detail=detail)
    if detail in {"audio_file_empty", "audio_file_too_large", "unsupported_audio_content_type"}:
        return HTTPException(status_code=422, detail=detail)
    if detail in {"transcript_empty"}:
        return HTTPException(status_code=422, detail=detail)
    if "timeout" in detail:
        return HTTPException(status_code=504, detail=detail)
    return HTTPException(status_code=502, detail=detail)
