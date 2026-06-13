from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import (
    ConversationFeedbackModel,
    ConversationSessionModel,
    ConversationTurnModel,
    PracticeProgressModel,
)
from app.domain.conversation_practice import (
    DEFAULT_LESSON_SLUG,
    CoachFeedback,
    ConversationSession,
    ConversationTurn,
    TurnTranscription,
    coach_reply_for_turn,
    evaluate_answer,
    learner_name_from_transcripts,
    personalize_feedback,
    personalize_learner_name,
    total_turns_for_lesson,
)


class ConversationPracticeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_session(
        self,
        demo_user_id: str,
        user_id: Optional[str] = None,
        language_code: str = "en",
        level_code: str = "A1",
        mode: str = "lesson_practice_coach",
        scenario_key: str = "greeting_intro",
        lesson_slug: str = DEFAULT_LESSON_SLUG,
    ) -> ConversationSession:
        total_turns_for_lesson(lesson_slug)
        now = datetime.utcnow()
        session_model = ConversationSessionModel(
            id=f"session-{uuid4().hex[:10]}",
            user_id=user_id,
            demo_user_id=demo_user_id,
            language_code=language_code,
            level_code=level_code,
            mode=mode,
            scenario_key=scenario_key,
            lesson_slug=lesson_slug,
            status="started",
            created_at=now,
            updated_at=now,
        )
        self.db.add(session_model)
        self.db.flush()
        self._upsert_progress(session_model=session_model, completed_turns=0, last_score=0)
        self.db.commit()
        return self._model_to_domain(session_model)

    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        model = self._get_session_model(session_id)
        if model is None:
            return None
        return self._model_to_domain(model)

    def add_turn(
        self,
        session_id: str,
        transcript: str,
        transcription: Optional[TurnTranscription] = None,
        feedback: Optional[CoachFeedback] = None,
    ) -> tuple[ConversationSession, ConversationTurn]:
        session_model = self._get_session_model(session_id)
        if session_model is None:
            raise KeyError(session_id)

        total_turns = total_turns_for_lesson(session_model.lesson_slug)
        if len(session_model.turns) >= total_turns:
            raise ValueError("conversation_session_completed")

        now = datetime.utcnow()
        turn_index = len(session_model.turns)
        next_turn_index = turn_index + 1
        if feedback is None:
            feedback = evaluate_answer(
                transcript,
                turn_index,
                lesson_slug=session_model.lesson_slug,
            )
        learner_name = learner_name_from_transcripts(
            [turn.user_transcript for turn in session_model.turns] + [transcript]
        )
        feedback = personalize_feedback(feedback, learner_name)
        turn_model = ConversationTurnModel(
            id=f"turn-{uuid4().hex[:10]}",
            session_id=session_model.id,
            turn_index=turn_index,
            user_transcript=transcript.strip(),
            coach_reply=personalize_learner_name(
                coach_reply_for_turn(session_model.lesson_slug, next_turn_index),
                learner_name,
            ),
            minutes_consumed=1,
            input_source=transcription.input_source if transcription else "typed",
            stt_provider=transcription.provider if transcription else None,
            stt_model=transcription.model if transcription else None,
            stt_transcript_id=transcription.transcript_id if transcription else None,
            stt_confidence=transcription.confidence if transcription else None,
            stt_audio_duration_seconds=(
                transcription.audio_duration_seconds if transcription else None
            ),
            stt_metadata_json=transcription.metadata if transcription else None,
            created_at=now,
        )
        feedback_model = ConversationFeedbackModel(
            turn_id=turn_model.id,
            better_version=feedback.better_version,
            indonesian_explanation=feedback.indonesian_explanation,
            scores=feedback.scores,
            next_practice=[feedback.next_practice],
            created_at=now,
        )
        turn_model.feedback = feedback_model
        session_model.turns.append(turn_model)
        session_model.updated_at = now
        session_model.status = "completed" if len(session_model.turns) >= total_turns else "in_progress"
        self._upsert_progress(
            session_model=session_model,
            completed_turns=len(session_model.turns),
            last_score=feedback.average_score,
        )
        self.db.commit()

        session = self._model_to_domain(session_model)
        return session, session.turns[-1]

    def latest_session_for_user(
        self,
        demo_user_id: str,
        user_id: Optional[str] = None,
        lesson_slug: str = DEFAULT_LESSON_SLUG,
    ) -> Optional[ConversationSession]:
        progress_filters = [PracticeProgressModel.lesson_slug == lesson_slug]
        session_filters = [ConversationSessionModel.lesson_slug == lesson_slug]
        if user_id:
            progress_filters.append(PracticeProgressModel.user_id == user_id)
            session_filters.append(ConversationSessionModel.user_id == user_id)
        else:
            progress_filters.append(PracticeProgressModel.demo_user_id == demo_user_id)
            session_filters.append(ConversationSessionModel.demo_user_id == demo_user_id)

        progress = self.db.execute(
            select(PracticeProgressModel).where(*progress_filters)
        ).scalar_one_or_none()

        if progress is not None:
            return self.get_session(progress.latest_session_id)

        model = self.db.execute(
            select(ConversationSessionModel)
            .where(*session_filters)
            .order_by(ConversationSessionModel.updated_at.desc())
            .limit(1)
            .options(
                selectinload(ConversationSessionModel.turns).selectinload(
                    ConversationTurnModel.feedback
                )
            )
        ).scalar_one_or_none()
        return self._model_to_domain(model) if model else None

    def reset_latest_for_user(
        self,
        demo_user_id: str,
        user_id: Optional[str] = None,
        lesson_slug: str = DEFAULT_LESSON_SLUG,
    ) -> bool:
        session = self.latest_session_for_user(
            demo_user_id=demo_user_id,
            user_id=user_id,
            lesson_slug=lesson_slug,
        )
        if session is None:
            return False

        progress_filters = [PracticeProgressModel.lesson_slug == lesson_slug]
        if user_id:
            progress_filters.append(PracticeProgressModel.user_id == user_id)
        else:
            progress_filters.append(PracticeProgressModel.demo_user_id == demo_user_id)

        progress = self.db.execute(
            select(PracticeProgressModel).where(*progress_filters)
        ).scalar_one_or_none()
        if progress is not None:
            self.db.delete(progress)

        session_model = self._get_session_model(session.id)
        if session_model is not None:
            self.db.delete(session_model)

        self.db.commit()
        return True

    def _get_session_model(self, session_id: str) -> Optional[ConversationSessionModel]:
        return self.db.execute(
            select(ConversationSessionModel)
            .where(ConversationSessionModel.id == session_id)
            .options(
                selectinload(ConversationSessionModel.turns).selectinload(
                    ConversationTurnModel.feedback
                )
            )
        ).scalar_one_or_none()

    def _upsert_progress(
        self,
        session_model: ConversationSessionModel,
        completed_turns: int,
        last_score: int,
    ) -> None:
        progress = self.db.execute(
            select(PracticeProgressModel).where(
                PracticeProgressModel.demo_user_id == session_model.demo_user_id,
                PracticeProgressModel.lesson_slug == session_model.lesson_slug,
            )
        ).scalar_one_or_none()

        total_turns = total_turns_for_lesson(session_model.lesson_slug)
        completed = completed_turns >= total_turns
        if progress is None:
            progress = PracticeProgressModel(
                user_id=session_model.user_id,
                demo_user_id=session_model.demo_user_id,
                lesson_slug=session_model.lesson_slug,
                latest_session_id=session_model.id,
                completed_turns=completed_turns,
                total_turns=total_turns,
                completed=completed,
                last_score=last_score,
                updated_at=session_model.updated_at,
            )
            self.db.add(progress)
            return

        progress.latest_session_id = session_model.id
        progress.user_id = session_model.user_id
        progress.completed_turns = completed_turns
        progress.total_turns = total_turns
        progress.completed = completed
        progress.last_score = last_score
        progress.updated_at = session_model.updated_at

    def _model_to_domain(self, model: ConversationSessionModel) -> ConversationSession:
        return ConversationSession(
            id=model.id,
            user_id=model.user_id,
            demo_user_id=model.demo_user_id,
            language_code=model.language_code,
            level_code=model.level_code,
            mode=model.mode,
            scenario_key=model.scenario_key,
            lesson_slug=model.lesson_slug,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
            turns=[
                ConversationTurn(
                    id=turn.id,
                    turn_index=turn.turn_index,
                    user_transcript=turn.user_transcript,
                    coach_reply=turn.coach_reply,
                    feedback=CoachFeedback(
                        better_version=turn.feedback.better_version,
                        indonesian_explanation=turn.feedback.indonesian_explanation,
                        next_practice=turn.feedback.next_practice[0],
                        scores=turn.feedback.scores,
                    ),
                    minutes_consumed=turn.minutes_consumed,
                    created_at=turn.created_at,
                    transcription=(
                        TurnTranscription(
                            input_source=turn.input_source,
                            provider=turn.stt_provider or "",
                            model=turn.stt_model or "",
                            transcript_id=turn.stt_transcript_id or "",
                            confidence=turn.stt_confidence,
                            audio_duration_seconds=turn.stt_audio_duration_seconds,
                            metadata=turn.stt_metadata_json or {},
                        )
                        if turn.input_source == "audio" and turn.stt_provider
                        else None
                    ),
                )
                for turn in model.turns
            ],
        )
