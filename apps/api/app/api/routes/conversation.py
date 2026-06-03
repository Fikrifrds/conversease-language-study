from fastapi import APIRouter, Depends, HTTPException
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
