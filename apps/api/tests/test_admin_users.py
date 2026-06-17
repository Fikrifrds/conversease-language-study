import unittest
from datetime import datetime, timedelta

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


class AdminUsersRoutesTest(unittest.TestCase):
    def setUp(self):
        self.original_admin_emails_raw = settings.admin_emails_raw
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)

    def tearDown(self):
        settings.admin_emails_raw = self.original_admin_emails_raw

    def client(self) -> TestClient:
        def override_db():
            db = self.SessionLocal()
            try:
                yield db
            finally:
                db.close()

        app = create_app()
        app.dependency_overrides[get_db] = override_db
        return TestClient(app)

    def seed_users(self) -> None:
        with self.SessionLocal() as db:
            now = datetime.utcnow()
            db.add_all(
                [
                    models.UserModel(
                        id="user-admin",
                        name="Admin User",
                        email="admin@example.local",
                        role="admin",
                        password_hash="hashed",
                        email_verified_at=now,
                        created_at=now,
                        updated_at=now,
                    ),
                    models.UserModel(
                        id="user-student",
                        name="Student User",
                        email="student@example.local",
                        role="student",
                        password_hash="hashed",
                        email_verified_at=now,
                        created_at=now,
                        updated_at=now,
                    ),
                    models.UserModel(
                        id="user-bootstrap",
                        name="Bootstrap User",
                        email="owner@example.local",
                        role="student",
                        password_hash="hashed",
                        email_verified_at=now,
                        created_at=now,
                        updated_at=now,
                    ),
                ]
            )
            db.commit()

    def auth_headers(self, user_id: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {create_access_token(user_id)}"}

    def seed_spam_user(self) -> None:
        with self.SessionLocal() as db:
            old = datetime.utcnow() - timedelta(days=45)
            db.add(
                models.UserModel(
                    id="user-spam",
                    name="MFTzSHgLpPSVUlCkOYM",
                    email="spammy@example.local",
                    role="student",
                    password_hash="hashed",
                    email_verified_at=None,
                    created_at=old,
                    updated_at=old,
                )
            )
            db.commit()

    def test_admin_bearer_can_list_and_update_user_roles(self):
        self.seed_users()
        client = self.client()

        listed = client.get("/api/admin/users", headers=self.auth_headers("user-admin"))
        promoted = client.patch(
            "/api/admin/users/user-student/role",
            headers=self.auth_headers("user-admin"),
            json={"role": "admin"},
        )
        self_demote = client.patch(
            "/api/admin/users/user-admin/role",
            headers=self.auth_headers("user-admin"),
            json={"role": "student"},
        )

        self.assertEqual(listed.status_code, 200)
        self.assertEqual(len(listed.json()["data"]), 3)
        self.assertEqual(promoted.status_code, 200)
        self.assertEqual(promoted.json()["data"]["role"], "admin")
        self.assertEqual(self_demote.status_code, 409)
        client.app.dependency_overrides.clear()

    def test_student_bearer_cannot_access_admin_routes(self):
        self.seed_users()
        client = self.client()

        response = client.get("/api/admin/users", headers=self.auth_headers("user-student"))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["detail"], "Admin role required")
        client.app.dependency_overrides.clear()

    def test_configured_admin_email_is_promoted_on_session_validation(self):
        self.seed_users()
        settings.admin_emails_raw = "owner@example.local"
        client = self.client()

        me = client.get("/api/auth/me", headers=self.auth_headers("user-bootstrap"))
        admin_route = client.get("/api/admin/users", headers=self.auth_headers("user-bootstrap"))

        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.json()["role"], "admin")
        self.assertEqual(admin_route.status_code, 200)
        client.app.dependency_overrides.clear()

    def test_admin_can_filter_and_bulk_delete_old_unverified_spam_users(self):
        self.seed_users()
        self.seed_spam_user()
        client = self.client()

        listed = client.get(
            "/api/admin/users?email_verified=false&min_account_age_days=30&suspicious_only=true",
            headers=self.auth_headers("user-admin"),
        )
        deleted = client.post(
            "/api/admin/users/bulk-delete",
            headers=self.auth_headers("user-admin"),
            json={"user_ids": ["user-spam"]},
        )
        search_after_delete = client.get(
            "/api/admin/users?search=spammy@example.local",
            headers=self.auth_headers("user-admin"),
        )

        self.assertEqual(listed.status_code, 200)
        self.assertEqual([user["id"] for user in listed.json()["data"]], ["user-spam"])
        self.assertTrue(listed.json()["data"][0]["looks_suspicious"])
        self.assertEqual(deleted.status_code, 200)
        self.assertEqual(deleted.json()["data"]["deleted"], 1)
        self.assertEqual(search_after_delete.status_code, 200)
        self.assertEqual(search_after_delete.json()["data"], [])
        client.app.dependency_overrides.clear()


if __name__ == "__main__":
    unittest.main()
