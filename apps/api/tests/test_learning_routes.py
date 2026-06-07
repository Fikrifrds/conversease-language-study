import unittest
from datetime import datetime
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.security import create_access_token
from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.session import get_db
from app.main import create_app


class LearningRoutesTest(unittest.TestCase):
    def test_authenticated_user_can_get_lesson_audio_asset(self):
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
        client = TestClient(app)
        token = create_access_token("user-123")
        headers = {"Authorization": f"Bearer {token}"}
        audio_asset = {
            "key": "dialogue_main",
            "type": "dialogue",
            "audio_url": "https://conversease-assets.s3.ap-southeast-1.amazonaws.com/audio.mp3",
            "playback_url": "https://signed.example.com/audio.mp3",
            "duration_seconds": 10.5,
            "provider": "minimax",
            "model": "speech-2.8-hd",
            "voice_id": "English_expressive_narrator",
            "audio_format": "mp3",
            "storage_key": "conversease/audio/english/A1/audio.mp3",
            "generated_at": "2026-06-04T00:00:00+00:00",
            "generated_by": "Audio QA",
        }

        try:
            with session_local() as db:
                now = datetime.utcnow()
                db.add(
                    models.UserModel(
                        id="user-123",
                        name="QA Tester",
                        email="qa@example.local",
                        password_hash="hashed",
                        email_verified_at=now,
                        created_at=now,
                        updated_at=now,
                    )
                )
                db.commit()

            with patch("app.api.routes.learning.lesson_audio_asset", return_value=audio_asset):
                unauthorized = client.get("/api/lessons/saying-hello-and-goodbye/audio")
                authorized = client.get("/api/lessons/saying-hello-and-goodbye/audio", headers=headers)

            self.assertEqual(unauthorized.status_code, 401)
            self.assertEqual(authorized.status_code, 200)
            self.assertEqual(authorized.json()["data"]["playback_url"], audio_asset["playback_url"])
        finally:
            app.dependency_overrides.clear()

    def test_courses_lists_all_levels_with_unlock_flags(self):
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
        client = TestClient(app)
        headers = {"Authorization": f"Bearer {create_access_token('user-123')}"}
        try:
            with session_local() as db:
                now = datetime.utcnow()
                db.add(
                    models.UserModel(
                        id="user-123",
                        name="QA",
                        email="qa-courses@example.local",
                        password_hash="hashed",
                        email_verified_at=now,
                        created_at=now,
                        updated_at=now,
                    )
                )
                db.commit()

            response = client.get("/api/courses", headers=headers)
            self.assertEqual(response.status_code, 200)
            courses = response.json()["data"]
            self.assertEqual([c["level_code"] for c in courses], ["A1", "A2", "B1", "B2", "C1"])
            # Fresh user: A1 unlocked, higher levels locked.
            self.assertTrue(courses[0]["unlocked"])
            self.assertFalse(courses[1]["unlocked"])

            # A non-A1 lesson resolves through the generalized lookup.
            b2 = client.get("/api/lessons/clear-argument-mission")
            self.assertEqual(b2.status_code, 200)
            self.assertEqual(b2.json()["data"]["level_code"], "B2")
        finally:
            app.dependency_overrides.clear()

    def test_completing_last_level_lesson_sends_level_up_email(self):
        from unittest.mock import AsyncMock

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
        client = TestClient(app)
        headers = {"Authorization": f"Bearer {create_access_token('user-123')}"}

        from app.data.curriculum import published_lessons

        a1_slugs = [lesson["slug"] for lesson in published_lessons("A1")]
        try:
            with session_local() as db:
                now = datetime.utcnow()
                db.add(
                    models.UserModel(
                        id="user-123",
                        name="QA",
                        email="qa-levelup@example.local",
                        password_hash="hashed",
                        email_verified_at=now,
                        created_at=now,
                        updated_at=now,
                    )
                )
                db.commit()

            send_mock = AsyncMock()
            with patch(
                "app.api.routes.learning.LearningEmailService.send_level_completed_email",
                new=send_mock,
            ):
                # Complete all but the last A1 lesson: no email yet.
                for slug in a1_slugs[:-1]:
                    client.post(f"/api/lessons/{slug}/progress/complete", headers=headers, json={})
                self.assertEqual(send_mock.await_count, 0)
                # Completing the last one triggers exactly one level-up email.
                client.post(
                    f"/api/lessons/{a1_slugs[-1]}/progress/complete", headers=headers, json={}
                )
                self.assertEqual(send_mock.await_count, 1)
                self.assertEqual(send_mock.await_args.kwargs["completed_level"], "A1")
                self.assertEqual(send_mock.await_args.kwargs["next_level"], "A2")
        finally:
            app.dependency_overrides.clear()

    def test_pro_gating_blocks_free_user_on_a2_lesson(self):
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
        client = TestClient(app)
        headers = {"Authorization": f"Bearer {create_access_token('user-123')}"}
        a2_slug = "starting-small-talk"
        try:
            with session_local() as db:
                now = datetime.utcnow()
                db.add(
                    models.UserModel(
                        id="user-123",
                        name="QA",
                        email="qa-pro@example.local",
                        password_hash="hashed",
                        email_verified_at=now,
                        created_at=now,
                        updated_at=now,
                    )
                )
                db.commit()

            # Free user: A1 lesson allowed, A2 lesson blocked with 403.
            a1 = client.post(
                "/api/lessons/saying-hello-and-goodbye/progress/start", headers=headers, json={}
            )
            self.assertEqual(a1.status_code, 200)
            blocked = client.post(f"/api/lessons/{a2_slug}/progress/start", headers=headers, json={})
            self.assertEqual(blocked.status_code, 403)

            # /courses marks A2 as requiring Pro and not accessible for a free user.
            courses = client.get("/api/courses", headers=headers).json()["data"]
            a2_course = next(c for c in courses if c["level_code"] == "A2")
            self.assertTrue(a2_course["requires_pro"])
            self.assertFalse(a2_course["accessible"])

            # Upgrade the user to Pro -> A2 lesson now allowed.
            with session_local() as db:
                now = datetime.utcnow()
                db.add(
                    models.UserSubscriptionModel(
                        id="sub-1",
                        user_id="user-123",
                        plan_key="pro_1_month",
                        status="active",
                        starts_at=now,
                        expires_at=None,
                        created_at=now,
                        updated_at=now,
                    )
                )
                db.commit()
            allowed = client.post(f"/api/lessons/{a2_slug}/progress/start", headers=headers, json={})
            self.assertEqual(allowed.status_code, 200)
        finally:
            app.dependency_overrides.clear()

    def test_get_a1_level_test_returns_published_test(self):
        client = TestClient(create_app())

        response = client.get("/api/level-tests/A1")

        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["level_code"], "A1")
        self.assertEqual(data["status"], "published")
        self.assertEqual(sum(section["weight"] for section in data["sections"]), 100)

    def test_a1_level_test_preview_uses_yaml_thresholds(self):
        client = TestClient(create_app())

        response = client.post(
            "/api/level-tests/A1/attempts/preview",
            json={
                "lesson_completion_percent": 85,
                "scores": {
                    "listening": 70,
                    "speaking_conversation": 70,
                    "pronunciation_fluency": 70,
                    "useful_phrases": 70,
                    "grammar": 70,
                    "reading": 70,
                    "writing": 70,
                },
            },
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertTrue(data["passed"])
        self.assertEqual(data["overall_score"], 70)

    def test_authenticated_user_can_start_submit_and_read_level_test_report(self):
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
        client = TestClient(app)
        token = create_access_token("user-123")
        headers = {"Authorization": f"Bearer {token}"}
        original_admin_key = settings.payment_admin_api_key
        settings.payment_admin_api_key = "test-admin-key-with-32-chars"
        admin_headers = {"x-admin-api-key": settings.payment_admin_api_key}

        try:
            with session_local() as db:
                now = datetime.utcnow()
                db.add(
                    models.UserModel(
                        id="user-123",
                        name="QA Tester",
                        email="qa@example.local",
                        password_hash="hashed",
                        email_verified_at=now,
                        created_at=now,
                        updated_at=now,
                    )
                )
                db.commit()

            started = client.post("/api/level-tests/A1/attempts", headers=headers)
            self.assertEqual(started.status_code, 200)
            attempt_id = started.json()["data"]["id"]

            submitted = client.post(
                f"/api/level-test-attempts/{attempt_id}/submit",
                headers=headers,
                json={
                    "lesson_completion_percent": 85,
                    "scores": {
                        "listening": 70,
                        "speaking_conversation": 70,
                        "pronunciation_fluency": 70,
                        "useful_phrases": 70,
                        "grammar": 70,
                        "reading": 70,
                        "writing": 70,
                    },
                    "responses": {"source": "test"},
                },
            )
            report = client.get(f"/api/level-test-attempts/{attempt_id}/report", headers=headers)
            attempts = client.get("/api/me/level-test-attempts?level_code=A1", headers=headers)
            admin_attempts = client.get(
                "/api/admin/level-test-attempts?level_code=A1&status=submitted",
                headers=admin_headers,
            )
            admin_scored = client.post(
                f"/api/admin/level-test-attempts/{attempt_id}/score",
                headers=admin_headers,
                json={
                    "reviewed_by": "Admin QA",
                    "lesson_completion_percent": 90,
                    "scores": {
                        "listening": 80,
                        "speaking_conversation": 80,
                        "pronunciation_fluency": 75,
                        "useful_phrases": 80,
                        "grammar": 80,
                        "reading": 75,
                        "writing": 75,
                    },
                    "notes": "Manual beta review",
                },
            )

            self.assertEqual(submitted.status_code, 200)
            self.assertEqual(submitted.json()["data"]["status"], "submitted")
            self.assertTrue(submitted.json()["data"]["passed"])
            self.assertEqual(report.status_code, 200)
            self.assertEqual(report.json()["data"]["id"], attempt_id)
            self.assertEqual(attempts.status_code, 200)
            self.assertEqual(attempts.json()["data"][0]["id"], attempt_id)
            self.assertEqual(admin_attempts.status_code, 200)
            self.assertEqual(admin_attempts.json()["data"][0]["id"], attempt_id)
            self.assertEqual(admin_scored.status_code, 200)
            self.assertEqual(admin_scored.json()["data"]["status"], "reviewed")
            self.assertEqual(admin_scored.json()["data"]["reviewed_by"], "Admin QA")
        finally:
            settings.payment_admin_api_key = original_admin_key
            app.dependency_overrides.clear()


if __name__ == "__main__":
    unittest.main()
