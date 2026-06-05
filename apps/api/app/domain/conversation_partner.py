from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple


@dataclass(frozen=True)
class PartnerTopic:
    key: str
    level_code: str
    title: str
    description: str
    partner_role: str
    partner_name: str
    goals: Tuple[str, ...]
    target_phrases: Tuple[str, ...]
    opening_line: str
    max_turns: int = 8


# Difficulty profiles steer the LLM's language complexity per CEFR level.
# Keep a single conversation engine; only the system-prompt guidance changes.
DIFFICULTY_PROFILES: Dict[str, str] = {
    "A1": (
        "Speak like talking to a beginner. Use very short sentences (3-8 words), "
        "present simple tense, and the most common ~500 words. One idea per reply. "
        "Avoid idioms, contractions are fine. Be warm and slow."
    ),
    "A2": (
        "Use short, simple sentences with everyday vocabulary. Present and simple past "
        "are fine. Keep replies to 1-2 sentences. Avoid idioms and complex clauses."
    ),
    "B1": (
        "Use clear, everyday English with some connected sentences. You may use common "
        "phrasal verbs and simple opinions. Keep replies to 2-3 sentences."
    ),
    "B2": (
        "Speak naturally with varied vocabulary, some idioms, and connected reasoning. "
        "You may ask follow-up questions and express nuance. Keep replies concise."
    ),
    "C1": (
        "Speak at a natural native pace with rich vocabulary, idioms, and abstract ideas. "
        "Challenge the learner with nuanced questions while staying on topic."
    ),
}

DEFAULT_LEVEL = "A1"


# Batch pertama: topik A1. Struktur siap untuk level lain (tinggal tambah entry).
PARTNER_TOPICS: Tuple[PartnerTopic, ...] = (
    PartnerTopic(
        key="order-a-drink",
        level_code="A1",
        title="Order a Drink",
        description="Pesan minuman di cafe, pilih ukuran, dan bayar.",
        partner_role="a friendly cafe barista",
        partner_name="Mina",
        goals=(
            "greet the barista",
            "order a drink",
            "answer the size question",
            "pay and say thank you",
        ),
        target_phrases=(
            "can I have",
            "I would like",
            "small",
            "large",
            "thank you",
        ),
        opening_line="Hi! Welcome to the cafe. What can I get you today?",
        max_turns=8,
    ),
    PartnerTopic(
        key="meet-a-new-friend",
        level_code="A1",
        title="Meet a New Friend",
        description="Berkenalan: sapaan, nama, asal, dan tanya balik.",
        partner_role="a friendly classmate in an English class",
        partner_name="Sara",
        goals=(
            "greet back",
            "say your name",
            "say where you are from",
            "ask the partner a question back",
        ),
        target_phrases=(
            "my name is",
            "i am from",
            "nice to meet you",
            "how about you",
        ),
        opening_line="Hi! Good morning. My name is Sara. What is your name?",
        max_turns=8,
    ),
    PartnerTopic(
        key="ask-for-directions",
        level_code="A1",
        title="Ask for Directions",
        description="Tanya lokasi tempat dan ikuti arahan sederhana.",
        partner_role="a helpful local person on the street",
        partner_name="Ben",
        goals=(
            "ask where a place is",
            "understand a simple direction",
            "confirm the direction",
            "say thank you",
        ),
        target_phrases=(
            "where is",
            "how do I get to",
            "go straight",
            "turn left",
            "turn right",
            "thank you",
        ),
        opening_line="Hello! You look a bit lost. Do you need any help?",
        max_turns=8,
    ),
    PartnerTopic(
        key="talk-about-your-day",
        level_code="A1",
        title="Talk About Your Day",
        description="Cerita rutinitas harian sederhana dan waktunya.",
        partner_role="a friendly coworker chatting during a break",
        partner_name="Lina",
        goals=(
            "say one morning activity",
            "say a time",
            "say one more activity",
            "ask the partner about their day",
        ),
        target_phrases=(
            "I wake up",
            "I study",
            "I work",
            "in the morning",
            "o'clock",
        ),
        opening_line="Hey! How is your day going so far?",
        max_turns=8,
    ),
)


def difficulty_profile(level_code: str) -> str:
    return DIFFICULTY_PROFILES.get(level_code.upper(), DIFFICULTY_PROFILES[DEFAULT_LEVEL])


def topics_for_level(level_code: str) -> Tuple[PartnerTopic, ...]:
    normalized = level_code.upper()
    return tuple(topic for topic in PARTNER_TOPICS if topic.level_code == normalized)


def get_topic(topic_key: str) -> Optional[PartnerTopic]:
    for topic in PARTNER_TOPICS:
        if topic.key == topic_key:
            return topic
    return None


def topic_payload(topic: PartnerTopic) -> Dict[str, object]:
    return {
        "key": topic.key,
        "level_code": topic.level_code,
        "title": topic.title,
        "description": topic.description,
        "partner_role": topic.partner_role,
        "partner_name": topic.partner_name,
        "goals": list(topic.goals),
        "opening_line": topic.opening_line,
        "max_turns": topic.max_turns,
    }
