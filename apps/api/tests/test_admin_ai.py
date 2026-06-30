import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.core.config import settings
from app.domain.ai import LLMResult
from app.main import create_app
from app.services.lesson_visual_regeneration import RegeneratedLessonVisual


class AdminAiDiagnosticsTest(unittest.TestCase):
    def setUp(self):
        self.original_key = settings.payment_admin_api_key
        settings.payment_admin_api_key = "test-admin-key-with-32-chars"
        self.client = TestClient(create_app())
        self.headers = {"x-admin-api-key": settings.payment_admin_api_key}

    def tearDown(self):
        settings.payment_admin_api_key = self.original_key

    def test_status_requires_admin_key(self):
        response = self.client.get("/api/admin/ai/status")
        self.assertIn(response.status_code, (401, 403))

    def test_status_reports_provider_configuration(self):
        with patch("app.api.routes.admin_ai.get_llm_provider", return_value=None):
            response = self.client.get("/api/admin/ai/status", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertFalse(data["llm"]["configured"])
        self.assertEqual(data["llm"]["provider"], settings.llm_default_provider)
        self.assertIn("feedback_model", data["llm"])
        self.assertEqual(data["stt"]["provider"], settings.stt_provider)
        self.assertEqual(data["tts"]["provider"], "minimax")
        self.assertEqual(data["image"]["provider"], "together")
        self.assertEqual(data["image"]["model"], "openai/gpt-image-2")

    def test_llm_live_test_returns_503_when_not_configured(self):
        with patch("app.api.routes.admin_ai.get_llm_provider", return_value=None):
            response = self.client.post("/api/admin/ai/test-llm", headers=self.headers)
        self.assertEqual(response.status_code, 503)

    def test_llm_live_test_returns_output(self):
        provider = AsyncMock()
        provider.generate_chat_completion = AsyncMock(
            return_value=LLMResult(content="OK")
        )
        with patch("app.api.routes.admin_ai.get_llm_provider", return_value=provider):
            response = self.client.post("/api/admin/ai/test-llm", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["output"], "OK")

    def test_lesson_visual_regeneration_requires_admin(self):
        response = self.client.post(
            "/api/admin/lessons/saying-hello-and-goodbye/visuals/hero/regenerate"
        )
        self.assertIn(response.status_code, (401, 403))

    def test_lesson_visual_regeneration_returns_stable_asset_url(self):
        result = RegeneratedLessonVisual(
            slug="saying-hello-and-goodbye",
            slot="hero",
            model="openai/gpt-image-2",
            version="123456",
            byte_count=42,
        )
        with patch(
            "app.api.routes.admin_ai.regenerate_lesson_visual",
            new=AsyncMock(return_value=result),
        ):
            response = self.client.post(
                "/api/admin/lessons/saying-hello-and-goodbye/visuals/hero/regenerate",
                headers=self.headers,
            )

        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["model"], "openai/gpt-image-2")
        self.assertEqual(
            data["asset_url"],
            "/lesson-visuals/saying-hello-and-goodbye/hero?v=123456",
        )


if __name__ == "__main__":
    unittest.main()
