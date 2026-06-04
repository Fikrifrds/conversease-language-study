from __future__ import annotations

import json
import logging
from typing import Optional

from app.domain.ai import TASK_MODEL_CONFIGS, ChatMessage, LLMProvider
from app.domain.conversation_practice import (
    CoachFeedback,
    clamp_score,
    evaluate_answer,
    roleplay_turns_for_lesson,
)
from app.services.llm import LLMError, get_llm_provider

logger = logging.getLogger(__name__)


FEEDBACK_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "better_version": {"type": "string"},
        "indonesian_explanation": {"type": "string"},
        "next_practice": {"type": "string"},
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
    "required": ["better_version", "indonesian_explanation", "next_practice", "scores"],
}


async def generate_conversation_feedback(
    *,
    answer: str,
    turn_index: int,
    lesson_slug: str,
    provider: Optional[LLMProvider] = None,
) -> CoachFeedback:
    """LLM-backed feedback with a transparent keyword fallback.

    Falls back to the deterministic keyword evaluation when the LLM is not
    configured or any error occurs, so behavior is always honest and never
    blocks the learner.
    """
    keyword_feedback = evaluate_answer(answer, turn_index, lesson_slug=lesson_slug)

    active_provider = provider or get_llm_provider()
    if active_provider is None:
        return keyword_feedback

    turns = roleplay_turns_for_lesson(lesson_slug)
    safe_index = min(turn_index, len(turns) - 1)
    target = turns[safe_index]

    messages = [
        ChatMessage(role="system", content=_system_prompt()),
        ChatMessage(
            role="user",
            content=_user_prompt(
                coach_line=target.coach,
                focus=target.focus,
                sample_answer=target.sample_answer,
                learner_answer=answer,
            ),
        ),
    ]

    try:
        result = await active_provider.generate_chat_completion(
            messages=messages,
            model_config=TASK_MODEL_CONFIGS["conversation_feedback"],
            response_schema=FEEDBACK_RESPONSE_SCHEMA,
        )
        return _parse_feedback(result.content, fallback=keyword_feedback)
    except LLMError as exc:
        logger.warning("conversation_feedback_llm_failed: %s", exc)
        return keyword_feedback
    except Exception as exc:  # never let feedback break a paid turn
        logger.warning("conversation_feedback_unexpected_error: %s", exc)
        return keyword_feedback


def _system_prompt() -> str:
    return (
        "You are an English conversation coach for Indonesian A1 beginners. "
        "Give short, encouraging, accurate feedback. "
        "Write better_version in natural English. "
        "Write indonesian_explanation in Bahasa Indonesia, max 2 sentences. "
        "Write next_practice as one short actionable tip. "
        "Score speaking, grammar, and fluency as integers from 55 to 95 based on the learner's answer. "
        "Respond with JSON only, matching the requested schema."
    )


def _user_prompt(*, coach_line: str, focus: str, sample_answer: str, learner_answer: str) -> str:
    return (
        f"Coach said: \"{coach_line}\"\n"
        f"Conversation focus: {focus}\n"
        f"A good sample answer: \"{sample_answer}\"\n"
        f"Learner answered: \"{learner_answer.strip()}\"\n\n"
        "Evaluate the learner answer and return the JSON feedback."
    )


def _parse_feedback(content: str, *, fallback: CoachFeedback) -> CoachFeedback:
    try:
        data = json.loads(_extract_json(content))
        scores = data["scores"]
        return CoachFeedback(
            better_version=str(data["better_version"]).strip() or fallback.better_version,
            indonesian_explanation=str(data["indonesian_explanation"]).strip()
            or fallback.indonesian_explanation,
            next_practice=str(data["next_practice"]).strip() or fallback.next_practice,
            scores={
                "speaking": clamp_score(int(scores["speaking"])),
                "grammar": clamp_score(int(scores["grammar"])),
                "fluency": clamp_score(int(scores["fluency"])),
            },
        )
    except (ValueError, KeyError, TypeError) as exc:
        logger.warning("conversation_feedback_parse_failed: %s", exc)
        return fallback


def _extract_json(content: str) -> str:
    text = content.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("no_json_object")
    return text[start : end + 1]
