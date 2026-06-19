import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.rate_limit import rate_limiter
from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.session import get_db
from app.main import create_app


class RateLimitTest(unittest.TestCase):
    def setUp(self):
        self.original_enabled = settings.rate_limit_enabled
        self.original_window = settings.rate_limit_window_seconds
        self.original_auth_limit = settings.auth_rate_limit_requests
        self.original_admin_limit = settings.admin_rate_limit_requests
        self.original_conversation_limit = settings.conversation_rate_limit_requests
        self.original_email_recipient_limit = settings.email_recipient_rate_limit_requests
        rate_limiter.reset()

    def tearDown(self):
        settings.rate_limit_enabled = self.original_enabled
        settings.rate_limit_window_seconds = self.original_window
        settings.auth_rate_limit_requests = self.original_auth_limit
        settings.admin_rate_limit_requests = self.original_admin_limit
        settings.conversation_rate_limit_requests = self.original_conversation_limit
        settings.email_recipient_rate_limit_requests = self.original_email_recipient_limit
        rate_limiter.reset()

    def client_with_database(self) -> TestClient:
        engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(engine)
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

    def test_auth_endpoint_is_rate_limited(self):
        settings.rate_limit_enabled = True
        settings.rate_limit_window_seconds = 60
        settings.auth_rate_limit_requests = 1
        client = self.client_with_database()

        first = client.post(
            "/api/auth/login",
            json={"email": "missing@example.local", "password": "WrongPassword123"},
        )
        second = client.post(
            "/api/auth/login",
            json={"email": "missing@example.local", "password": "WrongPassword123"},
        )

        self.assertEqual(first.status_code, 401)
        self.assertEqual(second.status_code, 429)
        self.assertEqual(second.json()["detail"], "Rate limit exceeded")
        self.assertEqual(second.headers["retry-after"], "60")
        self.assertEqual(second.headers["x-ratelimit-limit"], "1")
        self.assertEqual(second.headers["x-ratelimit-remaining"], "0")

    def test_admin_endpoint_is_rate_limited_before_admin_key_check(self):
        settings.rate_limit_enabled = True
        settings.rate_limit_window_seconds = 60
        settings.admin_rate_limit_requests = 1
        client = TestClient(create_app())

        first = client.get("/api/admin/cms/summary")
        second = client.get("/api/admin/cms/summary")

        self.assertIn(first.status_code, {401, 503})
        self.assertEqual(second.status_code, 429)
        self.assertEqual(second.json()["detail"], "Rate limit exceeded")

    def test_conversation_turn_is_rate_limited_per_client(self):
        settings.rate_limit_enabled = True
        settings.rate_limit_window_seconds = 60
        settings.conversation_rate_limit_requests = 1
        client = TestClient(create_app())

        # Unauthenticated, but the rate limiter runs before auth. Different
        # session ids share one bucket per client, so the second turn is blocked.
        first = client.post("/api/conversation-sessions/session-a/turns", json={"transcript": "hi"})
        second = client.post("/api/conversation-sessions/session-b/turns", json={"transcript": "hi"})

        self.assertNotEqual(first.status_code, 429)
        self.assertEqual(second.status_code, 429)
        self.assertEqual(second.json()["detail"], "Rate limit exceeded")

    def test_forgot_password_is_limited_per_recipient_email(self):
        settings.rate_limit_enabled = True
        settings.rate_limit_window_seconds = 60
        settings.auth_rate_limit_requests = 100  # keep the per-IP limiter out of the way
        settings.email_recipient_rate_limit_requests = 2
        client = self.client_with_database()

        payload = {"email": "victim@example.local"}
        statuses = [client.post("/api/auth/forgot-password", json=payload).status_code for _ in range(3)]

        self.assertEqual(statuses, [200, 200, 429])

    def test_email_recipient_limit_does_not_leak_account_existence(self):
        # A non-existent address hits the same cap, so 429-vs-200 can't be used
        # to enumerate which emails are registered.
        settings.rate_limit_enabled = True
        settings.rate_limit_window_seconds = 60
        settings.auth_rate_limit_requests = 100
        settings.email_recipient_rate_limit_requests = 1
        client = self.client_with_database()

        first = client.post("/api/auth/forgot-password", json={"email": "ghost@example.local"})
        second = client.post("/api/auth/forgot-password", json={"email": "ghost@example.local"})

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 429)

    def test_health_is_not_rate_limited(self):
        settings.rate_limit_enabled = True
        settings.auth_rate_limit_requests = 1
        client = TestClient(create_app())

        responses = [client.get("/api/health") for _ in range(3)]

        self.assertEqual([response.status_code for response in responses], [200, 200, 200])


if __name__ == "__main__":
    unittest.main()
