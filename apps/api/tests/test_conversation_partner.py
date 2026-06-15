import asyncio
import unittest
from typing import Any, Dict, List, Optional

from app.domain.ai import ChatMessage, LLMProvider, LLMResult, ModelConfig
from app.domain.conversation_partner import (
    difficulty_profile,
    get_topic,
    topics_for_level,
)
from app.services.conversation_partner_chat import (
    generate_partner_reply,
    summarize_session,
)


class FakeProvider(LLMProvider):
    def __init__(self, content: str) -> None:
        self.content = content
        self.calls = 0
        self.last_messages: List[ChatMessage] = []

    async def generate_chat_completion(
        self,
        messages: List[ChatMessage],
        model_config: ModelConfig,
        response_schema: Optional[Dict[str, Any]] = None,
    ) -> LLMResult:
        self.calls += 1
        self.last_messages = messages
        return LLMResult(content=self.content)


class RaisingProvider(LLMProvider):
    async def generate_chat_completion(self, messages, model_config, response_schema=None):
        raise RuntimeError("network down")


TOPIC = get_topic("order-a-drink")


class ConversationPartnerDomainTest(unittest.TestCase):
    def test_a1_topics_exist(self):
        topics = topics_for_level("A1")
        self.assertTrue(topics)
        self.assertTrue(all(t.level_code == "A1" for t in topics))

    def test_difficulty_profile_differs_by_level(self):
        self.assertNotEqual(difficulty_profile("A1"), difficulty_profile("C1"))


class ConversationPartnerReplyTest(unittest.TestCase):
    def test_uses_llm_reply_when_valid(self):
        provider = FakeProvider(
            '{"reply": "Sure! Small or large?", "on_topic": true, "should_end": false}'
        )
        reply = asyncio.run(
            generate_partner_reply(
                topic=TOPIC,
                level_code="A1",
                history=[("user", "I want coffee")],
                user_message="I want coffee",
                completed_turns=1,
                provider=provider,
            )
        )
        self.assertEqual(provider.calls, 1)
        self.assertEqual(reply.reply, "Sure! Small or large?")
        self.assertFalse(reply.should_end)

    def test_uses_llm_reply_under_response_key(self):
        provider = FakeProvider(
            '{"response": "Sure! Small or large?", "on_topic": true, "should_end": false}'
        )
        reply = asyncio.run(
            generate_partner_reply(
                topic=TOPIC,
                level_code="A1",
                history=[("user", "I want coffee")],
                user_message="I want coffee",
                completed_turns=1,
                provider=provider,
            )
        )
        self.assertEqual(reply.reply, "Sure! Small or large?")
        self.assertFalse(reply.should_end)

    def test_forces_end_when_no_turns_left(self):
        provider = FakeProvider(
            '{"reply": "Anything else?", "on_topic": true, "should_end": false}'
        )
        reply = asyncio.run(
            generate_partner_reply(
                topic=TOPIC,
                level_code="A1",
                history=[],
                user_message="ok",
                completed_turns=TOPIC.max_turns,  # turns_left -> 0
                provider=provider,
            )
        )
        self.assertTrue(reply.should_end)

    def test_does_not_end_early_before_min_turns(self):
        # Even if the LLM signals should_end on turn 1, the partner keeps going
        # until enough exchanges have happened so the conversation isn't abrupt.
        provider = FakeProvider(
            '{"reply": "Great, anything else?", "on_topic": true, "should_end": true}'
        )
        reply = asyncio.run(
            generate_partner_reply(
                topic=TOPIC,
                level_code="A1",
                history=[("user", "coffee please")],
                user_message="coffee please",
                completed_turns=0,  # current_turn = 1, below the minimum
                provider=provider,
            )
        )
        self.assertFalse(reply.should_end)

    def test_honors_end_after_min_turns(self):
        provider = FakeProvider(
            '{"reply": "Thanks, see you!", "on_topic": true, "should_end": true}'
        )
        reply = asyncio.run(
            generate_partner_reply(
                topic=TOPIC,
                level_code="A1",
                history=[],
                user_message="thank you",
                completed_turns=TOPIC.max_turns - 2,  # well past the minimum
                provider=provider,
            )
        )
        self.assertTrue(reply.should_end)

    def test_final_turn_prompt_instructs_a_graceful_close(self):
        # On the last allowed exchange the partner must close gracefully instead
        # of asking a dangling question (the "tiba-tiba berhenti" report).
        provider = FakeProvider(
            '{"reply": "It was great meeting you. Goodbye!", "on_topic": true, "should_end": true}'
        )
        reply = asyncio.run(
            generate_partner_reply(
                topic=TOPIC,
                level_code="A1",
                history=[],
                user_message="see you",
                completed_turns=TOPIC.max_turns - 1,  # this reply is the final turn
                provider=provider,
            )
        )
        self.assertTrue(reply.should_end)
        system_prompt = provider.last_messages[0].content
        self.assertIn("FINAL EXCHANGE", system_prompt)
        self.assertIn("Do NOT ask a new question", system_prompt)

    def test_early_end_window_still_closes_gracefully(self):
        # When ending is allowed but it's not the hard cap, the prompt must still
        # forbid a dangling question so a voluntary early close stays smooth.
        provider = FakeProvider(
            '{"reply": "Lovely chatting. See you around!", "on_topic": true, "should_end": true}'
        )
        reply = asyncio.run(
            generate_partner_reply(
                topic=TOPIC,
                level_code="A1",
                history=[],
                user_message="thanks",
                completed_turns=TOPIC.max_turns - 2,  # ending allowed, not the cap
                provider=provider,
            )
        )
        self.assertTrue(reply.should_end)
        system_prompt = provider.last_messages[0].content
        self.assertNotIn("FINAL EXCHANGE", system_prompt)
        self.assertIn("PREFER to close", system_prompt)
        self.assertIn("do NOT end on a question", system_prompt)

    def test_prompt_forbids_repeating_answered_questions(self):
        provider = FakeProvider(
            '{"reply": "Nice! What do you study?", "on_topic": true, "should_end": false}'
        )
        asyncio.run(
            generate_partner_reply(
                topic=TOPIC,
                level_code="A1",
                history=[
                    ("partner", "Where are you from?"),
                    ("user", "I'm from Indonesia."),
                ],
                user_message="I'm from Indonesia.",
                completed_turns=1,
                provider=provider,
            )
        )
        system_prompt = provider.last_messages[0].content
        self.assertIn("already answered", system_prompt)
        self.assertIn("NEW detail", system_prompt)

    def test_cannot_end_too_early(self):
        # Early in the conversation, ending is not allowed even if the LLM signals
        # it, and the prompt must not contain the closing directives.
        provider = FakeProvider(
            '{"reply": "Nice! What size?", "on_topic": true, "should_end": true}'
        )
        reply = asyncio.run(
            generate_partner_reply(
                topic=TOPIC,
                level_code="A1",
                history=[],
                user_message="a coffee",
                completed_turns=1,  # current_turn = 2, far below min_turns
                provider=provider,
            )
        )
        self.assertFalse(reply.should_end)
        system_prompt = provider.last_messages[0].content
        self.assertNotIn("FINAL EXCHANGE", system_prompt)
        self.assertNotIn("PREFER to close", system_prompt)
        self.assertIn("follow-up question", system_prompt)

    def test_falls_back_when_no_provider(self):
        reply = asyncio.run(
            generate_partner_reply(
                topic=TOPIC,
                level_code="A1",
                history=[],
                user_message="hello",
                completed_turns=0,
                provider=None,
            )
        )
        self.assertTrue(reply.reply)

    def test_falls_back_when_provider_errors(self):
        reply = asyncio.run(
            generate_partner_reply(
                topic=TOPIC,
                level_code="A1",
                history=[],
                user_message="hello",
                completed_turns=0,
                provider=RaisingProvider(),
            )
        )
        self.assertTrue(reply.reply)

    def test_falls_back_when_json_malformed(self):
        provider = FakeProvider("not json")
        reply = asyncio.run(
            generate_partner_reply(
                topic=TOPIC,
                level_code="A1",
                history=[],
                user_message="hello",
                completed_turns=0,
                provider=provider,
            )
        )
        self.assertTrue(reply.reply)


class ConversationPartnerSummaryTest(unittest.TestCase):
    def test_summary_clamps_scores(self):
        provider = FakeProvider(
            '{"summary": "Nice", "indonesian_explanation": "Bagus", '
            '"scores": {"speaking": 200, "grammar": 10, "fluency": 80}}'
        )
        summary = asyncio.run(
            summarize_session(
                topic=TOPIC,
                level_code="A1",
                history=[("partner", "Hi"), ("user", "I want coffee")],
                provider=provider,
            )
        )
        self.assertEqual(summary.scores["speaking"], 95)
        self.assertEqual(summary.scores["grammar"], 55)

    def test_summary_falls_back_on_error(self):
        summary = asyncio.run(
            summarize_session(
                topic=TOPIC,
                level_code="A1",
                history=[],
                provider=RaisingProvider(),
            )
        )
        self.assertTrue(summary.summary)
        self.assertIn("speaking", summary.scores)


if __name__ == "__main__":
    unittest.main()
