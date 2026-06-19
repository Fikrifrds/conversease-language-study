import unittest
from datetime import datetime
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_current_user
from app.core.observability import runtime_metrics
from app.db.session import get_db
from app.domain.ai import LLMResult
from app.domain.users import User
from app.main import create_app


class ObservabilityTest(unittest.TestCase):
    def client_with_database(self) -> TestClient:
        engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        session_local = sessionmaker(bind=engine, expire_on_commit=False)

        def override_db():
            db = session_local()
            try:
                yield db
            finally:
                db.close()

        app = create_app()
        app.dependency_overrides[get_db] = override_db
        return TestClient(app)

    def test_health_includes_release_and_security_headers(self):
        client = TestClient(create_app())

        response = client.get("/api/health", headers={"x-request-id": "req-test-123"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["x-request-id"], "req-test-123")
        self.assertEqual(response.headers["x-content-type-options"], "nosniff")
        self.assertEqual(response.headers["x-frame-options"], "DENY")
        self.assertEqual(
            response.headers["content-security-policy"],
            "default-src 'none'; frame-ancestors 'none'",
        )
        # HSTS is production-only; dev (is_production=False) must not send it.
        self.assertNotIn("strict-transport-security", response.headers)
        self.assertEqual(response.json()["release_version"], "dev")

    def test_ready_includes_database_and_migration_checks(self):
        client = self.client_with_database()

        with patch(
            "app.api.routes.health.migration_readiness_check",
            return_value={
                "ok": True,
                "applied_heads": ["202606030009"],
                "expected_heads": ["202606030009"],
                "pending_heads": [],
                "unexpected_heads": [],
            },
        ):
            response = client.get("/api/ready")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["checks"]["database"], "ok")
        self.assertEqual(response.json()["checks"]["migrations"], "ok")
        self.assertEqual(response.json()["checks"]["applied_heads"], ["202606030009"])

    def test_ready_fails_when_migrations_are_pending(self):
        client = self.client_with_database()

        with patch(
            "app.api.routes.health.migration_readiness_check",
            return_value={
                "ok": False,
                "applied_heads": ["202606030008"],
                "expected_heads": ["202606030009"],
                "pending_heads": ["202606030009"],
                "unexpected_heads": [],
            },
        ):
            response = client.get("/api/ready")

        self.assertEqual(response.status_code, 503)
        detail = response.json()["detail"]
        self.assertEqual(detail["status"], "not_ready")
        self.assertEqual(detail["checks"]["database"], "ok")
        self.assertEqual(detail["checks"]["migrations"], "pending")
        self.assertEqual(detail["checks"]["pending_heads"], ["202606030009"])

    def test_metrics_reports_runtime_request_counts(self):
        runtime_metrics.reset_for_tests()
        client = TestClient(create_app())

        health_response = client.get("/api/health")
        metrics_response = client.get("/api/metrics")

        self.assertEqual(health_response.status_code, 200)
        self.assertEqual(metrics_response.status_code, 200)
        self.assertEqual(metrics_response.headers["x-content-type-options"], "nosniff")

        payload = metrics_response.json()
        self.assertEqual(payload["service"], "conversease-api")
        self.assertEqual(payload["release_version"], "dev")
        self.assertEqual(payload["requests"]["total"], 1)
        self.assertEqual(payload["requests"]["status_buckets"], {"2xx": 1})
        self.assertEqual(payload["requests"]["methods"], {"GET": 1})
        self.assertEqual(payload["requests"]["paths"], {"/api/health": 1})

    def test_llm_health_returns_ok_when_provider_is_configured(self):
        app = create_app()

        app.dependency_overrides[get_current_user] = lambda: User(
            id="user-1",
            name="Test User",
            email="test@example.local",
            email_verified_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        class FakeProvider:
            async def generate_chat_completion(self, messages, model_config, response_schema=None):
                return LLMResult(content='{"ok": true}')

        with patch("app.api.routes.health.get_llm_provider", return_value=FakeProvider()):
            client = TestClient(app)
            response = client.get("/api/health/llm")

        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "ok")


if __name__ == "__main__":
    unittest.main()
