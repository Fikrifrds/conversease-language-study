from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.admin_deps import AdminActor, require_admin_api_key
from app.db.session import get_db
from app.domain.users import User, name_looks_suspicious
from app.repositories.users import USER_ROLE_ADMIN, USER_ROLE_STUDENT, UserRepository, normalize_role


router = APIRouter()


class AdminUserRolePayload(BaseModel):
    role: str = Field(pattern=f"^({USER_ROLE_STUDENT}|{USER_ROLE_ADMIN})$")


class AdminBulkDeleteUsersPayload(BaseModel):
    user_ids: list[str] = Field(min_length=1, max_length=100)


def user_payload(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "looks_suspicious": looks_suspicious_user(user),
        "email_verified_at": isoformat(user.email_verified_at),
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
    }


def isoformat(value: Optional[datetime]) -> Optional[str]:
    return value.isoformat() if value else None


def looks_suspicious_user(user: User) -> bool:
    return name_looks_suspicious(user.name, user.email)


@router.get("/admin/users")
async def list_admin_users(
    search: Optional[str] = Query(default=None, max_length=160),
    limit: int = Query(default=100, ge=1, le=200),
    email_verified: Optional[bool] = Query(default=None),
    min_account_age_days: Optional[int] = Query(default=None, ge=1, le=3650),
    suspicious_only: bool = Query(default=False),
    _: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    repository = UserRepository(db)
    fetch_limit = min(limit * 5, 1000) if suspicious_only else limit
    users = repository.list_users(
        limit=fetch_limit,
        search=search,
        email_verified=email_verified,
        min_account_age_days=min_account_age_days,
    )
    if suspicious_only:
        users = [user for user in users if looks_suspicious_user(user)][:limit]
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


@router.delete("/admin/users/{user_id}")
async def delete_admin_user(
    user_id: str,
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    repository = UserRepository(db)
    user = repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id == admin.id:
        raise HTTPException(status_code=409, detail="Cannot delete your own account")
    if user.role == USER_ROLE_ADMIN:
        raise HTTPException(status_code=409, detail="Cannot delete another admin account")

    repository.delete_user(user_id)
    return {"data": {"deleted": True, "user_id": user_id}}


@router.post("/admin/users/bulk-delete")
async def bulk_delete_admin_users(
    payload: AdminBulkDeleteUsersPayload,
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    repository = UserRepository(db)
    candidate_ids = [user_id.strip() for user_id in payload.user_ids if user_id.strip()]
    if not candidate_ids:
        raise HTTPException(status_code=422, detail="No user ids provided")

    users = [repository.get_by_id(user_id) for user_id in dict.fromkeys(candidate_ids)]
    protected_users = [
        user for user in users if user is not None and (user.id == admin.id or user.role == USER_ROLE_ADMIN)
    ]
    if protected_users:
        raise HTTPException(status_code=409, detail="Admin accounts cannot be deleted in bulk")

    deleted_ids = repository.delete_users(candidate_ids)
    return {"data": {"deleted": len(deleted_ids), "user_ids": deleted_ids}}
