import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.data.admin_cms import curriculum_summary, get_admin_lesson, get_email_template
from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.models import AudioVoicePreviewModel, ContentRevisionModel
from app.db.session import get_db
from app.main import create_app
from app.repositories.audio_voice_previews import DEFAULT_VOICE_PREVIEW_SAMPLE_TEXT
from app.repositories.content_revisions import ContentRevisionRepository, content_hash


class AdminCmsTest(unittest.TestCase):
    def test_curriculum_and_email_templates_are_readable(self):
        summary = curriculum_summary()
        lesson = get_admin_lesson("saying-your-name")
        template = get_email_template("auth_verify_email")

        self.assertEqual(summary["course"]["lesson_count"], 40)
        self.assertEqual(summary["readiness_overview"]["planned_lesson_count"], 240)
        self.assertEqual(summary["readiness_overview"]["implemented_lesson_count"], 240)
        self.assertEqual(
            sorted(
                (level["course"]["language"], level["course"]["level_code"])
                for level in summary["readiness_levels"]
            ),
            [
                ("arabic", "A1"),
                ("english", "A1"),
                ("english", "A2"),
                ("english", "B1"),
                ("english", "B2"),
                ("english", "C1"),
            ],
        )
        self.assertEqual(summary["validation_issues"], [])
        self.assertEqual(lesson["roleplay"]["scenario_key"], "saying_your_name_online_class")
        self.assertEqual(len(lesson["content_hash"]), 64)
        self.assertEqual(template["subject"], "Verifikasi email Conversease kamu")
        self.assertEqual(len(template["content_hash"]), 64)

    def test_admin_cms_routes_require_admin_key(self):
        original_key = settings.payment_admin_api_key
        settings.payment_admin_api_key = "test-admin-key-with-32-chars"
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

        try:
            with TestClient(app) as client:
                unauthorized = client.get("/api/admin/cms/summary")
                authorized = client.get(
                    "/api/admin/cms/summary",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                )
                overview = client.get(
                    "/api/admin/cms/overview",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                )
                english_readiness = client.get(
                    "/api/admin/cms/readiness?language=english",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                )
                english_lessons = client.get(
                    "/api/admin/cms/curriculum/lessons?language=english",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                )
                cms_email_templates = client.get(
                    "/api/admin/cms/email-templates",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                )
                revisions = client.get(
                    "/api/admin/cms/revisions",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                )
                legacy_email_route = client.get(
                    "/api/admin/email-templates",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                )

                self.assertEqual(unauthorized.status_code, 401)
                self.assertEqual(authorized.status_code, 200)
                self.assertEqual(overview.status_code, 200)
                self.assertEqual(english_readiness.status_code, 200)
                self.assertEqual(english_lessons.status_code, 200)
                self.assertEqual(cms_email_templates.status_code, 200)
                self.assertEqual(revisions.status_code, 200)
                self.assertEqual(authorized.json()["data"]["curriculum"]["course"]["lesson_count"], 40)
                self.assertEqual(
                    english_readiness.json()["data"]["readiness_overview"]["planned_lesson_count"],
                    200,
                )
                self.assertEqual(len(english_lessons.json()["data"]["lessons"]), 200)
            self.assertEqual(
                authorized.json()["data"]["curriculum"]["readiness_overview"]["planned_lesson_count"],
                240,
            )
            self.assertEqual(legacy_email_route.status_code, 200)
        finally:
            settings.payment_admin_api_key = original_key
            app.dependency_overrides.clear()

    def test_admin_cms_patch_records_content_revision(self):
        original_key = settings.payment_admin_api_key
        settings.payment_admin_api_key = "test-admin-key-with-32-chars"
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

        before_lesson = {
            "slug": "saying-your-name",
            "title": "Saying Your Name",
            "roleplay": {"opening_line": "Hello."},
        }
        before_lesson = {**before_lesson, "content_hash": content_hash(before_lesson)}
        after_lesson = {
            **before_lesson,
            "title": "Say Your Name Clearly",
        }
        after_lesson = {**after_lesson, "content_hash": content_hash(after_lesson)}
        app = create_app()
        app.dependency_overrides[get_db] = override_db

        try:
            client = TestClient(app)
            with (
                patch("app.api.routes.admin_cms.get_admin_lesson", return_value=before_lesson),
                patch("app.api.routes.admin_cms.update_lesson_metadata", return_value=after_lesson),
            ):
                response = client.patch(
                    "/api/admin/cms/curriculum/lessons/saying-your-name",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                    json={
                        "updated_by": "Fikri",
                        "expected_content_hash": before_lesson["content_hash"],
                        "title": "Say Your Name Clearly",
                    },
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["revision"]["version"], 1)
            self.assertEqual(response.json()["revision"]["changed_by"], "Fikri")

            with session_local() as db:
                revision = db.execute(select(ContentRevisionModel)).scalar_one()
                self.assertEqual(revision.resource_type, "curriculum_lesson")
                self.assertEqual(revision.resource_key, "saying-your-name")
                self.assertEqual(revision.before_json["title"], "Saying Your Name")
                self.assertEqual(revision.after_json["title"], "Say Your Name Clearly")
                self.assertNotIn("content_hash", revision.before_json)
                self.assertNotIn("content_hash", revision.after_json)
        finally:
            settings.payment_admin_api_key = original_key
            app.dependency_overrides.clear()

    def test_admin_cms_audio_settings_route(self):
        original_key = settings.payment_admin_api_key
        settings.payment_admin_api_key = "test-admin-key-with-32-chars"
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

        try:
            client = TestClient(app)
            with patch(
                "app.api.routes.admin_cms.audio_generation_settings",
                new=AsyncMock(
                    return_value={
                        "minimax_configured": True,
                        "s3_configured": True,
                        "default_model": "speech-2.8-hd",
                        "default_voice_id": "English_expressive_narrator",
                        "default_language_boost": "English",
                        "models": ["speech-2.8-hd"],
                        "voices": [
                            {
                                "voice_id": "English_expressive_narrator",
                                "voice_name": "Expressive Narrator",
                                "category": "system",
                                "description": "Clear narrator voice.",
                            }
                        ],
                    }
                ),
            ):
                response = client.get(
                    "/api/admin/cms/audio/settings",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json()["data"]["minimax_configured"])
            self.assertEqual(response.json()["data"]["voices"][0]["voice_id"], "English_expressive_narrator")
        finally:
            settings.payment_admin_api_key = original_key
            app.dependency_overrides.clear()

    def test_admin_cms_voice_preview_route(self):
        original_key = settings.payment_admin_api_key
        settings.payment_admin_api_key = "test-admin-key-with-32-chars"
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

        preview_audio = {
            "audio_url": "https://cdn.example.com/previews/sample.mp3",
            "playback_url": "https://signed.example.com/previews/sample.mp3",
            "object_key": "conversease/audio/previews/voice/sample.mp3",
            "duration_seconds": 3.2,
            "audio_format": "mp3",
            "audio_size": 3200,
            "model": "speech-2.8-hd",
            "voice_id": "English_expressive_narrator",
            "trace_id": "trace-preview",
            "usage_characters": 82,
            "sample_text": DEFAULT_VOICE_PREVIEW_SAMPLE_TEXT,
            "generated_by": "Audio QA",
            "generated_at": "2026-06-04T00:00:00+00:00",
        }

        try:
            client = TestClient(app)
            with patch(
                "app.services.audio_preview_cache.generate_voice_preview_audio",
                new=AsyncMock(return_value=preview_audio),
            ) as generate_preview:
                first_response = client.post(
                    "/api/admin/cms/audio/voice-preview",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                    json={
                        "generated_by": "Audio QA",
                        "model": "speech-2.8-hd",
                        "voice_id": "English_expressive_narrator",
                        "speed": 1,
                    },
                )
                second_response = client.post(
                    "/api/admin/cms/audio/voice-preview",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                    json={
                        "generated_by": "Audio QA",
                        "model": "speech-2.8-hd",
                        "voice_id": "English_expressive_narrator",
                        "speed": 1,
                    },
                )
                list_response = client.get(
                    "/api/admin/cms/audio/voice-previews?model=speech-2.8-hd&speed=1",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                )

            self.assertEqual(first_response.status_code, 200)
            self.assertEqual(second_response.status_code, 200)
            self.assertEqual(list_response.status_code, 200)
            self.assertEqual(first_response.json()["data"]["audio_url"], preview_audio["audio_url"])
            self.assertFalse(first_response.json()["data"]["cached"])
            self.assertTrue(second_response.json()["data"]["cached"])
            self.assertEqual(list_response.json()["data"][0]["voice_id"], "English_expressive_narrator")
            generate_preview.assert_awaited_once_with(
                provider="minimax",
                model="speech-2.8-hd",
                voice_id="English_expressive_narrator",
                speed=1.0,
                sample_text=DEFAULT_VOICE_PREVIEW_SAMPLE_TEXT,
                generated_by="Audio QA",
            )

            with session_local() as db:
                preview = db.execute(select(AudioVoicePreviewModel)).scalar_one()
                self.assertEqual(preview.voice_id, "English_expressive_narrator")
                self.assertEqual(preview.sample_text, DEFAULT_VOICE_PREVIEW_SAMPLE_TEXT)
        finally:
            settings.payment_admin_api_key = original_key
            app.dependency_overrides.clear()

    def test_admin_cms_generate_audio_records_revision(self):
        original_key = settings.payment_admin_api_key
        settings.payment_admin_api_key = "test-admin-key-with-32-chars"
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

        lesson_ref = SimpleNamespace(
            lesson_key="lesson-01-saying-hello",
            audio_manifest_path="/tmp/audio_manifest.yaml",
        )
        generated_audio = {
            "lesson_slug": "saying-hello",
            "lesson_key": "lesson-01-saying-hello",
            "title": "Saying Hello and Goodbye",
            "audio_url": "https://cdn.example.com/audio.mp3",
            "playback_url": "https://signed.example.com/audio.mp3",
            "object_key": "conversease/audio/english/A1/audio.mp3",
            "duration_seconds": 12.4,
            "audio_format": "mp3",
            "audio_size": 12000,
            "provider": "minimax",
            "model": "speech-2.8-hd",
            "voice_id": "English_expressive_narrator",
            "trace_id": "trace-1",
            "usage_characters": 120,
            "manifest": {"status": "generated"},
        }
        app = create_app()
        app.dependency_overrides[get_db] = override_db

        try:
            client = TestClient(app)
            with (
                patch("app.api.routes.admin_cms.find_lesson_audio_reference", return_value=lesson_ref),
                patch("app.api.routes.admin_cms.read_yaml_mapping", return_value={"status": "not_generated"}),
                patch(
                    "app.api.routes.admin_cms.generate_lesson_listening_audio",
                    new=AsyncMock(return_value=generated_audio),
                ) as generate_audio,
                patch(
                    "app.api.routes.admin_cms.curriculum_summary",
                    return_value={"readiness_overview": {"audio_ready_count": 1}},
                ),
            ):
                response = client.post(
                    "/api/admin/cms/curriculum/lessons/saying-hello/audio/listening",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                    json={
                        "generated_by": "Audio QA",
                        "model": "speech-2.8-hd",
                        "voice_id": "English_expressive_narrator",
                        "speed": 0.95,
                    },
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["data"]["audio_url"], generated_audio["audio_url"])
            self.assertEqual(response.json()["data"]["playback_url"], generated_audio["playback_url"])
            self.assertEqual(response.json()["revision"]["resource_type"], "curriculum_audio")
            self.assertEqual(response.json()["revision"]["changed_by"], "Audio QA")
            generate_audio.assert_awaited_once_with(
                lesson_slug="saying-hello",
                provider=None,
                model="speech-2.8-hd",
                voice_id="English_expressive_narrator",
                speed=0.95,
                generated_by="Audio QA",
            )

            with session_local() as db:
                revision = db.execute(select(ContentRevisionModel)).scalar_one()
                self.assertEqual(revision.resource_type, "curriculum_audio")
                self.assertEqual(revision.resource_key, "saying-hello")
                self.assertEqual(revision.metadata_json["provider"], "minimax")
        finally:
            settings.payment_admin_api_key = original_key
            app.dependency_overrides.clear()

    def test_admin_cms_patch_rejects_stale_content_hash(self):
        original_key = settings.payment_admin_api_key
        settings.payment_admin_api_key = "test-admin-key-with-32-chars"
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

        current_lesson = {
            "slug": "saying-your-name",
            "title": "Current Title",
            "roleplay": {"opening_line": "Hello."},
        }
        current_lesson = {**current_lesson, "content_hash": content_hash(current_lesson)}
        app = create_app()
        app.dependency_overrides[get_db] = override_db

        try:
            client = TestClient(app)
            with (
                patch("app.api.routes.admin_cms.get_admin_lesson", return_value=current_lesson),
                patch("app.api.routes.admin_cms.update_lesson_metadata") as update_lesson,
            ):
                response = client.patch(
                    "/api/admin/cms/curriculum/lessons/saying-your-name",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                    json={
                        "updated_by": "Fikri",
                        "expected_content_hash": "0" * 64,
                        "title": "Stale Update",
                    },
                )

            self.assertEqual(response.status_code, 409)
            self.assertEqual(response.json()["detail"], "content_changed_reload_required")
            update_lesson.assert_not_called()
        finally:
            settings.payment_admin_api_key = original_key
            app.dependency_overrides.clear()

    def test_admin_cms_rollback_creates_new_revision(self):
        original_key = settings.payment_admin_api_key
        settings.payment_admin_api_key = "test-admin-key-with-32-chars"
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

        current_lesson = {
            "slug": "saying-your-name",
            "title": "Edited Title",
            "status": "published",
            "estimated_minutes": 8,
            "conversation_goal": "Edited goal for rollback test.",
            "roleplay": {
                "opening_line": "Edited opening.",
                "learner_goal": "Edited learner goal.",
                "max_turns": 4,
                "target_phrases": ["Edited phrase"],
            },
        }
        target_lesson = {
            **current_lesson,
            "title": "Saying Your Name",
            "conversation_goal": "Practice saying your name clearly.",
        }

        with session_local() as db:
            target_revision = ContentRevisionRepository(db).record_revision(
                resource_type="curriculum_lesson",
                resource_key="saying-your-name",
                action="update",
                changed_by="Fikri",
                before_payload=current_lesson,
                after_payload=target_lesson,
                metadata={"source": "admin_cms"},
            )
            target_revision_id = target_revision.id

        app = create_app()
        app.dependency_overrides[get_db] = override_db

        try:
            client = TestClient(app)
            with (
                patch("app.api.routes.admin_cms.get_admin_lesson", return_value=current_lesson),
                patch(
                    "app.api.routes.admin_cms.restore_lesson_from_snapshot",
                    return_value=target_lesson,
                ) as restore_lesson,
            ):
                response = client.post(
                    f"/api/admin/cms/revisions/{target_revision_id}/rollback",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                    json={"restored_by": "Admin QA", "notes": "Rollback smoke"},
                )

            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertEqual(body["data"]["title"], "Saying Your Name")
            self.assertEqual(body["revision"]["action"], "rollback")
            self.assertEqual(body["revision"]["version"], 2)
            self.assertEqual(body["revision"]["changed_by"], "Admin QA")
            self.assertEqual(body["rolled_back_from"]["id"], target_revision_id)
            restore_lesson.assert_called_once_with("saying-your-name", target_lesson)

            with session_local() as db:
                revisions = (
                    db.execute(
                        select(ContentRevisionModel).order_by(ContentRevisionModel.version.asc())
                    )
                    .scalars()
                    .all()
                )
                self.assertEqual(len(revisions), 2)
                self.assertEqual(revisions[0].action, "update")
                self.assertEqual(revisions[1].action, "rollback")
                self.assertEqual(revisions[1].metadata_json["rollback_revision_id"], target_revision_id)
                self.assertEqual(revisions[1].metadata_json["notes"], "Rollback smoke")
        finally:
            settings.payment_admin_api_key = original_key
            app.dependency_overrides.clear()


class AdminCmsExamAudioTest(unittest.TestCase):
    def setUp(self):
        self.original_key = settings.payment_admin_api_key
        settings.payment_admin_api_key = "test-admin-key-with-32-chars"
        engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(engine)
        self.session_local = sessionmaker(bind=engine, expire_on_commit=False)

        def override_db():
            db = self.session_local()
            try:
                yield db
            finally:
                db.close()

        self.app = create_app()
        self.app.dependency_overrides[get_db] = override_db
        self.client = TestClient(self.app)
        self.headers = {"x-admin-api-key": settings.payment_admin_api_key}
        self._seed_exam()

    def tearDown(self):
        settings.payment_admin_api_key = self.original_key
        self.app.dependency_overrides.clear()

    def _seed_exam(self):
        from datetime import datetime

        from app.db.exam_models import ExamItemModel, ExamSectionModel, ExamTemplateModel
        from app.services.audio_generation import exam_item_source_text_hash

        now = datetime.utcnow()
        with self.session_local() as db:
            template = ExamTemplateModel(
                id="tpl-1",
                code="CEFR-A1-EXAM-v1",
                level_code="A1",
                title="A1 Exam",
                duration_minutes=45,
                passing_score_percent=60,
                status="active",
                created_by="tests",
                created_at=now,
                updated_at=now,
            )
            listening = ExamSectionModel(
                id="sec-listening",
                exam_template_id="tpl-1",
                code="LISTENING",
                title="Listening",
                sequence_order=1,
                duration_minutes=10,
                score_weight_percent=25,
                item_types_allowed=["mcq"],
                created_at=now,
                updated_at=now,
            )
            speaking = ExamSectionModel(
                id="sec-speaking",
                exam_template_id="tpl-1",
                code="SPEAKING",
                title="Speaking",
                sequence_order=2,
                duration_minutes=5,
                score_weight_percent=25,
                item_types_allowed=["audio_response"],
                created_at=now,
                updated_at=now,
            )
            fresh = ExamItemModel(
                id="item-fresh",
                exam_template_id="tpl-1",
                section_id="sec-listening",
                item_type="mcq",
                sequence_order=1,
                prompt_text="Where are they?",
                stimulus_text="Mina: Hello there.\nBen: Good morning.",
                stimulus_audio_url="https://cdn.example.com/fresh.wav",
                score_points=1,
                created_at=now,
                updated_at=now,
            )
            fresh.config_json = {
                "audio_generation": {"source_text_hash": exam_item_source_text_hash(fresh)}
            }
            stale = ExamItemModel(
                id="item-stale",
                exam_template_id="tpl-1",
                section_id="sec-listening",
                item_type="mcq",
                sequence_order=2,
                prompt_text="What time is it?",
                stimulus_text="Mina: It is three o'clock now.",
                stimulus_audio_url="https://cdn.example.com/old.wav",
                config_json={"audio_generation": {"source_text_hash": "outdated-hash"}},
                score_points=1,
                created_at=now,
                updated_at=now,
            )
            speaking_item = ExamItemModel(
                id="item-speaking",
                exam_template_id="tpl-1",
                section_id="sec-speaking",
                item_type="audio_response",
                sequence_order=1,
                prompt_text="Read this sentence aloud.",
                stimulus_text="Hello, my name is Anna.",
                score_points=10,
                created_at=now,
                updated_at=now,
            )
            db.add_all([template, listening, speaking, fresh, stale, speaking_item])
            db.commit()

    def test_templates_report_speaking_items_and_stale_audio(self):
        response = self.client.get("/api/admin/cms/exams/templates", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        data = response.json()["data"][0]
        self.assertEqual(data["listening_item_count"], 2)
        self.assertEqual(data["listening_audio_stale_count"], 1)
        self.assertEqual(data["speaking_item_count"], 1)
        self.assertEqual(data["speaking_audio_ready_count"], 0)
        by_id = {item["id"]: item for item in data["listening_items"] + data["speaking_items"]}
        self.assertFalse(by_id["item-fresh"]["audio_stale"])
        self.assertTrue(by_id["item-stale"]["audio_stale"])
        self.assertFalse(by_id["item-speaking"]["audio_ready"])

    def test_bulk_generation_only_missing_covers_stale_and_speaking(self):
        generated_audio = {
            "audio_url": "https://cdn.example.com/new.wav",
            "playback_url": "https://signed.example.com/new.wav",
            "object_key": "conversease/audio/exams/new.wav",
            "duration_seconds": 9.5,
            "audio_format": "wav",
            "audio_size": 9000,
            "provider": "minimax",
            "model": "speech-2.8-hd",
            "voice_id": "English_expressive_narrator",
            "speaker_voices": {},
            "line_count": 2,
            "trace_id": "trace-1",
            "usage_characters": 80,
            "generated_by": "Audio QA",
            "generated_at": "2026-06-12T00:00:00+00:00",
        }

        with patch(
            "app.api.routes.admin_cms.generate_exam_item_listening_audio",
            new=AsyncMock(return_value=generated_audio),
        ) as generate_audio:
            response = self.client.post(
                "/api/admin/cms/exams/templates/tpl-1/audio/listening",
                headers=self.headers,
                json={
                    "generated_by": "Audio QA",
                    "model": "speech-2.8-hd",
                    "voice_id": "English_expressive_narrator",
                    "speed": 1.0,
                    "only_missing": True,
                },
            )

        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        # Stale listening item and speaking item regenerate; fresh item is skipped.
        self.assertEqual(payload["generated_count"], 2)
        generated_item_ids = {
            call.kwargs["item"].id for call in generate_audio.await_args_list
        }
        self.assertEqual(generated_item_ids, {"item-stale", "item-speaking"})

        # Regenerated items now carry the current source hash and are no longer stale.
        listing = self.client.get("/api/admin/cms/exams/templates", headers=self.headers)
        data = listing.json()["data"][0]
        by_id = {item["id"]: item for item in data["listening_items"] + data["speaking_items"]}
        self.assertFalse(by_id["item-stale"]["audio_stale"])
        self.assertTrue(by_id["item-speaking"]["audio_ready"])


if __name__ == "__main__":
    unittest.main()
