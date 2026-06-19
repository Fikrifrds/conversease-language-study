import unittest
import unittest.mock

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.routes.auth import validate_email, validate_password_strength
from app.core.security import create_access_token, decode_access_token
from app.db.base import Base
from app.db import models  # noqa: F401
from app.domain.users import name_looks_suspicious
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

    def test_authenticate_missing_user_still_verifies_to_equalize_timing(self):
        with self.SessionLocal() as db:
            repository = UserRepository(db)
            with unittest.mock.patch(
                "app.repositories.users.waste_password_verification"
            ) as waste:
                result = repository.authenticate("ghost@example.com", "password123")

            self.assertIsNone(result)
            waste.assert_called_once()

    def test_access_token_roundtrip(self):
        token = create_access_token("user-123")

        self.assertEqual(decode_access_token(token), "user-123")

    def test_validate_email_accepts_normal_addresses(self):
        self.assertEqual(validate_email("Fikri.Firdaus@Example.com"), "fikri.firdaus@example.com")
        self.assertEqual(validate_email("user+tag@sub.example.co.id"), "user+tag@sub.example.co.id")

    def test_validate_email_rejects_injection_and_spam_payloads(self):
        payloads = [
            "testing@example.com'||dbms_pipe.receive_message(chr(98)||chr(98)||chr(98),15)||'",
            "testing@example.comv8k2f6yq') or 801=(select 801 from pg_sleep(15))--",
            "testing@example.com-1 waitfor delay '0:0:15' --",
            "no-at-symbol.com",
            "spaces in@example.com",
            "trailing.dot@example.",
            "@example.com",
        ]
        for payload in payloads:
            with self.assertRaises(HTTPException, msg=payload) as ctx:
                validate_email(payload)
            self.assertEqual(ctx.exception.status_code, 422)

    def test_validate_password_strength_accepts_reasonable_passwords(self):
        for password in ["CorrectHorse9", "myDog$Rex2024", "sunset47beach"]:
            validate_password_strength(password)  # should not raise

    def test_validate_password_strength_rejects_weak_passwords(self):
        weak = [
            "password",      # common
            "password123",   # common
            "12345678",      # common + all digits
            "aaaaaaaa",      # <= 2 distinct chars
            "abababab",      # <= 2 distinct chars
            "19901990",      # all digits
            "letmeinplease",  # all letters
        ]
        for password in weak:
            with self.assertRaises(HTTPException, msg=password) as ctx:
                validate_password_strength(password)
            self.assertEqual(ctx.exception.status_code, 422)

    def test_register_rejects_bot_names(self):
        bots = [
            "mMFlPCiwwJYwWfsti",
            "DRSRQoBbtXEYlUBgNEOOgBFY",
            "QZgliFlBSLlPoAQSkIcXgixZ",
            "UlYJaxJpfztTPBzxlrJf",
            "iThQipySquPsQnKoMlUK",
            "pAEFlvwOZTiGpbbdd",
            "   ",
            "...",
        ]
        for name in bots:
            self.assertTrue(name_looks_suspicious(name, "stolen@hotmail.com"), msg=name)

    def test_register_allows_real_names_including_non_latin_scripts(self):
        real = [
            "Fikri Firdaus",
            "Budi Santoso",
            "Li Wang",
            "McDonald",
            "JoAnne",
            "García",
            "Müller",
            "王伟",
            "أحمد",
            "محمد علي",
            "Иван",
        ]
        for name in real:
            self.assertFalse(name_looks_suspicious(name, "real.person@gmail.com"), msg=name)

    def test_google_login_does_not_run_name_check(self):
        # Google has already verified the human, so the gibberish-name heuristic
        # must not gate the Google flow even if Google returns an unusual name.
        with self.SessionLocal() as db:
            user = UserRepository(db).get_or_create_google_user(
                name="mMFlPCiwwJYwWfsti",
                email="real.google.user@gmail.com",
                email_verified=True,
            )
            self.assertEqual(user.name, "mMFlPCiwwJYwWfsti")
            self.assertIsNotNone(user.email_verified_at)

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
