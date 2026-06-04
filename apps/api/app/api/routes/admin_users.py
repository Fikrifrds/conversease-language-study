from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.admin_deps import AdminActor, require_admin_api_key
from app.db.session import get_db
from app.domain.users import User
from app.repositories.users import USER_ROLE_ADMIN, USER_ROLE_STUDENT, UserRepository, normalize_role


router = APIRouter()


class AdminUserRolePayload(BaseModel):
    role: str = Field(pattern=f"^({USER_ROLE_STUDENT}|{USER_ROLE_ADMIN})$")


def user_payload(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "email_verified_at": isoformat(user.email_verified_at),
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
    }


def isoformat(value: Optional[datetime]) -> Optional[str]:
    return value.isoformat() if value else None


@router.get("/admin/users")
async def list_admin_users(
    search: Optional[str] = Query(default=None, max_length=160),
    limit: int = Query(default=100, ge=1, le=200),
    _: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    users = UserRepository(db).list_users(limit=limit, search=search)
    return {"data": [user_payload(user) for user in users]}


@router.patch("/admin/users/{user_id}/role")
async def update_admin_user_role(
    user_id: str,
    payload: AdminUserRolePayload,
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    try:
        role = normalize_role(payload.role)
        if user_id == admin.id and role != USER_ROLE_ADMIN:
            raise HTTPException(status_code=409, detail="Cannot remove your own admin role")
        user = UserRepository(db).update_role(user_id, role)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Invalid role") from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="User not found") from exc

    return {"data": user_payload(user)}
