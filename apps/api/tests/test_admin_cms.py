import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.data.admin_cms import curriculum_summary, get_admin_lesson, get_email_template
from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.models import ContentRevisionModel
from app.db.session import get_db
from app.main import create_app
from app.repositories.content_revisions import ContentRevisionRepository, content_hash


class AdminCmsTest(unittest.TestCase):
    def test_curriculum_and_email_templates_are_readable(self):
        summary = curriculum_summary()
        lesson = get_admin_lesson("saying-your-name")
        template = get_email_template("auth_verify_email")

        self.assertEqual(summary["course"]["lesson_count"], 5)
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
                legacy_email_route = client.get(
                    "/api/admin/email-templates",
                    headers={"x-admin-api-key": settings.payment_admin_api_key},
                )

            self.assertEqual(unauthorized.status_code, 401)
            self.assertEqual(authorized.status_code, 200)
            self.assertEqual(authorized.json()["data"]["curriculum"]["course"]["lesson_count"], 5)
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


if __name__ == "__main__":
    unittest.main()
