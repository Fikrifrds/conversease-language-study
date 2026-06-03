from __future__ import annotations

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
class ConversationTurn:
    id: str
    turn_index: int
    user_transcript: str
    coach_reply: Optional[str]
    feedback: CoachFeedback
    minutes_consumed: int
    created_at: datetime


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


ROLEPLAY_SCRIPTS: dict[str, tuple[CoachTurn, ...]] = {
    "saying-hello-and-goodbye": (
        CoachTurn(
            coach="Hi. Good morning. How are you today?",
            hint="Jawab sapaan, lalu beri respons singkat.",
            sample_answer="Good morning. I'm good, thank you. How are you?",
            focus="Greeting response",
            expected_keywords=("good morning", "morning", "hi", "hello", "thank", "thanks"),
            indonesian_explanation=(
                "Jawabanmu sudah masuk konteks. Akan lebih natural kalau menambahkan pertanyaan balik singkat."
            ),
        ),
        CoachTurn(
            coach="Nice. What is your name?",
            hint="Sebutkan nama dengan pola: My name is ... atau I'm ...",
            sample_answer="My name is Fikri. Nice to meet you.",
            focus="Self introduction",
            expected_keywords=("my name is", "i'm", "i am", "nice to meet"),
            indonesian_explanation=(
                "Untuk perkenalan, pola 'My name is ...' atau 'I'm ...' sudah cukup. Tambahkan 'Nice to meet you' agar lebih ramah."
            ),
        ),
        CoachTurn(
            coach="Nice to meet you. Where are you from?",
            hint="Jawab asalmu, lalu tambahkan pertanyaan balik sederhana.",
            sample_answer="I'm from Indonesia. How about you?",
            focus="Follow-up question",
            expected_keywords=("from", "indonesia", "jakarta", "how about you", "?"),
            indonesian_explanation=(
                "Saat menjawab asal, tambahkan pertanyaan balik seperti 'How about you?' supaya percakapan terus berjalan."
            ),
        ),
    ),
    "saying-your-name": (
        CoachTurn(
            coach="Hi, my name is Sara. What is your name?",
            hint="Jawab dengan pola: My name is ... atau I'm ...",
            sample_answer="My name is Fikri. Nice to meet you.",
            focus="Saying your name",
            expected_keywords=("my name is", "i'm", "i am", "nice to meet"),
            indonesian_explanation=(
                "Sebutkan nama dengan satu kalimat jelas, lalu tambahkan respons ramah seperti 'Nice to meet you'."
            ),
        ),
        CoachTurn(
            coach="Nice to meet you. What should I call you?",
            hint="Gunakan pola: Please call me ...",
            sample_answer="Please call me Fikri.",
            focus="Nickname",
            expected_keywords=("please call me", "call me"),
            indonesian_explanation=(
                "Kalau ingin menyebut nama panggilan, gunakan pola pendek 'Please call me ...'."
            ),
        ),
        CoachTurn(
            coach="Great. Nice to meet you, Fikri.",
            hint="Balas dengan sopan: Nice to meet you too.",
            sample_answer="Nice to meet you too.",
            focus="Polite response",
            expected_keywords=("nice to meet you too", "you too"),
            indonesian_explanation=(
                "Untuk membalas sapaan perkenalan, 'Nice to meet you too' sudah natural dan sopan."
            ),
        ),
    ),
    "asking-someones-name": (
        CoachTurn(
            coach="Hi. I am new here.",
            hint="Tanyakan nama dengan: What's your name?",
            sample_answer="Hi. What's your name?",
            focus="Asking a name",
            expected_keywords=("what's your name", "what is your name", "may i know your name", "?"),
            indonesian_explanation=(
                "Tanyakan nama dengan pertanyaan sederhana. 'What's your name?' cukup untuk konteks santai."
            ),
        ),
        CoachTurn(
            coach="My name is Mina.",
            hint="Ulangi nama orang itu dalam responsmu.",
            sample_answer="Nice to meet you, Mina.",
            focus="Using the name",
            expected_keywords=("nice to meet you", "mina"),
            indonesian_explanation=(
                "Mengulang nama lawan bicara membuat responsmu terdengar lebih perhatian."
            ),
        ),
        CoachTurn(
            coach="Nice to meet you too.",
            hint="Tutup dengan respons singkat yang natural.",
            sample_answer="See you later.",
            focus="Closing",
            expected_keywords=("see you", "later", "bye"),
            indonesian_explanation=(
                "Gunakan closing sederhana seperti 'See you later' agar percakapan selesai dengan sopan."
            ),
        ),
    ),
    "saying-where-you-are-from": (
        CoachTurn(
            coach="Where are you from?",
            hint="Jawab dengan pola: I'm from ...",
            sample_answer="I'm from Indonesia.",
            focus="Origin",
            expected_keywords=("from", "indonesia", "jakarta", "bandung", "surabaya"),
            indonesian_explanation=(
                "Untuk asal negara atau kota, gunakan pola 'I'm from ...' dengan singkat dan jelas."
            ),
        ),
        CoachTurn(
            coach="Where do you live now?",
            hint="Gunakan pola: I live in ...",
            sample_answer="I live in Jakarta.",
            focus="Current city",
            expected_keywords=("live in", "jakarta", "bandung", "surabaya"),
            indonesian_explanation=(
                "Bedakan origin dan tempat tinggal sekarang: 'I'm from ...' dan 'I live in ...'."
            ),
        ),
        CoachTurn(
            coach="Nice. Ask me the same question.",
            hint="Tanyakan balik dengan: How about you?",
            sample_answer="How about you?",
            focus="Question back",
            expected_keywords=("how about you", "where are you from", "?"),
            indonesian_explanation=(
                "Pertanyaan balik seperti 'How about you?' menjaga percakapan tetap berjalan."
            ),
        ),
    ),
    "first-conversation-mission": (
        CoachTurn(
            coach="Hi, good morning. My name is Sara.",
            hint="Sapa balik dan sebutkan namamu.",
            sample_answer="Good morning. My name is Fikri.",
            focus="Greeting and name",
            expected_keywords=("good morning", "my name is", "i'm", "i am"),
            indonesian_explanation=(
                "Gabungkan greeting dan nama dalam dua kalimat pendek agar pembuka percakapan terasa jelas."
            ),
        ),
        CoachTurn(
            coach="Nice to meet you. Where are you from?",
            hint="Jawab asalmu lalu tanyakan balik.",
            sample_answer="I'm from Indonesia. How about you?",
            focus="Origin and follow-up",
            expected_keywords=("from", "indonesia", "how about you", "?"),
            indonesian_explanation=(
                "Setelah menjawab asal, tanyakan balik supaya percakapan tidak berhenti."
            ),
        ),
        CoachTurn(
            coach="I'm from Malaysia. Nice to meet you.",
            hint="Balas dan tutup percakapan.",
            sample_answer="Nice to meet you too. See you later.",
            focus="Closing mission",
            expected_keywords=("nice to meet you too", "see you", "later"),
            indonesian_explanation=(
                "Tutup misi dengan respons sopan dan closing singkat seperti 'See you later'."
            ),
        ),
    ),
}


COACH_TURNS = ROLEPLAY_SCRIPTS[DEFAULT_LESSON_SLUG]


def roleplay_turns_for_lesson(lesson_slug: str) -> tuple[CoachTurn, ...]:
    return ROLEPLAY_SCRIPTS.get(lesson_slug, COACH_TURNS)


def total_turns_for_lesson(lesson_slug: str) -> int:
    return len(roleplay_turns_for_lesson(lesson_slug))


def first_coach_message(lesson_slug: str) -> str:
    return roleplay_turns_for_lesson(lesson_slug)[0].coach


def coach_reply_for_turn(lesson_slug: str, turn_index: int) -> Optional[str]:
    turns = roleplay_turns_for_lesson(lesson_slug)
    return turns[turn_index].coach if turn_index < len(turns) else None


def clamp_score(score: int) -> int:
    return max(55, min(score, 95))


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
    keyword_hits = sum(1 for keyword in active_turn.expected_keywords if keyword in normalized)
    has_question = "?" in normalized
    enough_words = len([word for word in text.split() if word]) >= 5

    speaking = 64
    grammar = 66
    fluency = 64

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
        indonesian_explanation=active_turn.indonesian_explanation
        or f"Jawabanmu sudah masuk konteks. Latih pola ini agar lebih natural: {active_turn.sample_answer}",
        next_practice=next_practice,
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

    def add_turn(self, session_id: str, transcript: str) -> ConversationTurn:
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
    }
