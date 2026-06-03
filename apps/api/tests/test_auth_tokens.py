from datetime import timedelta
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import models  # noqa: F401
from app.db.base import Base
from app.repositories.auth_tokens import (
    EMAIL_VERIFICATION_TOKEN,
    PASSWORD_RESET_TOKEN,
    AuthTokenRepository,
    InvalidAuthTokenError,
)
from app.repositories.users import UserRepository


class AuthTokenRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)

    def test_email_verification_token_marks_user_verified_once(self):
        with self.SessionLocal() as db:
            users = UserRepository(db)
            tokens = AuthTokenRepository(db)
            user = users.create_user("Fikri", "fikri@example.com", "password123")
            created = tokens.create_token(
                user_id=user.id,
                token_type=EMAIL_VERIFICATION_TOKEN,
                expires_delta=timedelta(hours=24),
            )

            consumed = tokens.consume_token(created.token, EMAIL_VERIFICATION_TOKEN)
            verified_user = users.mark_email_verified(consumed.user_id)

            self.assertIsNotNone(verified_user.email_verified_at)

            with self.assertRaises(InvalidAuthTokenError):
                tokens.consume_token(created.token, EMAIL_VERIFICATION_TOKEN)

    def test_password_reset_token_updates_password_once(self):
        with self.SessionLocal() as db:
            users = UserRepository(db)
            tokens = AuthTokenRepository(db)
            user = users.create_user("Fikri", "fikri@example.com", "password123")
            created = tokens.create_token(
                user_id=user.id,
                token_type=PASSWORD_RESET_TOKEN,
                expires_delta=timedelta(minutes=60),
            )

            consumed = tokens.consume_token(created.token, PASSWORD_RESET_TOKEN)
            users.update_password(consumed.user_id, "newpassword123")

            self.assertIsNone(users.authenticate("fikri@example.com", "password123"))
            self.assertIsNotNone(users.authenticate("fikri@example.com", "newpassword123"))

            with self.assertRaises(InvalidAuthTokenError):
                tokens.consume_token(created.token, PASSWORD_RESET_TOKEN)


if __name__ == "__main__":
    unittest.main()
