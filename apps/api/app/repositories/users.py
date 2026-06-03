from datetime import datetime
from secrets import token_urlsafe
from typing import Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.db.models import UserModel
from app.domain.users import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(self, name: str, email: str, password: str) -> User:
        now = datetime.utcnow()
        model = UserModel(
            id=f"user-{uuid4().hex[:16]}",
            name=name.strip(),
            email=normalize_email(email),
            password_hash=hash_password(password),
            created_at=now,
            updated_at=now,
        )
        self.db.add(model)
        self.db.commit()
        return self._model_to_domain(model)

    def get_or_create_google_user(
        self,
        name: str,
        email: str,
        email_verified: bool,
    ) -> User:
        now = datetime.utcnow()
        model = self.get_model_by_email(email)

        if model is None:
            model = UserModel(
                id=f"user-{uuid4().hex[:16]}",
                name=name.strip() or normalize_email(email).split("@")[0],
                email=normalize_email(email),
                password_hash=hash_password(token_urlsafe(48)),
                email_verified_at=now if email_verified else None,
                created_at=now,
                updated_at=now,
            )
            self.db.add(model)
        else:
            model.name = model.name or name.strip()
            if email_verified and model.email_verified_at is None:
                model.email_verified_at = now
            model.updated_at = now

        self.db.commit()
        return self._model_to_domain(model)

    def get_by_id(self, user_id: str) -> Optional[User]:
        model = self.db.get(UserModel, user_id)
        return self._model_to_domain(model) if model else None

    def get_model_by_id(self, user_id: str) -> Optional[UserModel]:
        return self.db.get(UserModel, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        model = self.get_model_by_email(email)
        return self._model_to_domain(model) if model else None

    def get_model_by_email(self, email: str) -> Optional[UserModel]:
        return self.db.execute(
            select(UserModel).where(UserModel.email == normalize_email(email))
        ).scalar_one_or_none()

    def authenticate(self, email: str, password: str) -> Optional[User]:
        model = self.get_model_by_email(email)
        if model is None:
            return None
        if not verify_password(password, model.password_hash):
            return None
        return self._model_to_domain(model)

    def mark_email_verified(self, user_id: str, verified_at: Optional[datetime] = None) -> User:
        model = self.db.get(UserModel, user_id)
        if model is None:
            raise KeyError(user_id)

        now = verified_at or datetime.utcnow()
        model.email_verified_at = model.email_verified_at or now
        model.updated_at = now
        self.db.commit()
        return self._model_to_domain(model)

    def update_password(self, user_id: str, password: str) -> User:
        model = self.db.get(UserModel, user_id)
        if model is None:
            raise KeyError(user_id)

        now = datetime.utcnow()
        model.password_hash = hash_password(password)
        model.updated_at = now
        self.db.commit()
        return self._model_to_domain(model)

    def _model_to_domain(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            email_verified_at=model.email_verified_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


def normalize_email(email: str) -> str:
    return email.strip().lower()
