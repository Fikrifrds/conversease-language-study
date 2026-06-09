from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.admin_deps import AdminActor, require_admin_api_key
from app.db.exam_models import ExamItemModel, ExamSectionModel, ExamTemplateModel, MediaArtifactModel
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
from app.services.audio_generation import (
    AudioGenerationError,
    audio_generation_settings,
    find_lesson_audio_reference,
    generate_exam_item_listening_audio,
    generate_lesson_listening_audio,
    read_yaml_mapping,
)
from app.services.audio_preview_cache import get_or_generate_voice_preview, list_voice_preview_cache
from app.services.exam_service import ExamItemNotFoundError, ExamService


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


class AudioGenerationPayload(BaseModel):
    generated_by: Optional[str] = Field(default="admin", min_length=2, max_length=160)
    model: Optional[str] = Field(default=None, max_length=40)
    voice_id: Optional[str] = Field(default=None, max_length=160)
    speed: float = Field(default=1.0, ge=0.5, le=2.0)


class VoicePreviewPayload(BaseModel):
    generated_by: Optional[str] = Field(default="admin", min_length=2, max_length=160)
    model: Optional[str] = Field(default=None, max_length=40)
    voice_id: Optional[str] = Field(default=None, max_length=160)
    speed: float = Field(default=1.0, ge=0.5, le=2.0)
    sample_text: Optional[str] = Field(default=None, min_length=8, max_length=500)
    force: bool = False


class ExamAudioBulkGenerationPayload(BaseModel):
    generated_by: Optional[str] = Field(default="admin", min_length=2, max_length=160)
    model: Optional[str] = Field(default=None, max_length=40)
    voice_id: Optional[str] = Field(default=None, max_length=160)
    speed: float = Field(default=1.0, ge=0.5, le=2.0)
    only_missing: bool = True


@router.get("/admin/cms/summary")
async def get_cms_summary(
    _: AdminActor = Depends(require_admin_api_key),
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
    _: AdminActor = Depends(require_admin_api_key),
) -> dict:
    try:
        return {"data": get_admin_lesson(lesson_slug)}
    except AdminCmsError as exc:
        raise admin_cms_http_error(exc) from exc


@router.patch("/admin/cms/curriculum/lessons/{lesson_slug}")
async def patch_cms_lesson(
    lesson_slug: str,
    payload: AdminLessonUpdatePayload,
    admin: AdminActor = Depends(require_admin_api_key),
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
            changed_by=admin_display_name(payload.updated_by, admin),
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


@router.get("/admin/cms/audio/settings")
async def get_audio_generation_settings(
    _: AdminActor = Depends(require_admin_api_key),
) -> dict:
    return {"data": await audio_generation_settings()}


@router.post("/admin/cms/audio/voice-preview")
async def generate_cms_voice_preview_audio(
    payload: VoicePreviewPayload,
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    try:
        result = await get_or_generate_voice_preview(
            db,
            model=payload.model,
            voice_id=payload.voice_id,
            speed=payload.speed,
            sample_text=payload.sample_text,
            generated_by=admin_display_name(payload.generated_by, admin),
            force=payload.force,
        )
        return {"data": result}
    except AudioGenerationError as exc:
        raise audio_generation_http_error(exc) from exc


@router.get("/admin/cms/audio/voice-previews")
async def list_cms_voice_preview_audio(
    model: Optional[str] = Query(default=None, max_length=40),
    speed: Optional[float] = Query(default=None, ge=0.5, le=2.0),
    sample_text: Optional[str] = Query(default=None, min_length=8, max_length=500),
    _: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    try:
        return {
            "data": list_voice_preview_cache(
                db,
                model=model,
                speed=speed,
                sample_text=sample_text,
            )
        }
    except AudioGenerationError as exc:
        raise audio_generation_http_error(exc) from exc


@router.post("/admin/cms/curriculum/lessons/{lesson_slug}/audio/listening")
async def generate_cms_lesson_listening_audio(
    lesson_slug: str,
    payload: AudioGenerationPayload,
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    try:
        lesson_ref = find_lesson_audio_reference(lesson_slug)
        before_payload = {
            "lesson_slug": lesson_slug,
            "lesson_key": lesson_ref.lesson_key,
            "audio_manifest": read_yaml_mapping(lesson_ref.audio_manifest_path),
        }
        result = await generate_lesson_listening_audio(
            lesson_slug=lesson_slug,
            model=payload.model,
            voice_id=payload.voice_id,
            speed=payload.speed,
            generated_by=admin_display_name(payload.generated_by, admin),
        )
        revision = ContentRevisionRepository(db).record_revision(
            resource_type="curriculum_audio",
            resource_key=lesson_slug,
            action="generate",
            changed_by=admin_display_name(payload.generated_by, admin),
            before_payload=before_payload,
            after_payload=result,
            metadata={
                "source": "admin_cms_audio",
                "provider": "minimax",
                "model": result["model"],
                "voice_id": result["voice_id"],
                "storage_key": result["object_key"],
            },
        )
        return {
            "data": result,
            "revision": revision_payload(revision),
            "readiness_overview": curriculum_summary()["readiness_overview"],
        }
    except AudioGenerationError as exc:
        raise audio_generation_http_error(exc) from exc


@router.get("/admin/cms/exams/templates")
async def list_exam_audio_templates(
    status: Optional[str] = Query(default=None, max_length=32),
    _: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    query = select(ExamTemplateModel).order_by(ExamTemplateModel.created_at.desc())
    if status:
        query = query.where(ExamTemplateModel.status == status)

    templates = db.execute(query).scalars().all()
    return {"data": [serialize_exam_template_audio(template, db) for template in templates]}


@router.post("/admin/cms/exams/items/{item_id}/audio/listening")
async def generate_exam_item_audio(
    item_id: str,
    payload: AudioGenerationPayload,
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    service = ExamService(db)
    try:
        item = service.get_exam_item(item_id)
    except ExamItemNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    section = db.get(ExamSectionModel, item.section_id)
    template = db.get(ExamTemplateModel, item.exam_template_id)
    if section is None or template is None:
        raise HTTPException(status_code=404, detail="exam_item_dependencies_not_found")

    before_payload = serialize_exam_item_audio(item)
    try:
        result = await generate_exam_item_listening_audio(
            item=item,
            exam_template=template,
            section=section,
            model=payload.model,
            voice_id=payload.voice_id,
            speed=payload.speed,
            generated_by=admin_display_name(payload.generated_by, admin),
        )
    except AudioGenerationError as exc:
        raise audio_generation_http_error(exc) from exc

    service.update_exam_item_audio(
        item_id=item.id,
        stimulus_audio_url=result["audio_url"],
        audio_metadata={
            "playback_url": result["playback_url"],
            "object_key": result["object_key"],
            "duration_seconds": result["duration_seconds"],
            "audio_format": result["audio_format"],
            "audio_size": result["audio_size"],
            "provider": "minimax",
            "model": result["model"],
            "voice_id": result["voice_id"],
            "speaker_voices": result["speaker_voices"],
            "line_count": result["line_count"],
            "trace_id": result["trace_id"],
            "usage_characters": result["usage_characters"],
            "generated_by": result["generated_by"],
            "generated_at": result["generated_at"],
        },
    )

    now = datetime.utcnow()
    artifact = MediaArtifactModel(
        id=service._generate_id(),
        owner_type="exam_item",
        owner_id=item.id,
        artifact_type="listening_prompt_audio",
        file_url=result["audio_url"],
        object_key=result["object_key"],
        mime_type="audio/wav" if result["audio_format"] == "wav" else "audio/mpeg",
        file_size_bytes=result["audio_size"],
        duration_seconds=result["duration_seconds"],
        metadata_json={
            "template_id": template.id,
            "template_code": template.code,
            "section_id": section.id,
            "section_code": section.code,
            "provider": "minimax",
            "model": result["model"],
            "voice_id": result["voice_id"],
            "speaker_voices": result["speaker_voices"],
            "trace_id": result["trace_id"],
        },
        created_at=now,
        updated_at=now,
    )
    db.add(artifact)
    db.commit()

    updated_item = service.get_exam_item(item.id)
    revision = ContentRevisionRepository(db).record_revision(
        resource_type="exam_audio",
        resource_key=item.id,
        action="generate",
        changed_by=admin_display_name(payload.generated_by, admin),
        before_payload=before_payload,
        after_payload=serialize_exam_item_audio(updated_item),
        metadata={
            "source": "admin_exam_audio",
            "provider": "minimax",
            "model": result["model"],
            "voice_id": result["voice_id"],
            "storage_key": result["object_key"],
            "template_id": template.id,
            "template_code": template.code,
        },
    )
    return {"data": serialize_exam_item_audio(updated_item), "revision": revision_payload(revision)}


@router.post("/admin/cms/exams/templates/{template_id}/audio/listening")
async def generate_exam_template_audio(
    template_id: str,
    payload: ExamAudioBulkGenerationPayload,
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    template = db.get(ExamTemplateModel, template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="exam_template_not_found")

    section_ids = [
        section.id
        for section in db.execute(
            select(ExamSectionModel)
            .where(ExamSectionModel.exam_template_id == template_id)
            .where(ExamSectionModel.code == "LISTENING")
        )
        .scalars()
        .all()
    ]
    if not section_ids:
        raise HTTPException(status_code=422, detail="listening_section_not_found")

    query = (
        select(ExamItemModel)
        .where(ExamItemModel.section_id.in_(section_ids))
        .order_by(ExamItemModel.sequence_order.asc())
    )
    if payload.only_missing:
        query = query.where(ExamItemModel.stimulus_audio_url.is_(None))

    items = db.execute(query).scalars().all()
    results = []
    for item in items:
        result = await generate_exam_item_audio(
            item.id,
            AudioGenerationPayload(
                generated_by=payload.generated_by,
                model=payload.model,
                voice_id=payload.voice_id,
                speed=payload.speed,
            ),
            admin,
            db,
        )
        results.append(result["data"])

    return {
        "data": {
            "template_id": template.id,
            "template_code": template.code,
            "generated_count": len(results),
            "items": results,
        }
    }


@router.get("/admin/cms/email-templates/{template_key}")
async def get_cms_email_template(
    template_key: str,
    _: AdminActor = Depends(require_admin_api_key),
) -> dict:
    try:
        return {"data": get_email_template(template_key)}
    except AdminCmsError as exc:
        raise admin_cms_http_error(exc) from exc


@router.patch("/admin/cms/email-templates/{template_key}")
async def patch_cms_email_template(
    template_key: str,
    payload: EmailTemplateUpdatePayload,
    admin: AdminActor = Depends(require_admin_api_key),
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
            changed_by=admin_display_name(payload.updated_by, admin),
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
    _: AdminActor = Depends(require_admin_api_key),
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
    admin: AdminActor = Depends(require_admin_api_key),
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
            changed_by=admin_display_name(payload.restored_by, admin),
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


def audio_generation_http_error(exc: AudioGenerationError) -> HTTPException:
    detail = str(exc)
    if "not_found" in detail:
        return HTTPException(status_code=404, detail=detail)
    if "missing" in detail or detail.endswith("_config_missing"):
        return HTTPException(status_code=503, detail=detail)
    return HTTPException(status_code=422, detail=detail)


def verify_expected_content_hash(expected_content_hash: str, current_payload: dict) -> None:
    if expected_content_hash != current_payload.get("content_hash"):
        raise HTTPException(status_code=409, detail="content_changed_reload_required")


def admin_display_name(value: Optional[str], admin: AdminActor) -> str:
    clean_value = (value or "").strip()
    if clean_value and clean_value.lower() != "admin":
        return clean_value
    return admin.display_name


def serialize_exam_template_audio(template: ExamTemplateModel, db: Session) -> dict:
    sections = (
        db.execute(
            select(ExamSectionModel)
            .where(ExamSectionModel.exam_template_id == template.id)
            .order_by(ExamSectionModel.sequence_order.asc())
        )
        .scalars()
        .all()
    )
    listening_sections = [section for section in sections if section.code.upper() == "LISTENING"]
    listening_items = (
        db.execute(
            select(ExamItemModel)
            .where(ExamItemModel.section_id.in_([section.id for section in listening_sections] or [""]))
            .order_by(ExamItemModel.sequence_order.asc())
        )
        .scalars()
        .all()
    )
    return {
        "id": template.id,
        "code": template.code,
        "level_code": template.level_code,
        "title": template.title,
        "status": template.status,
        "duration_minutes": template.duration_minutes,
        "listening_item_count": len(listening_items),
        "listening_audio_ready_count": len([item for item in listening_items if item.stimulus_audio_url]),
        "listening_items": [serialize_exam_item_audio(item) for item in listening_items],
    }


def serialize_exam_item_audio(item: ExamItemModel) -> dict:
    audio_generation = (item.config_json or {}).get("audio_generation", {})
    return {
        "id": item.id,
        "section_id": item.section_id,
        "sequence_order": item.sequence_order,
        "item_type": item.item_type,
        "prompt_text": item.prompt_text,
        "stimulus_text": item.stimulus_text,
        "stimulus_audio_url": item.stimulus_audio_url,
        "audio_ready": bool(item.stimulus_audio_url),
        "audio_metadata": audio_generation if isinstance(audio_generation, dict) else {},
    }
