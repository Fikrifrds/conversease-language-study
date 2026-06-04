import asyncio
import unittest
from typing import Any, Dict, List, Optional

from app.domain.ai import ChatMessage, LLMProvider, LLMResult, ModelConfig
from app.services.conversation_feedback import generate_conversation_feedback


class FakeProvider(LLMProvider):
    def __init__(self, content: str) -> None:
        self.content = content
        self.calls = 0

    async def generate_chat_completion(
        self,
        messages: List[ChatMessage],
        model_config: ModelConfig,
        response_schema: Optional[Dict[str, Any]] = None,
    ) -> LLMResult:
        self.calls += 1
        return LLMResult(content=self.content)


class RaisingProvider(LLMProvider):
    async def generate_chat_completion(self, messages, model_config, response_schema=None):
        raise RuntimeError("network down")


class ConversationFeedbackTest(unittest.TestCase):
    def test_uses_llm_response_when_valid(self):
        provider = FakeProvider(
            '{"better_version": "Good morning. I am good, thank you.", '
            '"indonesian_explanation": "Jawaban bagus.", '
            '"next_practice": "Tambahkan pertanyaan balik.", '
            '"scores": {"speaking": 88, "grammar": 90, "fluency": 85}}'
        )
        feedback = asyncio.run(
            generate_conversation_feedback(
                answer="Good morning, I'm good.",
                turn_index=0,
                lesson_slug="saying-hello-and-goodbye",
                provider=provider,
            )
        )
        self.assertEqual(provider.calls, 1)
        self.assertEqual(feedback.scores["grammar"], 90)
        self.assertEqual(feedback.better_version, "Good morning. I am good, thank you.")

    def test_clamps_out_of_range_scores(self):
        provider = FakeProvider(
            '{"better_version": "x", "indonesian_explanation": "y", '
            '"next_practice": "z", "scores": {"speaking": 200, "grammar": 10, "fluency": 75}}'
        )
        feedback = asyncio.run(
            generate_conversation_feedback(
                answer="hi",
                turn_index=0,
                lesson_slug="saying-hello-and-goodbye",
                provider=provider,
            )
        )
        self.assertEqual(feedback.scores["speaking"], 95)
        self.assertEqual(feedback.scores["grammar"], 55)

    def test_falls_back_to_keyword_when_no_provider(self):
        feedback = asyncio.run(
            generate_conversation_feedback(
                answer="Good morning, thank you.",
                turn_index=0,
                lesson_slug="saying-hello-and-goodbye",
                provider=None,
            )
        )
        # keyword evaluator returns a sample answer as better_version
        self.assertTrue(feedback.better_version)
        self.assertIn("speaking", feedback.scores)

    def test_falls_back_when_provider_errors(self):
        feedback = asyncio.run(
            generate_conversation_feedback(
                answer="Good morning, thank you.",
                turn_index=0,
                lesson_slug="saying-hello-and-goodbye",
                provider=RaisingProvider(),
            )
        )
        self.assertTrue(feedback.better_version)

    def test_falls_back_when_json_malformed(self):
        provider = FakeProvider("not json at all")
        feedback = asyncio.run(
            generate_conversation_feedback(
                answer="hello there",
                turn_index=0,
                lesson_slug="saying-hello-and-goodbye",
                provider=provider,
            )
        )
        self.assertTrue(feedback.better_version)


if __name__ == "__main__":
    unittest.main()
