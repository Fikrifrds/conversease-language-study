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
        opening_line="Hi! Good morning. I am a new classmate here. What is your name?",
        max_turns=8,
    ),
    PartnerTopic(
        key="ask-for-directions",
        level_code="A1",
        title="Ask for Directions",
        description="Tanya lokasi tempat dan ikuti arahan sederhana.",
        partner_role="a helpful local person on the street",
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
    PartnerTopic(
        key="make-weekend-plans",
        level_code="A2",
        title="Make Weekend Plans",
        description="Ajak teman membuat rencana akhir pekan dan tentukan waktu.",
        partner_role="a friendly friend planning the weekend",
        goals=(
            "suggest an activity",
            "ask about the time",
            "agree or propose another time",
            "confirm the plan",
        ),
        target_phrases=(
            "do you want to",
            "how about",
            "what time",
            "on Saturday",
            "let's",
        ),
        opening_line="Hi! Do you want to do something this weekend?",
        max_turns=9,
    ),
    PartnerTopic(
        key="talk-about-yesterday",
        level_code="A2",
        title="Talk About Yesterday",
        description="Cerita kegiatan kemarin dan tanya balik dengan simple past.",
        partner_role="a classmate catching up after class",
        goals=(
            "say what you did yesterday",
            "give one detail",
            "ask a follow-up question",
            "respond to a follow-up question",
        ),
        target_phrases=(
            "yesterday I",
            "I went to",
            "I watched",
            "after that",
            "what about you",
        ),
        opening_line="Hey! How was your day yesterday?",
        max_turns=9,
    ),
    PartnerTopic(
        key="buy-a-ticket",
        level_code="A2",
        title="Buy a Ticket",
        description="Beli tiket, tanya jam berangkat, dan konfirmasi harga.",
        partner_role="a helpful ticket clerk at a station",
        goals=(
            "say where you want to go",
            "ask about departure time",
            "confirm the price",
            "say thank you and finish",
        ),
        target_phrases=(
            "I want a ticket to",
            "what time does it leave",
            "how much is it",
            "is it",
            "thank you",
        ),
        opening_line="Hello! Where would you like to go today?",
        max_turns=9,
    ),
    PartnerTopic(
        key="work-clarification",
        level_code="B1",
        title="Ask for Clarification at Work",
        description="Minta klarifikasi sopan tentang tugas dan deadline.",
        partner_role="a manager giving you a task",
        goals=(
            "acknowledge the request",
            "ask one clarification question",
            "confirm the deadline",
            "summarize what you will do",
        ),
        target_phrases=(
            "sure",
            "could you clarify",
            "do you mean",
            "by Friday",
            "I'll",
        ),
        opening_line="Hi. Can you help me with a quick task today?",
        max_turns=10,
    ),
    PartnerTopic(
        key="give-your-opinion",
        level_code="B1",
        title="Give Your Opinion",
        description="Sampaikan pendapat sederhana dengan alasan dan tanya balik.",
        partner_role="a colleague discussing a simple idea",
        goals=(
            "share your opinion",
            "give one reason",
            "ask for the partner's opinion",
            "respond politely",
        ),
        target_phrases=(
            "I think",
            "because",
            "in my opinion",
            "what do you think",
            "I agree",
        ),
        opening_line="Hey, I have an idea for our class project. What do you think?",
        max_turns=10,
    ),
    PartnerTopic(
        key="make-a-polite-request",
        level_code="B1",
        title="Make a Polite Request",
        description="Minta bantuan kecil, cek kesediaan, dan ucapkan terima kasih.",
        partner_role="a helpful teammate",
        goals=(
            "make a polite request",
            "give a short reason",
            "offer an alternative time",
            "say thank you",
        ),
        target_phrases=(
            "could you",
            "would you mind",
            "if you have time",
            "can we",
            "thank you",
        ),
        opening_line="Hi! Do you need any help with something today?",
        max_turns=10,
    ),
    PartnerTopic(
        key="run-a-short-meeting",
        level_code="B2",
        title="Run a Short Meeting",
        description="Buka meeting singkat, bahas 2 poin, dan simpulkan next steps.",
        partner_role="a colleague in a short team meeting",
        goals=(
            "set the agenda",
            "discuss one point",
            "discuss a second point",
            "confirm next steps",
        ),
        target_phrases=(
            "today I'd like to",
            "first",
            "second",
            "let's",
            "next steps",
        ),
        opening_line="Hi everyone. We have 10 minutes. What would you like to cover today?",
        max_turns=10,
    ),
    PartnerTopic(
        key="disagree-politely",
        level_code="B2",
        title="Disagree Politely",
        description="Tidak setuju dengan sopan, beri alasan, dan cari jalan tengah.",
        partner_role="a teammate discussing options",
        goals=(
            "state disagreement politely",
            "give a clear reason",
            "offer an alternative",
            "reach a compromise",
        ),
        target_phrases=(
            "I see your point",
            "however",
            "I suggest",
            "what if we",
            "that could work",
        ),
        opening_line="I think we should change the plan. Do you agree?",
        max_turns=10,
    ),
    PartnerTopic(
        key="present-an-idea",
        level_code="B2",
        title="Present an Idea",
        description="Jelaskan ide dengan struktur sederhana dan jawab pertanyaan.",
        partner_role="a supervisor listening to your proposal",
        goals=(
            "introduce your idea",
            "explain one benefit",
            "address one concern",
            "close with a clear ask",
        ),
        target_phrases=(
            "I'd like to propose",
            "the main benefit is",
            "one concern might be",
            "to solve this",
            "would you be open to",
        ),
        opening_line="Hi. You mentioned you have a proposal. Can you walk me through it?",
        max_turns=10,
    ),
    PartnerTopic(
        key="ask-tactful-questions",
        level_code="C1",
        title="Ask Tactful Questions",
        description="Tanya hal sensitif dengan sopan, jelas, dan menjaga hubungan kerja.",
        partner_role="a senior stakeholder in a professional meeting",
        goals=(
            "ask a tactful question",
            "clarify assumptions",
            "confirm constraints",
            "close politely",
        ),
        target_phrases=(
            "would you mind if I ask",
            "to clarify",
            "just to confirm",
            "what are the constraints",
            "thank you for clarifying",
        ),
        opening_line="Thanks for joining. We have a few details to align. What would you like to clarify first?",
        max_turns=11,
    ),
    PartnerTopic(
        key="handle-strong-feedback",
        level_code="C1",
        title="Handle Strong Feedback",
        description="Menanggapi feedback yang tegas dengan tenang dan solutif.",
        partner_role="a direct manager giving critical feedback",
        goals=(
            "acknowledge the feedback",
            "ask for one concrete example",
            "propose a next step",
            "confirm expectations",
        ),
        target_phrases=(
            "I appreciate the feedback",
            "could you give an example",
            "I will",
            "to avoid this",
            "does that meet your expectations",
        ),
        opening_line="I want to be honest: the last update was not clear enough.",
        max_turns=11,
    ),
    PartnerTopic(
        key="negotiate-scope",
        level_code="C1",
        title="Negotiate Scope",
        description="Negosiasi scope dan prioritas tanpa terdengar defensif.",
        partner_role="a client asking for more work",
        goals=(
            "acknowledge the request",
            "ask about priority",
            "offer trade-offs",
            "agree on a clear scope",
        ),
        target_phrases=(
            "I understand",
            "to prioritize",
            "given the timeline",
            "we can either",
            "let's agree on",
        ),
        opening_line="Can you also add a few more features before the deadline?",
        max_turns=11,
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
        "goals": list(topic.goals),
        "opening_line": topic.opening_line,
        "max_turns": topic.max_turns,
    }
