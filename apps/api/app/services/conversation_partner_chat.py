from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

from app.domain.ai import TASK_MODEL_CONFIGS, ChatMessage, LLMProvider
from app.domain.conversation_partner import PartnerTopic, difficulty_profile
from app.domain.conversation_practice import clamp_score
from app.services.llm import LLMError, get_llm_provider

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PartnerReply:
    reply: str
    on_topic: bool
    should_end: bool


@dataclass(frozen=True)
class PartnerSummary:
    summary: str
    indonesian_explanation: str
    scores: dict


REPLY_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "reply": {"type": "string"},
        "on_topic": {"type": "boolean"},
        "should_end": {"type": "boolean"},
    },
    "required": ["reply", "on_topic", "should_end"],
}

SUMMARY_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "indonesian_explanation": {"type": "string"},
        "scores": {
            "type": "object",
            "properties": {
                "speaking": {"type": "integer"},
                "grammar": {"type": "integer"},
                "fluency": {"type": "integer"},
            },
            "required": ["speaking", "grammar", "fluency"],
        },
    },
    "required": ["summary", "indonesian_explanation", "scores"],
}


async def generate_partner_reply(
    *,
    topic: PartnerTopic,
    level_code: str,
    history: Sequence[Tuple[str, str]],
    user_message: str,
    completed_turns: int,
    provider: Optional[LLMProvider] = None,
) -> PartnerReply:
    """Generate the partner's next spoken reply, staying on topic and on level.

    `history` is a sequence of (role, text) where role is "partner" or "user".
    Falls back to a safe, on-topic nudge when the LLM is unavailable so a paid
    turn is never blocked.
    """
    turns_left = max(0, topic.max_turns - (completed_turns + 1))
    fallback = _fallback_reply(topic=topic, turns_left=turns_left)

    active_provider = provider or get_llm_provider()
    if active_provider is None:
        return fallback

    messages = [
        ChatMessage(role="system", content=_reply_system_prompt(topic, level_code, turns_left)),
        *_history_messages(history),
        ChatMessage(role="user", content=user_message.strip()),
    ]

    try:
        result = await active_provider.generate_chat_completion(
            messages=messages,
            model_config=TASK_MODEL_CONFIGS["conversation_partner_reply"],
            response_schema=REPLY_RESPONSE_SCHEMA,
        )
        return _parse_reply(result.content, fallback=fallback, turns_left=turns_left)
    except LLMError as exc:
        logger.warning(
            "partner_reply_llm_failed topic=%s level=%s: %s",
            topic.key,
            level_code,
            exc,
        )
        return fallback
    except Exception as exc:  # never break a paid turn
        logger.error(
            "partner_reply_unexpected_error topic=%s level=%s: %s", topic.key, level_code, exc
        )
        return fallback


async def summarize_session(
    *,
    topic: PartnerTopic,
    level_code: str,
    history: Sequence[Tuple[str, str]],
    provider: Optional[LLMProvider] = None,
) -> PartnerSummary:
    fallback = PartnerSummary(
        summary="Great practice! You completed the conversation.",
        indonesian_explanation=(
            "Latihan selesai. Terus ulangi topik ini agar percakapanmu makin lancar."
        ),
        scores={"speaking": 70, "grammar": 68, "fluency": 70},
    )

    active_provider = provider or get_llm_provider()
    if active_provider is None:
        return fallback

    transcript = _render_transcript(history)
    messages = [
        ChatMessage(role="system", content=_summary_system_prompt()),
        ChatMessage(
            role="user",
            content=(
                f"Topic: {topic.title}\n"
                f"Learner level: {level_code}\n"
                f"Goals: {', '.join(topic.goals)}\n\n"
                f"Conversation transcript:\n{transcript}\n\n"
                "Evaluate the learner's English and return the JSON summary."
            ),
        ),
    ]

    try:
        result = await active_provider.generate_chat_completion(
            messages=messages,
            model_config=TASK_MODEL_CONFIGS["conversation_partner_summary"],
            response_schema=SUMMARY_RESPONSE_SCHEMA,
        )
        return _parse_summary(result.content, fallback=fallback)
    except LLMError as exc:
        logger.error("partner_summary_llm_failed topic=%s: %s", topic.key, exc)
        return fallback
    except Exception as exc:
        logger.error("partner_summary_unexpected_error topic=%s: %s", topic.key, exc)
        return fallback


def _reply_system_prompt(topic: PartnerTopic, level_code: str, turns_left: int) -> str:
    goals = "; ".join(topic.goals)
    phrases = ", ".join(topic.target_phrases)
    return (
        f"You are an AI conversation partner playing the role of {topic.partner_role}. "
        "You are having a short spoken role-play conversation with an Indonesian English "
        "learner to help them practice.\n"
        f"LEARNER LEVEL: {level_code}. {difficulty_profile(level_code)}\n"
        f"CONVERSATION TOPIC: {topic.title} - {topic.description}\n"
        f"GOALS the learner should reach: {goals}.\n"
        f"Helpful target phrases the learner may use: {phrases}.\n\n"
        "RULES:\n"
        "- React to what the learner just said, then ask ONE simple follow-up question to keep "
        "them talking. You are guiding the learner to speak, not narrating your own life. Do not "
        "list your own activities unless the learner asks you a direct question.\n"
        "- Stay strictly on this topic. If the learner drifts off-topic, gently and briefly "
        "steer back to the topic in role. Never start a new unrelated topic.\n"
        "- Keep your reply natural for the role but matched to the learner's level. One short turn "
        "(1-2 sentences), ending with a question most of the time.\n"
        "- Do not repeat your previous lines and do not just echo the learner's words back.\n"
        "- Do not invent a human name for yourself and do not give meta feedback, grammar "
        "corrections, or notes. Just play the role.\n"
        f"- About {turns_left} exchanges remain. When the goals are reached or no turns remain, "
        "wrap up the conversation politely and set should_end to true.\n"
        "- Set on_topic to false if the learner's last message was off-topic.\n"
        "Respond with JSON only, matching the requested schema."
    )


def _summary_system_prompt() -> str:
    return (
        "You are an English coach for Indonesian learners. Review a short practice "
        "conversation and return concise feedback. Write summary in English (1-2 sentences, "
        "encouraging). Write indonesian_explanation in Bahasa Indonesia (max 2 sentences) with one "
        "concrete tip. Score speaking, grammar, and fluency as integers from 55 to 95. "
        "Respond with JSON only, matching the requested schema."
    )


def _history_messages(history: Sequence[Tuple[str, str]]) -> List[ChatMessage]:
    messages: List[ChatMessage] = []
    for role, text in history:
        llm_role = "assistant" if role == "partner" else "user"
        messages.append(ChatMessage(role=llm_role, content=text))
    return messages


def _render_transcript(history: Sequence[Tuple[str, str]]) -> str:
    lines = []
    for role, text in history:
        speaker = "Partner" if role == "partner" else "Learner"
        lines.append(f"{speaker}: {text}")
    return "\n".join(lines)


def _fallback_reply(*, topic: PartnerTopic, turns_left: int) -> PartnerReply:
    if turns_left <= 0:
        return PartnerReply(
            reply="Thank you for chatting with me. Great practice today!",
            on_topic=True,
            should_end=True,
        )
    return PartnerReply(
        reply=f"Sorry, could you say that again about {topic.title.lower()}?",
        on_topic=True,
        should_end=False,
    )


def _parse_reply(content: str, *, fallback: PartnerReply, turns_left: int) -> PartnerReply:
    try:
        data = json.loads(_extract_json(content))
        raw_reply = (
            data.get("reply")
            or data.get("partner_reply")
            or data.get("partnerReply")
            or data.get("answer")
            or data.get("text")
            or data.get("message")
        )
        reply = str(raw_reply or "").strip()
        if not reply:
            logger.warning(
                "partner_reply_missing_reply keys=%s",
                sorted(list(data.keys())) if isinstance(data, dict) else "n/a",
            )
            return fallback
        should_end = bool(data.get("should_end") if "should_end" in data else data.get("shouldEnd", False)) or turns_left <= 0
        return PartnerReply(
            reply=reply,
            on_topic=bool(data.get("on_topic") if "on_topic" in data else data.get("onTopic", True)),
            should_end=should_end,
        )
    except (ValueError, KeyError, TypeError) as exc:
        logger.error(
            "partner_reply_parse_failed keys=%s: %s",
            sorted(list(data.keys())) if "data" in locals() and isinstance(data, dict) else "n/a",
            exc,
        )
        return fallback


def _parse_summary(content: str, *, fallback: PartnerSummary) -> PartnerSummary:
    try:
        data = json.loads(_extract_json(content))
        raw_scores = (
            data.get("scores")
            or data.get("score")
            or data.get("scoring")
            or (
                {"speaking": data.get("speaking"), "grammar": data.get("grammar"), "fluency": data.get("fluency")}
                if any(key in data for key in ("speaking", "grammar", "fluency"))
                else None
            )
        )
        if not isinstance(raw_scores, dict):
            raw_scores = {}
        scores = raw_scores

        summary = data.get("summary") or data.get("note") or fallback.summary
        indonesian_explanation = (
            data.get("indonesian_explanation")
            or data.get("indonesianExplanation")
            or data.get("explanation_id")
            or data.get("explanationId")
            or fallback.indonesian_explanation
        )
        if not scores:
            logger.warning(
                "partner_summary_missing_scores keys=%s",
                sorted(list(data.keys())) if isinstance(data, dict) else "n/a",
            )
        return PartnerSummary(
            summary=str(summary).strip() or fallback.summary,
            indonesian_explanation=str(indonesian_explanation).strip()
            or fallback.indonesian_explanation,
            scores={
                "speaking": clamp_score(int(scores.get("speaking", fallback.scores["speaking"]))),
                "grammar": clamp_score(int(scores.get("grammar", fallback.scores["grammar"]))),
                "fluency": clamp_score(int(scores.get("fluency", fallback.scores["fluency"]))),
            },
        )
    except (ValueError, KeyError, TypeError) as exc:
        logger.error(
            "partner_summary_parse_failed keys=%s: %s",
            sorted(list(data.keys())) if "data" in locals() and isinstance(data, dict) else "n/a",
            exc,
        )
        return fallback


def _extract_json(content: str) -> str:
    text = content.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("no_json_object")
    return text[start : end + 1]
