from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import Optional
from uuid import uuid4

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, waste_password_verification
from app.db.models import UserModel
from app.domain.users import User

USER_ROLE_STUDENT = "student"
USER_ROLE_ADMIN = "admin"
VALID_USER_ROLES = {USER_ROLE_STUDENT, USER_ROLE_ADMIN}


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(self, name: str, email: str, password: str) -> User:
        now = datetime.utcnow()
        model = UserModel(
            id=f"user-{uuid4().hex[:16]}",
            name=name.strip(),
            email=normalize_email(email),
            role=USER_ROLE_STUDENT,
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
                role=USER_ROLE_STUDENT,
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
            # Verify against a dummy hash anyway so a missing account takes the
            # same time as a wrong password, preventing user enumeration.
            waste_password_verification()
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

    def list_users(
        self,
        limit: int = 100,
        search: Optional[str] = None,
        email_verified: Optional[bool] = None,
        min_account_age_days: Optional[int] = None,
    ) -> list[User]:
        statement = select(UserModel)

        if search:
            pattern = f"%{search.strip()}%"
            statement = statement.where(
                or_(
                    UserModel.email.ilike(pattern),
                    UserModel.name.ilike(pattern),
                )
            )

        if email_verified is True:
            statement = statement.where(UserModel.email_verified_at.is_not(None))
        elif email_verified is False:
            statement = statement.where(UserModel.email_verified_at.is_(None))

        if min_account_age_days and min_account_age_days > 0:
            cutoff = datetime.utcnow() - timedelta(days=min_account_age_days)
            statement = statement.where(UserModel.created_at <= cutoff)

        statement = statement.order_by(UserModel.created_at.desc()).limit(limit)
        return [self._model_to_domain(model) for model in self.db.execute(statement).scalars().all()]

    def update_role(self, user_id: str, role: str) -> User:
        normalized_role = normalize_role(role)
        model = self.db.get(UserModel, user_id)
        if model is None:
            raise KeyError(user_id)

        model.role = normalized_role
        model.updated_at = datetime.utcnow()
        self.db.commit()
        return self._model_to_domain(model)

    def delete_user(self, user_id: str) -> None:
        model = self.db.get(UserModel, user_id)
        if model is None:
            raise KeyError(user_id)

        self.db.delete(model)
        self.db.commit()

    def delete_users(self, user_ids: list[str]) -> list[str]:
        deleted_ids: list[str] = []

        for user_id in dict.fromkeys(user_ids):
            model = self.db.get(UserModel, user_id)
            if model is None:
                continue
            self.db.delete(model)
            deleted_ids.append(user_id)

        self.db.commit()
        return deleted_ids

    def ensure_configured_admin_role(self, user: User, admin_emails: list[str]) -> User:
        configured_admin_emails = {normalize_email(email) for email in admin_emails if email.strip()}
        if normalize_email(user.email) not in configured_admin_emails or user.role == USER_ROLE_ADMIN:
            return user

        return self.update_role(user.id, USER_ROLE_ADMIN)

    def _model_to_domain(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            role=model.role or USER_ROLE_STUDENT,
            email_verified_at=model.email_verified_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_role(role: str) -> str:
    normalized = role.strip().lower()
    if normalized not in VALID_USER_ROLES:
        raise ValueError("invalid_user_role")
    return normalized
