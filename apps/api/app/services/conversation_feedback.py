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
        return _parse_feedback(
            result.content,
            fallback=keyword_feedback,
            lesson_slug=lesson_slug,
            turn_index=turn_index,
        )
    except LLMError as exc:
        logger.error(
            "conversation_feedback_llm_failed lesson=%s turn=%s: %s",
            lesson_slug,
            turn_index,
            exc,
        )
        return keyword_feedback
    except Exception as exc:  # never let feedback break a paid turn
        logger.error(
            "conversation_feedback_unexpected_error lesson=%s turn=%s: %s",
            lesson_slug,
            turn_index,
            exc,
        )
        return keyword_feedback


def _system_prompt() -> str:
    return (
        "You are an English conversation coach for Indonesian A1 beginners. "
        "Give short, encouraging, accurate feedback. "
        "If the learner's answer does not answer the coach question (e.g. they say 'No.'), say so clearly and provide a correct short answer. "
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


def _parse_feedback(
    content: str,
    *,
    fallback: CoachFeedback,
    lesson_slug: str,
    turn_index: int,
) -> CoachFeedback:
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
        if not scores:
            logger.warning(
                "conversation_feedback_missing_scores lesson=%s turn=%s keys=%s",
                lesson_slug,
                turn_index,
                sorted(list(data.keys())) if isinstance(data, dict) else "n/a",
            )

        better_version = (
            data.get("better_version")
            or data.get("betterVersion")
            or data.get("better")
            or data.get("suggested_answer")
            or data.get("suggestedAnswer")
            or fallback.better_version
        )
        indonesian_explanation = (
            data.get("indonesian_explanation")
            or data.get("indonesianExplanation")
            or data.get("explanation_id")
            or data.get("explanationId")
            or fallback.indonesian_explanation
        )
        next_practice = (
            data.get("next_practice")
            or data.get("nextPractice")
            or data.get("tip")
            or fallback.next_practice
        )
        return CoachFeedback(
            better_version=str(better_version).strip() or fallback.better_version,
            indonesian_explanation=str(indonesian_explanation).strip()
            or fallback.indonesian_explanation,
            next_practice=str(next_practice).strip() or fallback.next_practice,
            scores={
                "speaking": clamp_score(int(scores.get("speaking", fallback.scores["speaking"]))),
                "grammar": clamp_score(int(scores.get("grammar", fallback.scores["grammar"]))),
                "fluency": clamp_score(int(scores.get("fluency", fallback.scores["fluency"]))),
            },
        )
    except (ValueError, KeyError, TypeError) as exc:
        logger.error(
            "conversation_feedback_parse_failed lesson=%s turn=%s keys=%s: %s",
            lesson_slug,
            turn_index,
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
