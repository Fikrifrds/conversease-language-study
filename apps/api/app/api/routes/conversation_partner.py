from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.routes.conversation import (
    allowed_recorded_audio_content_type,
    speech_to_text_http_error,
)
from app.data.curriculum import requires_pro
from app.db.session import get_db
from app.domain.conversation_partner import (
    DEFAULT_LEVEL,
    get_topic,
    topic_payload,
    topics_for_level,
)
from app.domain.users import User
from app.repositories.billing import BillingRepository, InsufficientMinutesError
from app.repositories.conversation_partner import ConversationPartnerRepository
from app.services.audio_generation import synthesize_partner_reply_audio
from app.services.conversation_partner_chat import (
    generate_partner_reply,
    summarize_session,
)
from app.services.speech_to_text import SpeechToTextError, transcribe_recorded_audio


router = APIRouter()

# Opening lines are static per topic, so their TTS is identical every time a
# session is opened or resumed. Cache the synthesized data-URL per opening text
# to avoid paying for the same TTS on every create/resume.
_opening_audio_cache: dict[str, Optional[str]] = {}


async def _opening_audio_for(topic) -> Optional[str]:
    if topic.opening_line in _opening_audio_cache:
        return _opening_audio_cache[topic.opening_line]
    audio = await synthesize_partner_reply_audio(text=topic.opening_line)
    # Only cache successful synthesis so a transient TTS failure can retry later.
    if audio is not None:
        _opening_audio_cache[topic.opening_line] = audio
    return audio


class CreatePartnerSessionPayload(BaseModel):
    topic_key: str = Field(...)
    language_code: str = Field(default="en")


def get_repository(db: Session = Depends(get_db)) -> ConversationPartnerRepository:
    return ConversationPartnerRepository(db)


@router.get("/conversation-partner/topics")
async def list_partner_topics(
    level_code: str = DEFAULT_LEVEL,
    current_user: User = Depends(get_current_user),
) -> dict:
    topics = topics_for_level(level_code)
    return {"data": [topic_payload(topic) for topic in topics]}


@router.post("/conversation-partner/sessions")
async def create_partner_session(
    payload: CreatePartnerSessionPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    repository: ConversationPartnerRepository = Depends(get_repository),
) -> dict:
    topic = get_topic(payload.topic_key)
    if topic is None:
        raise HTTPException(status_code=404, detail="partner_topic_not_found")

    billing = BillingRepository(db)
    billing.ensure_free_access(current_user.id)

    # Gate A2+ topics behind Pro, consistent with course and Conversation Coach
    # access (A1 is free, A2-C1 require an active Pro subscription).
    if requires_pro(topic.level_code):
        if not current_user.is_admin and not billing.is_pro(current_user.id):
            raise HTTPException(
                status_code=403,
                detail="conversation_partner_requires_pro",
            )

    # Resume an unfinished session for this topic instead of creating a new one,
    # so abandoned attempts don't pile up. A fresh session is created only when
    # none is open (e.g. after finishing or resetting the topic).
    session = repository.find_open_session(user_id=current_user.id, topic_key=topic.key)
    if session is None:
        session = repository.create_session(
            user_id=current_user.id,
            topic=topic,
            language_code=payload.language_code,
        )

    opening_audio = await _opening_audio_for(topic)

    return {
        "data": {
            "session_id": session.id,
            "topic": topic_payload(topic),
            "opening_line": topic.opening_line,
            "opening_audio": opening_audio,
            "completed_turns": len(session.turns),
            "max_turns": topic.max_turns,
        }
    }


@router.post("/conversation-partner/sessions/{session_id}/turns/audio")
async def create_partner_audio_turn(
    session_id: str,
    audio: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    repository: ConversationPartnerRepository = Depends(get_repository),
) -> dict:
    session = repository.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="partner_session_not_found")
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="partner_session_user_mismatch")

    topic = get_topic(session.scenario_key)
    if topic is None:
        raise HTTPException(status_code=404, detail="partner_topic_not_found")

    if session.status == "completed":
        raise HTTPException(status_code=409, detail="partner_session_completed")

    if not allowed_recorded_audio_content_type(audio.content_type):
        raise HTTPException(status_code=422, detail="unsupported_audio_content_type")

    # Reject out-of-minute users before spending on STT/LLM/TTS. The actual debit
    # happens only after the turn is generated below, so a failed turn is never
    # charged.
    billing = BillingRepository(db)
    billing.ensure_free_access(current_user.id)
    if billing.minute_balance(current_user.id).total_minutes < 1:
        raise HTTPException(status_code=402, detail="Conversation Partner minutes are empty")

    audio_bytes = await audio.read()
    try:
        transcription = await transcribe_recorded_audio(
            audio_bytes=audio_bytes,
            filename=audio.filename or "partner-turn.webm",
            content_type=audio.content_type,
        )
    except SpeechToTextError as exc:
        raise speech_to_text_http_error(exc) from exc

    history = repository.history(session, opening_line=topic.opening_line)
    completed_turns = repository.completed_turns(session)
    reply = await generate_partner_reply(
        topic=topic,
        level_code=session.level_code,
        history=history,
        user_message=transcription.text,
        completed_turns=completed_turns,
    )

    reply_audio = await synthesize_partner_reply_audio(text=reply.reply)

    try:
        billing.consume_minutes(
            user_id=current_user.id,
            requested_minutes=1,
            related_session_id=session_id,
        )
    except InsufficientMinutesError as exc:
        raise HTTPException(status_code=402, detail="Conversation Partner minutes are empty") from exc

    turn = repository.add_turn(
        session=session,
        user_transcript=transcription.text,
        partner_reply=reply.reply,
        completed=reply.should_end,
        input_source=transcription.transcription.input_source,
        stt_provider=transcription.transcription.provider,
        stt_model=transcription.transcription.model,
        stt_transcript_id=transcription.transcription.transcript_id,
        stt_confidence=transcription.transcription.confidence,
        stt_audio_duration_seconds=transcription.transcription.audio_duration_seconds,
        stt_metadata=transcription.transcription.metadata,
    )

    return {
        "data": {
            "session_id": session.id,
            "user_transcript": transcription.text,
            "partner_reply": reply.reply,
            "partner_audio": reply_audio,
            "on_topic": reply.on_topic,
            "should_end": reply.should_end,
            "completed_turns": turn.turn_index + 1,
            "max_turns": topic.max_turns,
        }
    }


@router.post("/conversation-partner/sessions/{session_id}/end")
async def end_partner_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    repository: ConversationPartnerRepository = Depends(get_repository),
) -> dict:
    """End an in-progress session early and return its summary + score."""
    session = repository.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="partner_session_not_found")
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="partner_session_user_mismatch")

    topic = get_topic(session.scenario_key)
    if topic is None:
        raise HTTPException(status_code=404, detail="partner_topic_not_found")

    repository.end_session(session)

    # Reuse a stored summary if present; otherwise compute one from the history.
    stored = session.summary_json
    if not (isinstance(stored, dict) and stored.get("scores")):
        history = repository.history(session, opening_line=topic.opening_line)
        summary = await summarize_session(
            topic=topic,
            level_code=session.level_code,
            history=history,
        )
        repository.save_summary(
            session,
            summary=summary.summary,
            indonesian_explanation=summary.indonesian_explanation,
            scores=summary.scores,
        )
        stored = session.summary_json

    return {
        "data": {
            "session_id": session.id,
            "status": session.status,
            "summary": stored.get("summary", ""),
            "indonesian_explanation": stored.get("indonesian_explanation", ""),
            "scores": stored.get("scores", {}),
            "completed_turns": repository.completed_turns(session),
        }
    }


@router.post("/conversation-partner/sessions/{session_id}/summary")
async def get_partner_summary(
    session_id: str,
    current_user: User = Depends(get_current_user),
    repository: ConversationPartnerRepository = Depends(get_repository),
) -> dict:
    session = repository.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="partner_session_not_found")
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="partner_session_user_mismatch")

    topic = get_topic(session.scenario_key)
    if topic is None:
        raise HTTPException(status_code=404, detail="partner_topic_not_found")

    # Reuse a stored summary if we already computed one for this session so the
    # score is stable and we don't pay for a second LLM call on revisit.
    stored = session.summary_json
    if isinstance(stored, dict) and stored.get("scores"):
        return {
            "data": {
                "session_id": session.id,
                "summary": stored.get("summary", ""),
                "indonesian_explanation": stored.get("indonesian_explanation", ""),
                "scores": stored.get("scores", {}),
                "completed_turns": repository.completed_turns(session),
            }
        }

    history = repository.history(session, opening_line=topic.opening_line)
    summary = await summarize_session(
        topic=topic,
        level_code=session.level_code,
        history=history,
    )
    repository.save_summary(
        session,
        summary=summary.summary,
        indonesian_explanation=summary.indonesian_explanation,
        scores=summary.scores,
    )

    return {
        "data": {
            "session_id": session.id,
            "summary": summary.summary,
            "indonesian_explanation": summary.indonesian_explanation,
            "scores": summary.scores,
            "completed_turns": repository.completed_turns(session),
        }
    }


def _session_summary_payload(session) -> dict:
    """Compact history-row payload: identity, status, turns, and score if any."""
    topic = get_topic(session.scenario_key)
    summary = session.summary_json if isinstance(session.summary_json, dict) else None
    return {
        "session_id": session.id,
        "topic_key": session.scenario_key,
        "topic_title": topic.title if topic else session.scenario_key,
        "level_code": session.level_code,
        "status": session.status,
        "completed_turns": len(session.turns),
        "max_turns": topic.max_turns if topic else None,
        "overall_score": summary.get("overall") if summary else None,
        "scores": summary.get("scores") if summary else None,
        "updated_at": session.updated_at.isoformat(),
    }


@router.get("/conversation-partner/topic-progress")
async def get_partner_topic_progress(
    current_user: User = Depends(get_current_user),
    repository: ConversationPartnerRepository = Depends(get_repository),
) -> dict:
    """Per-topic progress (best score, done, open session) keyed by topic key, so
    each topic card can show its own status inline."""
    return {"data": repository.topic_progress(current_user.id)}


@router.delete("/conversation-partner/topics/{topic_key}/progress")
async def reset_partner_topic(
    topic_key: str,
    current_user: User = Depends(get_current_user),
    repository: ConversationPartnerRepository = Depends(get_repository),
) -> dict:
    """Clear a topic's progress so it returns to a fresh 'not started' state."""
    removed = repository.reset_topic(user_id=current_user.id, topic_key=topic_key)
    return {"data": {"topic_key": topic_key, "removed_sessions": removed}}


@router.get("/conversation-partner/sessions")
async def list_partner_sessions(
    current_user: User = Depends(get_current_user),
    repository: ConversationPartnerRepository = Depends(get_repository),
) -> dict:
    sessions = repository.list_sessions(current_user.id)
    return {"data": [_session_summary_payload(session) for session in sessions]}


@router.get("/conversation-partner/sessions/{session_id}")
async def get_partner_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    repository: ConversationPartnerRepository = Depends(get_repository),
) -> dict:
    session = repository.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="partner_session_not_found")
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="partner_session_user_mismatch")

    topic = get_topic(session.scenario_key)
    messages = []
    if topic:
        messages.append({"role": "partner", "text": topic.opening_line})
    for turn in sorted(session.turns, key=lambda t: t.turn_index):
        messages.append({"role": "user", "text": turn.user_transcript})
        if turn.coach_reply:
            messages.append({"role": "partner", "text": turn.coach_reply})

    summary = session.summary_json if isinstance(session.summary_json, dict) else None
    return {
        "data": {
            **_session_summary_payload(session),
            "topic": topic_payload(topic) if topic else None,
            "messages": messages,
            "summary": summary,
        }
    }
