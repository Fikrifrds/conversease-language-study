import unittest
from datetime import datetime
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import create_access_token
from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.session import get_db
from app.domain.conversation_practice import TurnTranscription
from app.main import create_app
from app.services.conversation_partner_chat import PartnerReply, PartnerSummary
from app.services.speech_to_text import SpeechToTextResult


class ConversationPartnerRoutesTest(unittest.TestCase):
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
                    email="qa-partner@example.local",
                    password_hash="hashed",
                    email_verified_at=now,
                    created_at=now,
                    updated_at=now,
                )
            )
            db.commit()

    def tearDown(self):
        self.app.dependency_overrides.clear()

    def test_topics_endpoint_returns_a1_topics(self):
        response = self.client.get(
            "/api/conversation-partner/topics?level_code=A1", headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertTrue(data)
        self.assertTrue(all(topic["level_code"] == "A1" for topic in data))

    def test_topics_endpoint_has_topics_for_each_level(self):
        for level in ["A1", "A2", "B1", "B2", "C1"]:
            response = self.client.get(
                f"/api/conversation-partner/topics?level_code={level}",
                headers=self.headers,
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()["data"]
            self.assertTrue(data, f"expected topics for level {level}")
            self.assertTrue(all(topic["level_code"] == level for topic in data))

    def test_full_flow_session_turn_and_summary(self):
        with patch(
            "app.api.routes.conversation_partner.synthesize_partner_reply_audio",
            new=AsyncMock(return_value="data:audio/mpeg;base64,AAAA"),
        ):
            create = self.client.post(
                "/api/conversation-partner/sessions",
                headers=self.headers,
                json={"topic_key": "order-a-drink"},
            )
        self.assertEqual(create.status_code, 200, create.text)
        session_id = create.json()["data"]["session_id"]
        self.assertEqual(create.json()["data"]["opening_audio"], "data:audio/mpeg;base64,AAAA")

        transcription = SpeechToTextResult(
            text="I want a coffee",
            transcription=TurnTranscription(
                input_source="audio",
                provider="assemblyai",
                model="universal-3-pro",
                transcript_id="tx-1",
                confidence=0.95,
                audio_duration_seconds=2.1,
                metadata={"language_code": "en"},
            ),
        )

        with patch(
            "app.api.routes.conversation_partner.transcribe_recorded_audio",
            new=AsyncMock(return_value=transcription),
        ), patch(
            "app.api.routes.conversation_partner.generate_partner_reply",
            new=AsyncMock(
                return_value=PartnerReply(
                    reply="Sure! Small or large?", on_topic=True, should_end=False
                )
            ),
        ), patch(
            "app.api.routes.conversation_partner.synthesize_partner_reply_audio",
            new=AsyncMock(return_value="data:audio/mpeg;base64,BBBB"),
        ):
            turn = self.client.post(
                f"/api/conversation-partner/sessions/{session_id}/turns/audio",
                headers=self.headers,
                files={"audio": ("turn.webm", b"fake-bytes", "audio/webm")},
            )

        self.assertEqual(turn.status_code, 200, turn.text)
        body = turn.json()["data"]
        self.assertEqual(body["user_transcript"], "I want a coffee")
        self.assertEqual(body["partner_reply"], "Sure! Small or large?")
        self.assertEqual(body["partner_audio"], "data:audio/mpeg;base64,BBBB")
        self.assertEqual(body["completed_turns"], 1)
        self.assertFalse(body["should_end"])

        with patch(
            "app.api.routes.conversation_partner.summarize_session",
            new=AsyncMock(
                return_value=PartnerSummary(
                    summary="Nice work",
                    indonesian_explanation="Bagus, lanjutkan.",
                    scores={"speaking": 80, "grammar": 75, "fluency": 82},
                )
            ),
        ):
            summary = self.client.post(
                f"/api/conversation-partner/sessions/{session_id}/summary",
                headers=self.headers,
            )

        self.assertEqual(summary.status_code, 200, summary.text)
        self.assertEqual(summary.json()["data"]["scores"]["speaking"], 80)
        self.assertEqual(summary.json()["data"]["completed_turns"], 1)

    def test_unknown_topic_returns_404(self):
        response = self.client.post(
            "/api/conversation-partner/sessions",
            headers=self.headers,
            json={"topic_key": "does-not-exist"},
        )
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
