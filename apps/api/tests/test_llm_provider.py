import unittest

import httpx

from app.domain.ai import ChatMessage, ModelConfig
from app.services.llm import LLMError, TogetherProvider


class FakeAsyncClient:
    """Returns queued httpx.Response objects and records the payloads posted."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.posted_payloads = []

    async def post(self, url, headers=None, json=None):
        # Snapshot the payload: the provider mutates the same dict across retries.
        self.posted_payloads.append(dict(json))
        status = self._responses.pop(0)
        request = httpx.Request("POST", url)
        if status == 200:
            return httpx.Response(
                200,
                request=request,
                json={
                    "choices": [{"message": {"content": '{"reply": "Hi there!"}'}}],
                    "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
                },
            )
        return httpx.Response(status, request=request, json={"error": "bad"})


def run(coro):
    import asyncio

    return asyncio.run(coro)


class TogetherProviderRetryTest(unittest.TestCase):
    def _provider_with(self, responses):
        provider = TogetherProvider(api_key="k", base_url="https://example", timeout_seconds=5)
        client = FakeAsyncClient(responses)
        provider._client = client
        return provider, client

    def test_drops_response_format_after_schema_400(self):
        provider, client = self._provider_with([400, 200])
        result = run(
            provider.generate_chat_completion(
                messages=[ChatMessage(role="user", content="hi")],
                model_config=ModelConfig(provider="together", model="m", temperature=0.5, max_tokens=50),
                response_schema={"type": "object"},
            )
        )
        self.assertIn("Hi there", result.content)
        # First attempt asked for JSON mode; the retry dropped it.
        self.assertIn("response_format", client.posted_payloads[0])
        self.assertNotIn("response_format", client.posted_payloads[1])

    def test_retries_transient_5xx_then_succeeds(self):
        provider, _ = self._provider_with([503, 200])
        result = run(
            provider.generate_chat_completion(
                messages=[ChatMessage(role="user", content="hi")],
                model_config=ModelConfig(provider="together", model="m", temperature=0.5, max_tokens=50),
            )
        )
        self.assertIn("Hi there", result.content)

    def test_raises_after_exhausting_retries(self):
        provider, _ = self._provider_with([500, 500, 500])
        with self.assertRaises(LLMError):
            run(
                provider.generate_chat_completion(
                    messages=[ChatMessage(role="user", content="hi")],
                    model_config=ModelConfig(provider="together", model="m", temperature=0.5, max_tokens=50),
                )
            )


if __name__ == "__main__":
    unittest.main()
