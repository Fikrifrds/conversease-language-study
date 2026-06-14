import unittest
from datetime import datetime
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import create_access_token
from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.models import ConversationTurnModel
from app.db.session import get_db
from app.domain.conversation_practice import TurnTranscription
from app.main import create_app
from app.services.speech_to_text import SpeechToTextResult


class ConversationRoutesTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)

        def override_db():
            db = self.SessionLocal()
            try:
                yield db
            finally:
                db.close()

        self.app = create_app()
        self.app.dependency_overrides[get_db] = override_db
        self.client = TestClient(self.app)
        self.headers = {"Authorization": f"Bearer {create_access_token('user-123')}"}

        with self.SessionLocal() as db:
            now = datetime.utcnow()
            db.add(
                models.UserModel(
                    id="user-123",
                    name="QA User",
                    email="qa-conversation@example.local",
                    password_hash="hashed",
                    email_verified_at=now,
                    created_at=now,
                    updated_at=now,
                )
            )
            db.commit()

    def tearDown(self):
        self.app.dependency_overrides.clear()

    def test_audio_turn_transcribes_and_records_stt_metadata(self):
        session_response = self.client.post(
            "/api/conversation-sessions",
            headers=self.headers,
            json={"lesson_slug": "saying-hello-and-goodbye"},
        )
        session_id = session_response.json()["data"]["id"]
        transcription = SpeechToTextResult(
            text="Good morning. I'm good, thank you.",
            transcription=TurnTranscription(
                input_source="audio",
                provider="assemblyai",
                model="universal-3-pro,universal-2",
                transcript_id="assembly-transcript-1",
                confidence=0.96,
                audio_duration_seconds=4.2,
                metadata={"filename": "answer.webm"},
            ),
        )

        with patch(
            "app.api.routes.conversation.transcribe_recorded_audio",
            new=AsyncMock(return_value=transcription),
        ) as transcribe_audio:
            response = self.client.post(
                f"/api/conversation-sessions/{session_id}/turns/audio",
                headers=self.headers,
                files={"audio": ("answer.webm", b"fake-audio", "audio/webm")},
            )

        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["user_transcript"], "Good morning. I'm good, thank you.")
        self.assertEqual(data["transcription"]["provider"], "assemblyai")
        self.assertEqual(data["transcription"]["transcript_id"], "assembly-transcript-1")
        transcribe_audio.assert_awaited_once()

        with self.SessionLocal() as db:
            turn = db.execute(select(ConversationTurnModel)).scalar_one()
            self.assertEqual(turn.input_source, "audio")
            self.assertEqual(turn.stt_provider, "assemblyai")
            self.assertEqual(turn.stt_transcript_id, "assembly-transcript-1")
            self.assertEqual(turn.stt_metadata_json["filename"], "answer.webm")

    def test_audio_turn_rejects_unsupported_content_type(self):
        session_response = self.client.post(
            "/api/conversation-sessions",
            headers=self.headers,
            json={"lesson_slug": "saying-hello-and-goodbye"},
        )
        session_id = session_response.json()["data"]["id"]

        response = self.client.post(
            f"/api/conversation-sessions/{session_id}/turns/audio",
            headers=self.headers,
            files={"audio": ("answer.txt", b"not audio", "text/plain")},
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], "unsupported_audio_content_type")

    def test_create_session_a1_is_free(self):
        response = self.client.post(
            "/api/conversation-sessions",
            headers=self.headers,
            json={"lesson_slug": "saying-hello-and-goodbye", "level_code": "A1"},
        )
        self.assertEqual(response.status_code, 200)

    def test_create_session_a2_requires_pro(self):
        # A free user cannot start an A2+ coach scenario; the level is derived
        # server-side from the lesson, so a spoofed level_code does not matter.
        response = self.client.post(
            "/api/conversation-sessions",
            headers=self.headers,
            json={"lesson_slug": "starting-small-talk", "level_code": "A1"},
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["detail"], "conversation_coach_requires_pro")

    def test_create_session_a2_allowed_for_pro_user(self):
        now = datetime.utcnow()
        with self.SessionLocal() as db:
            db.add(
                models.UserSubscriptionModel(
                    id="sub-pro-1",
                    user_id="user-123",
                    plan_key="pro_monthly",
                    status="active",
                    starts_at=now,
                    expires_at=None,
                    created_at=now,
                    updated_at=now,
                )
            )
            db.commit()

        response = self.client.post(
            "/api/conversation-sessions",
            headers=self.headers,
            json={"lesson_slug": "starting-small-talk", "level_code": "A2"},
        )
        self.assertEqual(response.status_code, 200)

    def test_latest_practice_returns_resumable_turns(self):
        session_response = self.client.post(
            "/api/conversation-sessions",
            headers=self.headers,
            json={"lesson_slug": "saying-hello-and-goodbye"},
        )
        session_id = session_response.json()["data"]["id"]

        self.client.post(
            f"/api/conversation-sessions/{session_id}/turns",
            headers=self.headers,
            json={"transcript": "Good morning. I'm good, thank you."},
        )

        latest = self.client.get(
            "/api/conversation-practice/latest?lesson_slug=saying-hello-and-goodbye",
            headers=self.headers,
        )
        self.assertEqual(latest.status_code, 200)
        data = latest.json()["data"]
        self.assertEqual(data["session_id"], session_id)
        self.assertEqual(data["completed_turns"], 1)
        self.assertEqual(len(data["turns"]), 1)
        self.assertEqual(data["turns"][0]["user_transcript"], "Good morning. I'm good, thank you.")
        self.assertIsNotNone(data["last_feedback"])
        self.assertIn("scores", data["last_feedback"])
        self.assertTrue(data["first_coach_message"])


if __name__ == "__main__":
    unittest.main()
