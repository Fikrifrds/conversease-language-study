from __future__ import annotations

from dataclasses import dataclass
import hmac
from typing import Optional

from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_access_token
from app.db.session import get_db
from app.domain.users import User
from app.repositories.users import USER_ROLE_ADMIN, UserRepository
from app.api.deps import bearer_scheme


@dataclass(frozen=True)
class AdminActor:
    id: str
    name: str
    email: str
    role: str
    auth_method: str

    @property
    def display_name(self) -> str:
        if self.name:
            return self.name
        if self.email:
            return self.email
        return "admin"


def admin_actor_from_user(user: User) -> AdminActor:
    return AdminActor(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        auth_method="bearer",
    )


def admin_actor_from_api_key() -> AdminActor:
    return AdminActor(
        id="admin-api-key",
        name="Admin API Key",
        email=settings.payment_admin_email,
        role=USER_ROLE_ADMIN,
        auth_method="api_key",
    )


def valid_admin_api_key(x_admin_api_key: Optional[str]) -> bool:
    return bool(
        settings.payment_admin_api_key
        and x_admin_api_key
        and hmac.compare_digest(x_admin_api_key, settings.payment_admin_api_key)
    )


def require_admin_access(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    x_admin_api_key: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
) -> AdminActor:
    bearer_status = 401
    bearer_detail = "Admin authentication required"

    if credentials is not None and credentials.scheme.lower() == "bearer":
        try:
            user_id = decode_access_token(credentials.credentials)
            repository = UserRepository(db)
            user = repository.get_by_id(user_id)
            if user is None:
                bearer_detail = "User not found"
            else:
                user = repository.ensure_configured_admin_role(user, settings.admin_emails)
                if user.role == USER_ROLE_ADMIN:
                    return admin_actor_from_user(user)
                bearer_status = 403
                bearer_detail = "Admin role required"
        except ValueError:
            bearer_detail = "Invalid token"

    if valid_admin_api_key(x_admin_api_key):
        return admin_actor_from_api_key()

    if credentials is not None:
        raise HTTPException(status_code=bearer_status, detail=bearer_detail)

    raise HTTPException(status_code=401, detail="Admin authentication required")


def require_admin_api_key(
    admin_actor: AdminActor = Depends(require_admin_access),
) -> AdminActor:
    return admin_actor
