from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4


@dataclass(frozen=True)
class CoachTurn:
    coach: str
    hint: str
    sample_answer: str
    focus: str
    expected_keywords: tuple[str, ...] = ()
    indonesian_explanation: str = ""


@dataclass(frozen=True)
class CoachFeedback:
    better_version: str
    indonesian_explanation: str
    next_practice: str
    scores: Dict[str, int]

    @property
    def average_score(self) -> int:
        values = [self.scores["speaking"], self.scores["grammar"], self.scores["fluency"]]
        return round(sum(values) / len(values))


@dataclass(frozen=True)
class TurnTranscription:
    input_source: str
    provider: str
    model: str
    transcript_id: str
    confidence: Optional[float] = None
    audio_duration_seconds: Optional[float] = None
    metadata: Dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class ConversationTurn:
    id: str
    turn_index: int
    user_transcript: str
    coach_reply: Optional[str]
    feedback: CoachFeedback
    minutes_consumed: int
    created_at: datetime
    transcription: Optional[TurnTranscription] = None


@dataclass
class ConversationSession:
    id: str
    user_id: Optional[str]
    demo_user_id: str
    language_code: str
    level_code: str
    mode: str
    scenario_key: str
    lesson_slug: str
    status: str
    created_at: datetime
    updated_at: datetime
    turns: List[ConversationTurn] = field(default_factory=list)

    @property
    def completed_turns(self) -> int:
        return len(self.turns)

    @property
    def completed(self) -> bool:
        return self.completed_turns >= total_turns_for_lesson(self.lesson_slug)

    @property
    def last_score(self) -> int:
        if not self.turns:
            return 0
        return self.turns[-1].feedback.average_score


DEFAULT_LESSON_SLUG = "saying-hello-and-goodbye"


try:
    from app.domain.generated_roleplay_scripts import GENERATED_ROLEPLAY_SCRIPTS
except Exception:
    GENERATED_ROLEPLAY_SCRIPTS = {}

ROLEPLAY_SCRIPTS: dict[str, tuple[CoachTurn, ...]] = {
    lesson_slug: tuple(
        CoachTurn(
            coach=turn.coach,
            hint=turn.hint,
            sample_answer=turn.sample_answer,
            focus=turn.focus,
            expected_keywords=tuple(turn.expected_keywords),
            indonesian_explanation=turn.indonesian_explanation,
        )
        for turn in turns
    )
    for lesson_slug, turns in GENERATED_ROLEPLAY_SCRIPTS.items()
}

if DEFAULT_LESSON_SLUG not in ROLEPLAY_SCRIPTS:
    raise RuntimeError(f"Default conversation roleplay slug is missing: {DEFAULT_LESSON_SLUG}")


class UnknownLessonSlugError(ValueError):
    pass


def roleplay_turns_for_lesson(lesson_slug: str) -> tuple[CoachTurn, ...]:
    turns = ROLEPLAY_SCRIPTS.get(lesson_slug)
    if turns is None:
        raise UnknownLessonSlugError(f"unknown_lesson_slug:{lesson_slug}")
    return turns


def total_turns_for_lesson(lesson_slug: str) -> int:
    return len(roleplay_turns_for_lesson(lesson_slug))


def first_coach_message(lesson_slug: str) -> str:
    return roleplay_turns_for_lesson(lesson_slug)[0].coach


def coach_reply_for_turn(lesson_slug: str, turn_index: int) -> Optional[str]:
    turns = roleplay_turns_for_lesson(lesson_slug)
    return turns[turn_index].coach if turn_index < len(turns) else None


def clamp_score(score: int) -> int:
    return max(55, min(score, 95))


def _looks_like_refusal(normalized: str) -> bool:
    cleaned = re.sub(r"[^a-z\s]", " ", normalized).strip()
    if not cleaned:
        return True
    tokens = [token for token in cleaned.split() if token]
    if not tokens:
        return True
    if len(tokens) <= 2 and all(token in {"no", "nope", "nah"} for token in tokens):
        return True
    if len(tokens) <= 2 and tokens[0] == "sorry":
        return True
    return False


def evaluate_answer(
    answer: str,
    turn_index: int,
    lesson_slug: str = DEFAULT_LESSON_SLUG,
) -> CoachFeedback:
    text = answer.strip()
    normalized = text.lower()
    active_turns = roleplay_turns_for_lesson(lesson_slug)
    safe_turn_index = min(turn_index, len(active_turns) - 1)
    active_turn = active_turns[safe_turn_index]
    expects_question = "?" in active_turn.expected_keywords
    keyword_hits = sum(1 for keyword in active_turn.expected_keywords if keyword != "?" and keyword in normalized)
    has_question = "?" in normalized
    enough_words = len([word for word in text.split() if word]) >= 5
    match_hits = keyword_hits + (1 if expects_question and has_question else 0)
    expected_total = sum(1 for keyword in active_turn.expected_keywords if keyword and keyword != "?") + (1 if expects_question else 0)
    off_track = expected_total > 0 and (match_hits == 0 or _looks_like_refusal(normalized))

    speaking = 58 if off_track else 64
    grammar = 56 if off_track else 66
    fluency = 55 if off_track else 64

    if enough_words:
        speaking += 8
        fluency += 8

    if keyword_hits:
        speaking += 12 + max(0, keyword_hits - 1) * 3
        grammar += 8
        fluency += min(keyword_hits, 2) * 3

    if has_question:
        speaking += 5
        fluency += 8

    next_practice = (
        "Ulangi roleplay dari awal tanpa melihat contoh jawaban."
        if safe_turn_index >= len(active_turns) - 1
        else f"Next: {active_turns[safe_turn_index + 1].focus}"
    )

    return CoachFeedback(
        better_version=active_turn.sample_answer,
        indonesian_explanation=(
            f"Jawabanmu belum menjawab pertanyaan ini. Coba jawab seperti: {active_turn.sample_answer}"
            if off_track
            else (
                active_turn.indonesian_explanation
                or f"Jawabanmu sudah masuk konteks. Latih pola ini agar lebih natural: {active_turn.sample_answer}"
            )
        ),
        next_practice=(
            f"Ulangi turn ini dan jawab sesuai fokus: {active_turn.focus}."
            if off_track
            else next_practice
        ),
        scores={
            "speaking": clamp_score(speaking),
            "grammar": clamp_score(grammar),
            "fluency": clamp_score(fluency),
        },
    )


class ConversationPracticeStore:
    def __init__(self) -> None:
        self.sessions: Dict[str, ConversationSession] = {}

    def create_session(
        self,
        demo_user_id: str,
        language_code: str = "en",
        level_code: str = "A1",
        mode: str = "lesson_practice_coach",
        scenario_key: str = "greeting_intro",
        lesson_slug: str = DEFAULT_LESSON_SLUG,
    ) -> ConversationSession:
        roleplay_turns_for_lesson(lesson_slug)
        now = datetime.utcnow()
        session = ConversationSession(
            id=f"session-{uuid4().hex[:10]}",
            user_id=None,
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
        self.sessions[session.id] = session
        return session

    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        return self.sessions.get(session_id)

    def add_turn(
        self,
        session_id: str,
        transcript: str,
        transcription: Optional[TurnTranscription] = None,
    ) -> ConversationTurn:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError(session_id)

        if session.completed:
            raise ValueError("conversation_session_completed")

        now = datetime.utcnow()
        turn_index = session.completed_turns
        next_turn_index = turn_index + 1
        feedback = evaluate_answer(transcript, turn_index, lesson_slug=session.lesson_slug)
        coach_reply = coach_reply_for_turn(session.lesson_slug, next_turn_index)
        turn = ConversationTurn(
            id=f"turn-{uuid4().hex[:10]}",
            turn_index=turn_index,
            user_transcript=transcript.strip(),
            coach_reply=coach_reply,
            feedback=feedback,
            minutes_consumed=1,
            created_at=now,
            transcription=transcription,
        )
        session.turns.append(turn)
        session.updated_at = now
        session.status = "completed" if session.completed else "in_progress"
        return turn

    def latest_session_for_user(
        self,
        demo_user_id: str,
        lesson_slug: str = DEFAULT_LESSON_SLUG,
    ) -> Optional[ConversationSession]:
        candidates = [
            session
            for session in self.sessions.values()
            if session.demo_user_id == demo_user_id and session.lesson_slug == lesson_slug
        ]
        if not candidates:
            return None
        return max(candidates, key=lambda session: session.updated_at)

    def reset_latest_for_user(
        self,
        demo_user_id: str,
        lesson_slug: str = DEFAULT_LESSON_SLUG,
    ) -> bool:
        session = self.latest_session_for_user(demo_user_id, lesson_slug)
        if session is None:
            return False
        del self.sessions[session.id]
        return True


def session_summary(session: ConversationSession) -> Dict[str, object]:
    return {
        "session_id": session.id,
        "lesson_slug": session.lesson_slug,
        "completed_turns": session.completed_turns,
        "total_turns": total_turns_for_lesson(session.lesson_slug),
        "completed": session.completed,
        "last_score": session.last_score,
        "updated_at": session.updated_at.isoformat() + "Z",
    }


def session_payload(session: ConversationSession) -> Dict[str, object]:
    return {
        "id": session.id,
        "user_id": session.user_id,
        "demo_user_id": session.demo_user_id,
        "language_code": session.language_code,
        "level_code": session.level_code,
        "mode": session.mode,
        "scenario_key": session.scenario_key,
        "lesson_slug": session.lesson_slug,
        "status": session.status,
        "first_coach_message": first_coach_message(session.lesson_slug),
        "completed_turns": session.completed_turns,
        "total_turns": total_turns_for_lesson(session.lesson_slug),
        "completed": session.completed,
        "updated_at": session.updated_at.isoformat() + "Z",
    }


def turn_payload(session: ConversationSession, turn: ConversationTurn) -> Dict[str, object]:
    return {
        "session_id": session.id,
        "turn_id": turn.id,
        "turn_index": turn.turn_index,
        "user_transcript": turn.user_transcript,
        "conversation_coach_reply": turn.coach_reply,
        "completed_turns": session.completed_turns,
        "total_turns": total_turns_for_lesson(session.lesson_slug),
        "completed": session.completed,
        "last_score": session.last_score,
        "updated_at": session.updated_at.isoformat() + "Z",
        "feedback": {
            "better_version": turn.feedback.better_version,
            "indonesian_explanation": turn.feedback.indonesian_explanation,
            "scores": turn.feedback.scores,
            "next_practice": [turn.feedback.next_practice],
        },
        "minutes_consumed": turn.minutes_consumed,
        "transcription": transcription_payload(turn.transcription),
    }


def transcription_payload(transcription: Optional[TurnTranscription]) -> Optional[Dict[str, object]]:
    if transcription is None:
        return None
    return {
        "input_source": transcription.input_source,
        "provider": transcription.provider,
        "model": transcription.model,
        "transcript_id": transcription.transcript_id,
        "confidence": transcription.confidence,
        "audio_duration_seconds": transcription.audio_duration_seconds,
        "metadata": transcription.metadata,
    }
