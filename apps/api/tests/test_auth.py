import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.security import create_access_token, decode_access_token
from app.db.base import Base
from app.db import models  # noqa: F401
from app.repositories.users import UserRepository
from app.services.google_oauth import create_google_oauth_state, decode_google_oauth_state, google_profile_from_claims


class AuthTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)

    def test_user_password_is_hashed_and_authenticates(self):
        with self.SessionLocal() as db:
            repository = UserRepository(db)
            user = repository.create_user(
                name="Fikri",
                email="FIKRI@example.com",
                password="password123",
            )

            stored = repository.get_model_by_id(user.id)
            authenticated = repository.authenticate("fikri@example.com", "password123")

            self.assertNotEqual(stored.password_hash, "password123")
            self.assertEqual(user.email, "fikri@example.com")
            self.assertIsNone(user.email_verified_at)
            self.assertIsNotNone(authenticated)
            self.assertEqual(authenticated.id, user.id)
            self.assertIsNone(repository.authenticate("fikri@example.com", "wrong-password"))

    def test_access_token_roundtrip(self):
        token = create_access_token("user-123")

        self.assertEqual(decode_access_token(token), "user-123")

    def test_google_oauth_state_roundtrip_sanitizes_next_path(self):
        state = create_google_oauth_state("/lessons/saying-your-name")
        decoded = decode_google_oauth_state(state)

        self.assertEqual(decoded.next_path, "/lessons/saying-your-name")
        self.assertEqual(decode_google_oauth_state(create_google_oauth_state("//evil.test")).next_path, "/dashboard")

    def test_google_user_is_created_and_marks_verified_email(self):
        with self.SessionLocal() as db:
            repository = UserRepository(db)

            user = repository.get_or_create_google_user(
                name="Google User",
                email="GOOGLE@example.com",
                email_verified=True,
            )
            same_user = repository.get_or_create_google_user(
                name="Updated Name",
                email="google@example.com",
                email_verified=True,
            )

            self.assertEqual(user.id, same_user.id)
            self.assertEqual(user.email, "google@example.com")
            self.assertIsNotNone(same_user.email_verified_at)

    def test_google_profile_from_claims_normalizes_userinfo_payload(self):
        profile = google_profile_from_claims(
            {
                "sub": "google-subject",
                "email": "FIKRI@example.com",
                "name": "Fikri",
                "email_verified": "true",
            }
        )

        self.assertEqual(profile.email, "fikri@example.com")
        self.assertEqual(profile.name, "Fikri")
        self.assertTrue(profile.email_verified)


if __name__ == "__main__":
    unittest.main()
