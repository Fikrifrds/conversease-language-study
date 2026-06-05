from datetime import datetime
from typing import List, Optional, Tuple
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import ConversationSessionModel, ConversationTurnModel
from app.domain.conversation_partner import PartnerTopic


class ConversationPartnerRepository:
    """Persistence for Conversation Partner sessions.

    Reuses the conversation_sessions / conversation_turns tables with
    mode="conversation_partner". Per-turn feedback rows are not used here;
    scoring happens once at session end via the summary endpoint.
    """

    MODE = "conversation_partner"

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_session(
        self,
        *,
        user_id: str,
        topic: PartnerTopic,
        language_code: str = "en",
    ) -> ConversationSessionModel:
        now = datetime.utcnow()
        session = ConversationSessionModel(
            id=f"partner-{uuid4().hex[:10]}",
            user_id=user_id,
            demo_user_id=user_id,
            language_code=language_code,
            level_code=topic.level_code,
            mode=self.MODE,
            scenario_key=topic.key,
            lesson_slug=topic.key,
            status="started",
            created_at=now,
            updated_at=now,
        )
        self.db.add(session)
        self.db.commit()
        return session

    def get_session(self, session_id: str) -> Optional[ConversationSessionModel]:
        return self.db.execute(
            select(ConversationSessionModel)
            .where(
                ConversationSessionModel.id == session_id,
                ConversationSessionModel.mode == self.MODE,
            )
            .options(selectinload(ConversationSessionModel.turns))
        ).scalar_one_or_none()

    def add_turn(
        self,
        *,
        session: ConversationSessionModel,
        user_transcript: str,
        partner_reply: str,
        completed: bool,
        input_source: str = "audio",
        stt_provider: Optional[str] = None,
        stt_model: Optional[str] = None,
        stt_transcript_id: Optional[str] = None,
        stt_confidence: Optional[float] = None,
        stt_audio_duration_seconds: Optional[float] = None,
        stt_metadata: Optional[dict] = None,
    ) -> ConversationTurnModel:
        now = datetime.utcnow()
        turn_index = len(session.turns)
        turn = ConversationTurnModel(
            id=f"pturn-{uuid4().hex[:10]}",
            session_id=session.id,
            turn_index=turn_index,
            user_transcript=user_transcript.strip(),
            coach_reply=partner_reply,
            minutes_consumed=1,
            input_source=input_source,
            stt_provider=stt_provider,
            stt_model=stt_model,
            stt_transcript_id=stt_transcript_id,
            stt_confidence=stt_confidence,
            stt_audio_duration_seconds=stt_audio_duration_seconds,
            stt_metadata_json=stt_metadata,
            created_at=now,
        )
        session.turns.append(turn)
        session.updated_at = now
        session.status = "completed" if completed else "in_progress"
        self.db.commit()
        return turn

    def history(
        self,
        session: ConversationSessionModel,
        opening_line: str = "",
    ) -> List[Tuple[str, str]]:
        """Ordered (role, text) pairs, starting with the partner's opening line so
        the conversation the LLM sees always begins with the partner turn, then
        alternates user -> partner for each completed turn."""
        pairs: List[Tuple[str, str]] = []
        if opening_line:
            pairs.append(("partner", opening_line))
        for turn in sorted(session.turns, key=lambda t: t.turn_index):
            pairs.append(("user", turn.user_transcript))
            if turn.coach_reply:
                pairs.append(("partner", turn.coach_reply))
        return pairs

    def completed_turns(self, session: ConversationSessionModel) -> int:
        return len(session.turns)
