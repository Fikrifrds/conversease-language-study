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
