from dataclasses import dataclass
from datetime import datetime, timedelta
from hashlib import sha256
from secrets import token_urlsafe
from typing import Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AuthTokenModel


EMAIL_VERIFICATION_TOKEN = "email_verification"
PASSWORD_RESET_TOKEN = "password_reset"
GOOGLE_LOGIN_TOKEN = "google_login"


class InvalidAuthTokenError(Exception):
    pass


@dataclass(frozen=True)
class CreatedAuthToken:
    token: str
    expires_at: datetime


class AuthTokenRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_token(
        self,
        user_id: str,
        token_type: str,
        expires_delta: timedelta,
    ) -> CreatedAuthToken:
        now = datetime.utcnow()
        token = token_urlsafe(32)
        expires_at = now + expires_delta
        model = AuthTokenModel(
            id=f"atok-{uuid4().hex[:16]}",
            user_id=user_id,
            token_type=token_type,
            token_hash=hash_token(token),
            expires_at=expires_at,
            used_at=None,
            created_at=now,
        )
        self.db.add(model)
        self.db.commit()
        return CreatedAuthToken(token=token, expires_at=expires_at)

    def consume_token(self, token: str, token_type: str) -> AuthTokenModel:
        now = datetime.utcnow()
        model = self.db.execute(
            select(AuthTokenModel)
            .where(
                AuthTokenModel.token_hash == hash_token(token),
                AuthTokenModel.token_type == token_type,
            )
            .limit(1)
        ).scalar_one_or_none()

        if model is None or model.used_at is not None or model.expires_at <= now:
            raise InvalidAuthTokenError("Invalid or expired token")

        model.used_at = now
        self.db.commit()
        return model

    def latest_active_token(
        self,
        user_id: str,
        token_type: str,
        now: Optional[datetime] = None,
    ) -> Optional[AuthTokenModel]:
        now = now or datetime.utcnow()
        return self.db.execute(
            select(AuthTokenModel)
            .where(
                AuthTokenModel.user_id == user_id,
                AuthTokenModel.token_type == token_type,
                AuthTokenModel.used_at.is_(None),
                AuthTokenModel.expires_at > now,
            )
            .order_by(AuthTokenModel.created_at.desc())
            .limit(1)
        ).scalar_one_or_none()


def hash_token(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()
