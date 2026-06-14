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

        # The opening-line TTS cache is module-level; clear it so a value cached
        # by one test's mock does not leak into another test.
        from app.api.routes import conversation_partner

        conversation_partner._opening_audio_cache.clear()

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

    def _topic_max_turns(self, topic_key: str) -> int:
        from app.domain.conversation_partner import get_topic

        return get_topic(topic_key).max_turns

    def _create_session_with_turn(self) -> str:
        with patch(
            "app.api.routes.conversation_partner.synthesize_partner_reply_audio",
            new=AsyncMock(return_value="data:audio/mpeg;base64,AAAA"),
        ):
            create = self.client.post(
                "/api/conversation-partner/sessions",
                headers=self.headers,
                json={"topic_key": "order-a-drink"},
            )
        session_id = create.json()["data"]["session_id"]
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
            self.client.post(
                f"/api/conversation-partner/sessions/{session_id}/turns/audio",
                headers=self.headers,
                files={"audio": ("turn.webm", b"fake-bytes", "audio/webm")},
            )
        return session_id

    def test_summary_is_persisted_and_reused(self):
        session_id = self._create_session_with_turn()
        summarize_mock = AsyncMock(
            return_value=PartnerSummary(
                summary="Nice work",
                indonesian_explanation="Bagus, lanjutkan.",
                scores={"speaking": 80, "grammar": 76, "fluency": 84},
            )
        )
        with patch(
            "app.api.routes.conversation_partner.summarize_session", new=summarize_mock
        ):
            first = self.client.post(
                f"/api/conversation-partner/sessions/{session_id}/summary",
                headers=self.headers,
            )
            second = self.client.post(
                f"/api/conversation-partner/sessions/{session_id}/summary",
                headers=self.headers,
            )

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.json()["data"]["scores"]["speaking"], 80)
        # The summary is computed once and then served from storage.
        self.assertEqual(summarize_mock.await_count, 1)

    def test_list_sessions_returns_history_with_score(self):
        session_id = self._create_session_with_turn()
        with patch(
            "app.api.routes.conversation_partner.summarize_session",
            new=AsyncMock(
                return_value=PartnerSummary(
                    summary="Nice work",
                    indonesian_explanation="Bagus.",
                    scores={"speaking": 80, "grammar": 70, "fluency": 78},
                )
            ),
        ):
            self.client.post(
                f"/api/conversation-partner/sessions/{session_id}/summary",
                headers=self.headers,
            )

        listing = self.client.get(
            "/api/conversation-partner/sessions", headers=self.headers
        )
        self.assertEqual(listing.status_code, 200, listing.text)
        rows = listing.json()["data"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["session_id"], session_id)
        self.assertEqual(rows[0]["topic_title"], "Order a Drink")
        self.assertEqual(rows[0]["completed_turns"], 1)
        self.assertEqual(rows[0]["overall_score"], 76)

    def test_session_detail_returns_messages(self):
        session_id = self._create_session_with_turn()
        detail = self.client.get(
            f"/api/conversation-partner/sessions/{session_id}", headers=self.headers
        )
        self.assertEqual(detail.status_code, 200, detail.text)
        data = detail.json()["data"]
        roles = [m["role"] for m in data["messages"]]
        self.assertEqual(roles, ["partner", "user", "partner"])
        self.assertEqual(data["messages"][1]["text"], "I want a coffee")
        # Resume relies on these to restore the progress bar.
        self.assertEqual(data["completed_turns"], 1)
        self.assertEqual(data["max_turns"], self._topic_max_turns("order-a-drink"))

    def test_topic_progress_exposes_open_session_for_resume(self):
        session_id = self._create_session_with_turn()  # one turn, not completed
        progress = self.client.get(
            "/api/conversation-partner/topic-progress", headers=self.headers
        )
        self.assertEqual(progress.status_code, 200)
        entry = progress.json()["data"]["order-a-drink"]
        self.assertFalse(entry["completed"])
        self.assertTrue(entry["has_open_session"])
        self.assertEqual(entry["open_session_id"], session_id)

    def test_start_reuses_open_session(self):
        # Starting the same topic twice without finishing reuses the same session
        # instead of creating a new (abandoned) one.
        session_id = self._create_session_with_turn()
        with patch(
            "app.api.routes.conversation_partner.synthesize_partner_reply_audio",
            new=AsyncMock(return_value="data:audio/mpeg;base64,AAAA"),
        ):
            again = self.client.post(
                "/api/conversation-partner/sessions",
                headers=self.headers,
                json={"topic_key": "order-a-drink"},
            )
        self.assertEqual(again.status_code, 200, again.text)
        self.assertEqual(again.json()["data"]["session_id"], session_id)
        self.assertEqual(again.json()["data"]["completed_turns"], 1)

    def test_topic_progress_reports_score_and_open_session(self):
        # A completed session with a score.
        done_id = self._create_session_with_turn()
        with patch(
            "app.api.routes.conversation_partner.summarize_session",
            new=AsyncMock(
                return_value=PartnerSummary(
                    summary="Nice",
                    indonesian_explanation="Bagus.",
                    scores={"speaking": 80, "grammar": 70, "fluency": 78},
                )
            ),
        ):
            self.client.post(
                f"/api/conversation-partner/sessions/{done_id}/summary",
                headers=self.headers,
            )
        # Mark it completed via a final turn flagged should_end.
        with self.SessionLocal() as db:
            session = db.get(models.ConversationSessionModel, done_id)
            session.status = "completed"
            db.commit()

        progress = self.client.get(
            "/api/conversation-partner/topic-progress", headers=self.headers
        )
        self.assertEqual(progress.status_code, 200, progress.text)
        data = progress.json()["data"]
        self.assertIn("order-a-drink", data)
        self.assertTrue(data["order-a-drink"]["completed"])
        self.assertEqual(data["order-a-drink"]["best_score"], 76)
        # The completed session id is exposed so the UI can load its transcript.
        self.assertEqual(data["order-a-drink"]["session_id"], done_id)

    def test_reset_topic_clears_progress(self):
        self._create_session_with_turn()
        reset = self.client.delete(
            "/api/conversation-partner/topics/order-a-drink/progress",
            headers=self.headers,
        )
        self.assertEqual(reset.status_code, 200, reset.text)
        self.assertGreaterEqual(reset.json()["data"]["removed_sessions"], 1)

        progress = self.client.get(
            "/api/conversation-partner/topic-progress", headers=self.headers
        )
        self.assertNotIn("order-a-drink", progress.json()["data"])

    def test_unknown_topic_returns_404(self):
        response = self.client.post(
            "/api/conversation-partner/sessions",
            headers=self.headers,
            json={"topic_key": "does-not-exist"},
        )
        self.assertEqual(response.status_code, 404)

    def test_a1_topic_is_free(self):
        with patch(
            "app.api.routes.conversation_partner.synthesize_partner_reply_audio",
            new=AsyncMock(return_value="data:audio/mpeg;base64,AAAA"),
        ):
            response = self.client.post(
                "/api/conversation-partner/sessions",
                headers=self.headers,
                json={"topic_key": "order-a-drink"},
            )
        self.assertEqual(response.status_code, 200, response.text)

    def test_a2_topic_requires_pro(self):
        with patch(
            "app.api.routes.conversation_partner.synthesize_partner_reply_audio",
            new=AsyncMock(return_value="data:audio/mpeg;base64,AAAA"),
        ):
            response = self.client.post(
                "/api/conversation-partner/sessions",
                headers=self.headers,
                json={"topic_key": "make-weekend-plans"},
            )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["detail"], "conversation_partner_requires_pro")

    def test_a2_topic_allowed_for_pro_user(self):
        now = datetime.utcnow()
        with self.SessionLocal() as db:
            db.add(
                models.UserSubscriptionModel(
                    id="sub-pro-partner",
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

        with patch(
            "app.api.routes.conversation_partner.synthesize_partner_reply_audio",
            new=AsyncMock(return_value="data:audio/mpeg;base64,AAAA"),
        ):
            response = self.client.post(
                "/api/conversation-partner/sessions",
                headers=self.headers,
                json={"topic_key": "make-weekend-plans"},
            )
        self.assertEqual(response.status_code, 200, response.text)

    def test_opening_audio_is_cached_across_sessions(self):
        synth = AsyncMock(return_value="data:audio/mpeg;base64,AAAA")
        with patch(
            "app.api.routes.conversation_partner.synthesize_partner_reply_audio",
            new=synth,
        ):
            first = self.client.post(
                "/api/conversation-partner/sessions",
                headers=self.headers,
                json={"topic_key": "order-a-drink"},
            )
            second = self.client.post(
                "/api/conversation-partner/sessions",
                headers=self.headers,
                json={"topic_key": "order-a-drink"},
            )

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        # Opening TTS for a static line is synthesized once, then served from cache.
        self.assertEqual(synth.await_count, 1)

    def test_turn_not_charged_when_no_minutes(self):
        from app.repositories.billing import BillingRepository

        session_id = self._create_session_with_turn()

        # Drain remaining minutes, then attempt another turn.
        with self.SessionLocal() as db:
            balance = BillingRepository(db).minute_balance("user-123")
            remaining_before = balance.total_minutes

        transcription = SpeechToTextResult(
            text="another line",
            transcription=TurnTranscription(
                input_source="audio",
                provider="assemblyai",
                model="universal-3-pro",
                transcript_id="tx-2",
                confidence=0.9,
            ),
        )
        # Force an out-of-minutes state by consuming everything first.
        with self.SessionLocal() as db:
            billing = BillingRepository(db)
            if remaining_before > 0:
                billing.consume_minutes(
                    user_id="user-123", requested_minutes=remaining_before
                )

        reply_mock = AsyncMock()
        with patch(
            "app.api.routes.conversation_partner.transcribe_recorded_audio",
            new=AsyncMock(return_value=transcription),
        ), patch(
            "app.api.routes.conversation_partner.generate_partner_reply",
            new=reply_mock,
        ):
            blocked = self.client.post(
                f"/api/conversation-partner/sessions/{session_id}/turns/audio",
                headers=self.headers,
                files={"audio": ("turn.webm", b"fake-bytes", "audio/webm")},
            )

        self.assertEqual(blocked.status_code, 402)
        # Rejected before any paid LLM call when out of minutes.
        reply_mock.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()
