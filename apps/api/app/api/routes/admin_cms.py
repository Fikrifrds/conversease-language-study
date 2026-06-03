from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.admin_deps import require_admin_api_key
from app.db.session import get_db
from app.data.admin_cms import (
    AdminCmsError,
    curriculum_summary,
    get_admin_lesson,
    get_email_template,
    list_email_template_files,
    restore_email_template_from_snapshot,
    restore_lesson_from_snapshot,
    update_email_template,
    update_lesson_metadata,
)
from app.repositories.content_revisions import ContentRevisionRepository, revision_payload


router = APIRouter()


class AdminLessonUpdatePayload(BaseModel):
    updated_by: Optional[str] = Field(default="admin", min_length=2, max_length=160)
    expected_content_hash: str = Field(min_length=64, max_length=64)
    title: Optional[str] = Field(default=None, max_length=120)
    status: Optional[str] = Field(default=None, max_length=32)
    estimated_minutes: Optional[int] = Field(default=None, ge=1, le=120)
    conversation_goal: Optional[str] = Field(default=None, max_length=260)
    roleplay_opening_line: Optional[str] = Field(default=None, max_length=260)
    roleplay_learner_goal: Optional[str] = Field(default=None, max_length=320)
    roleplay_max_turns: Optional[int] = Field(default=None, ge=1, le=20)
    roleplay_target_phrases: Optional[list[str]] = None


class EmailTemplateUpdatePayload(BaseModel):
    updated_by: Optional[str] = Field(default="admin", min_length=2, max_length=160)
    expected_content_hash: str = Field(min_length=64, max_length=64)
    raw_body: str = Field(min_length=40, max_length=12000)


class ContentRevisionRollbackPayload(BaseModel):
    restored_by: Optional[str] = Field(default="admin", min_length=2, max_length=160)
    notes: Optional[str] = Field(default=None, max_length=1000)


@router.get("/admin/cms/summary")
async def get_cms_summary(
    _: bool = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    revisions = ContentRevisionRepository(db).list_revisions(limit=10)
    return {
        "data": {
            "curriculum": curriculum_summary(),
            "email_templates": list_email_template_files(),
            "recent_revisions": [revision_payload(revision) for revision in revisions],
        }
    }


@router.get("/admin/cms/curriculum/lessons/{lesson_slug}")
async def get_cms_lesson(
    lesson_slug: str,
    _: bool = Depends(require_admin_api_key),
) -> dict:
    try:
        return {"data": get_admin_lesson(lesson_slug)}
    except AdminCmsError as exc:
        raise admin_cms_http_error(exc) from exc


@router.patch("/admin/cms/curriculum/lessons/{lesson_slug}")
async def patch_cms_lesson(
    lesson_slug: str,
    payload: AdminLessonUpdatePayload,
    _: bool = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    try:
        before = get_admin_lesson(lesson_slug)
        verify_expected_content_hash(payload.expected_content_hash, before)
        lesson = update_lesson_metadata(
            lesson_slug,
            title=payload.title,
            status=payload.status,
            estimated_minutes=payload.estimated_minutes,
            conversation_goal=payload.conversation_goal,
            roleplay_opening_line=payload.roleplay_opening_line,
            roleplay_learner_goal=payload.roleplay_learner_goal,
            roleplay_max_turns=payload.roleplay_max_turns,
            roleplay_target_phrases=payload.roleplay_target_phrases,
        )
        revision = ContentRevisionRepository(db).record_revision(
            resource_type="curriculum_lesson",
            resource_key=lesson_slug,
            action="update",
            changed_by=payload.updated_by or "admin",
            before_payload=before,
            after_payload=lesson,
            metadata={"source": "admin_cms"},
        )
        return {
            "data": lesson,
            "revision": revision_payload(revision),
            "validation_issues": [],
        }
    except AdminCmsError as exc:
        raise admin_cms_http_error(exc) from exc


@router.get("/admin/cms/email-templates/{template_key}")
async def get_cms_email_template(
    template_key: str,
    _: bool = Depends(require_admin_api_key),
) -> dict:
    try:
        return {"data": get_email_template(template_key)}
    except AdminCmsError as exc:
        raise admin_cms_http_error(exc) from exc


@router.patch("/admin/cms/email-templates/{template_key}")
async def patch_cms_email_template(
    template_key: str,
    payload: EmailTemplateUpdatePayload,
    _: bool = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    try:
        before = get_email_template(template_key)
        verify_expected_content_hash(payload.expected_content_hash, before)
        template = update_email_template(template_key, payload.raw_body)
        revision = ContentRevisionRepository(db).record_revision(
            resource_type="email_template",
            resource_key=template_key,
            action="update",
            changed_by=payload.updated_by or "admin",
            before_payload=before,
            after_payload=template,
            metadata={"source": "admin_cms"},
        )
        return {"data": template, "revision": revision_payload(revision)}
    except AdminCmsError as exc:
        raise admin_cms_http_error(exc) from exc


@router.get("/admin/cms/revisions")
async def list_cms_revisions(
    resource_type: Optional[str] = Query(default=None, max_length=64),
    resource_key: Optional[str] = Query(default=None, max_length=240),
    limit: int = Query(default=50, ge=1, le=100),
    _: bool = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    revisions = ContentRevisionRepository(db).list_revisions(
        resource_type=resource_type,
        resource_key=resource_key,
        limit=limit,
    )
    return {"data": [revision_payload(revision) for revision in revisions]}


@router.post("/admin/cms/revisions/{revision_id}/rollback")
async def rollback_cms_revision(
    revision_id: str,
    payload: ContentRevisionRollbackPayload,
    _: bool = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    repository = ContentRevisionRepository(db)
    try:
        target_revision = repository.get_revision(revision_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="revision_not_found") from exc

    try:
        if target_revision.resource_type == "curriculum_lesson":
            before = get_admin_lesson(target_revision.resource_key)
            restored = restore_lesson_from_snapshot(
                target_revision.resource_key,
                target_revision.after_json,
            )
        elif target_revision.resource_type == "email_template":
            before = get_email_template(target_revision.resource_key)
            restored = restore_email_template_from_snapshot(
                target_revision.resource_key,
                target_revision.after_json,
            )
        else:
            raise AdminCmsError("unsupported_revision_resource_type")

        rollback_revision = repository.record_revision(
            resource_type=target_revision.resource_type,
            resource_key=target_revision.resource_key,
            action="rollback",
            changed_by=payload.restored_by or "admin",
            before_payload=before,
            after_payload=restored,
            metadata={
                "source": "admin_cms",
                "rollback_revision_id": target_revision.id,
                "rollback_revision_version": target_revision.version,
                "notes": payload.notes or "",
            },
        )
        return {
            "data": restored,
            "revision": revision_payload(rollback_revision),
            "rolled_back_from": revision_payload(target_revision),
        }
    except AdminCmsError as exc:
        raise admin_cms_http_error(exc) from exc


def admin_cms_http_error(exc: AdminCmsError) -> HTTPException:
    detail = str(exc)
    if "not_found" in detail:
        return HTTPException(status_code=404, detail=detail)
    return HTTPException(status_code=422, detail=detail)


def verify_expected_content_hash(expected_content_hash: str, current_payload: dict) -> None:
    if expected_content_hash != current_payload.get("content_hash"):
        raise HTTPException(status_code=409, detail="content_changed_reload_required")
