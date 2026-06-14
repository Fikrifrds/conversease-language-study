import unittest

from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.llm_usage import (
    estimate_cost_usd,
    llm_usage_registry,
    record_llm_usage_from_raw,
)
from app.main import create_app


class LlmUsageRegistryTest(unittest.TestCase):
    def setUp(self):
        llm_usage_registry.reset()

    def tearDown(self):
        llm_usage_registry.reset()

    def test_records_tokens_and_estimates_cost(self):
        record_llm_usage_from_raw(
            provider="together",
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            raw={"usage": {"prompt_tokens": 1000, "completion_tokens": 500, "total_tokens": 1500}},
        )
        snapshot = llm_usage_registry.snapshot()
        self.assertEqual(snapshot["total"]["calls"], 1)
        self.assertEqual(snapshot["total"]["total_tokens"], 1500)
        # 1500 tokens of an ~$0.88/Mtok model is a fraction of a cent, but > 0.
        self.assertGreater(snapshot["total"]["estimated_cost_usd"], 0)
        model_key = "together:meta-llama/Llama-3.3-70B-Instruct-Turbo"
        self.assertIn(model_key, snapshot["by_model"])
        self.assertEqual(snapshot["by_model"][model_key]["prompt_tokens"], 1000)

    def test_estimate_cost_uses_per_model_pricing(self):
        # gpt-4.1-mini output is pricier than input.
        cheap = estimate_cost_usd("gpt-4.1-mini", 1_000_000, 0)
        pricey = estimate_cost_usd("gpt-4.1-mini", 0, 1_000_000)
        self.assertAlmostEqual(cheap, 0.40, places=4)
        self.assertAlmostEqual(pricey, 1.60, places=4)

    def test_missing_usage_block_is_safe(self):
        record_llm_usage_from_raw(provider="openai", model="gpt-4.1-mini", raw=None)
        record_llm_usage_from_raw(provider="openai", model="gpt-4.1-mini", raw={})
        # No usage data -> a call with zero tokens, no crash.
        self.assertEqual(llm_usage_registry.snapshot()["total"]["calls"], 2)
        self.assertEqual(llm_usage_registry.snapshot()["total"]["total_tokens"], 0)


class AdminAiUsageEndpointTest(unittest.TestCase):
    def setUp(self):
        self.original_key = settings.payment_admin_api_key
        settings.payment_admin_api_key = "test-admin-key-with-32-chars"
        llm_usage_registry.reset()
        self.client = TestClient(create_app())
        self.headers = {"x-admin-api-key": settings.payment_admin_api_key}

    def tearDown(self):
        settings.payment_admin_api_key = self.original_key
        llm_usage_registry.reset()

    def test_usage_endpoint_requires_admin(self):
        self.assertIn(self.client.get("/api/admin/ai/usage").status_code, (401, 403))

    def test_usage_endpoint_returns_aggregates(self):
        record_llm_usage_from_raw(
            provider="together",
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            raw={"usage": {"prompt_tokens": 200, "completion_tokens": 100, "total_tokens": 300}},
        )
        response = self.client.get("/api/admin/ai/usage", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["total"]["calls"], 1)
        self.assertEqual(data["total"]["total_tokens"], 300)
        self.assertIn("today", data)
        self.assertIn("by_model", data)


if __name__ == "__main__":
    unittest.main()
