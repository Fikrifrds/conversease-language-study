"""Admin AI diagnostics.

Lets operators verify from production which AI integrations are active:
LLM feedback (Conversation Coach), speech-to-text, and TTS. Mirrors the
admin email diagnostics pattern.
"""
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.api.admin_deps import AdminActor, require_admin_api_key
from app.core.config import settings
from app.core.llm_usage import llm_usage_registry
from app.db.session import get_db
from app.domain.ai import TASK_MODEL_CONFIGS, ChatMessage
from app.services.llm import LLMError, get_llm_provider
from app.services.lesson_visual_regeneration import (
    LessonVisualRegenerationError,
    MAX_IMAGE_BYTES,
    RegeneratedLessonVisual,
    get_active_lesson_visual,
    image_generation_dimensions,
    import_lesson_visual_from_url,
    list_lesson_visual_library,
    regenerate_lesson_visual,
    resolve_lesson_visual_prompt,
    select_lesson_visual_asset,
    upload_lesson_visual,
)

router = APIRouter()


class LessonVisualUrlPayload(BaseModel):
    url: str = Field(min_length=8, max_length=4096)


class LessonVisualLibrarySelectionPayload(BaseModel):
    asset_id: str = Field(min_length=8, max_length=120)


@router.get("/admin/ai/status")
async def get_ai_status(_: bool = Depends(require_admin_api_key)) -> dict:
    """Report which AI providers are configured (no external calls)."""
    llm_provider = get_llm_provider()
    stt_configured = (
        bool(settings.assemblyai_api_key)
        if settings.stt_provider == "assemblyai"
        else bool(settings.together_api_key)
    )
    return {
        "data": {
            "llm": {
                "configured": llm_provider is not None,
                "provider": settings.llm_default_provider,
                "feedback_model": TASK_MODEL_CONFIGS["conversation_feedback"].model,
                "partner_model": TASK_MODEL_CONFIGS["conversation_partner_reply"].model,
            },
            "stt": {
                "configured": stt_configured,
                "provider": settings.stt_provider,
            },
            "tts": {
                "configured": bool(settings.minimax_api_key),
                "provider": "minimax",
            },
            "image": {
                "configured": bool(settings.together_api_key),
                "provider": "together",
                "model": settings.together_image_model,
            },
        }
    }


@router.post("/admin/ai/test-llm")
async def test_llm_completion(_: bool = Depends(require_admin_api_key)) -> dict:
    """Run one tiny live completion to prove the LLM provider works end to end."""
    provider = get_llm_provider()
    if provider is None:
        raise HTTPException(status_code=503, detail="llm_not_configured")

    try:
        result = await provider.generate_chat_completion(
            messages=[
                ChatMessage(role="system", content="Reply with exactly: OK"),
                ChatMessage(role="user", content="Health check"),
            ],
            model_config=TASK_MODEL_CONFIGS["conversation_feedback"],
        )
    except LLMError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return {
        "data": {
            "provider": settings.llm_default_provider,
            "model": TASK_MODEL_CONFIGS["conversation_feedback"].model,
            "output": result.content.strip()[:200],
        }
    }


@router.get("/admin/ai/usage")
async def get_ai_usage(_: bool = Depends(require_admin_api_key)) -> dict:
    """Aggregated LLM token usage and estimated cost since the process started.

    In-memory and per-process (resets on restart); for live cost visibility.
    """
    return {"data": llm_usage_registry.snapshot()}


@router.post("/admin/lessons/{slug}/visuals/{slot}/regenerate")
async def regenerate_admin_lesson_visual(
    slug: str,
    slot: str,
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    """Generate one lesson image from its reviewed prompt and replace its override atomically."""
    try:
        result = await regenerate_lesson_visual(slug=slug, slot=slot, db=db)
    except LessonVisualRegenerationError as exc:
        raise lesson_visual_http_error(exc) from exc

    return lesson_visual_response(result=result, generated_by=admin.display_name)


@router.get("/admin/lessons/{slug}/visuals/{slot}/prompt")
async def get_admin_lesson_visual_prompt(
    slug: str,
    slot: str,
    _: AdminActor = Depends(require_admin_api_key),
) -> dict:
    try:
        _, prompt = resolve_lesson_visual_prompt(slug=slug, slot=slot)
    except LessonVisualRegenerationError as exc:
        raise lesson_visual_http_error(exc) from exc
    width, height = image_generation_dimensions(slot)
    return {
        "data": {
            "slug": slug,
            "slot": slot,
            "prompt": prompt,
            "width": width,
            "height": height,
        }
    }


@router.post("/admin/lessons/{slug}/visuals/{slot}/upload")
async def upload_admin_lesson_visual(
    slug: str,
    slot: str,
    image: UploadFile = File(...),
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    image_bytes = await image.read(MAX_IMAGE_BYTES + 1)
    try:
        result = await run_in_threadpool(
            upload_lesson_visual,
            slug=slug,
            slot=slot,
            image_bytes=image_bytes,
            db=db,
        )
    except LessonVisualRegenerationError as exc:
        raise lesson_visual_http_error(exc) from exc
    return lesson_visual_response(result=result, generated_by=admin.display_name)


@router.post("/admin/lessons/{slug}/visuals/{slot}/upload-url")
async def upload_admin_lesson_visual_from_url(
    slug: str,
    slot: str,
    payload: LessonVisualUrlPayload,
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    try:
        result = await import_lesson_visual_from_url(
            slug=slug,
            slot=slot,
            url=payload.url,
            db=db,
        )
    except LessonVisualRegenerationError as exc:
        raise lesson_visual_http_error(exc) from exc
    return lesson_visual_response(result=result, generated_by=admin.display_name)


@router.get("/admin/lessons/{slug}/visuals/{slot}/library")
async def get_admin_lesson_visual_library(
    slug: str,
    slot: str,
    _: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    try:
        library = await run_in_threadpool(
            list_lesson_visual_library, slug=slug, slot=slot, db=db
        )
    except LessonVisualRegenerationError as exc:
        raise lesson_visual_http_error(exc) from exc
    return {"data": library}


@router.post("/admin/lessons/{slug}/visuals/{slot}/library/select")
async def select_admin_lesson_visual_library_asset(
    slug: str,
    slot: str,
    payload: LessonVisualLibrarySelectionPayload,
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    try:
        result = await run_in_threadpool(
            select_lesson_visual_asset,
            slug=slug,
            slot=slot,
            asset_id=payload.asset_id,
            db=db,
        )
    except LessonVisualRegenerationError as exc:
        raise lesson_visual_http_error(exc) from exc
    return lesson_visual_response(result=result, generated_by=admin.display_name)


@router.get("/lesson-visuals/{slug}/{slot}/active")
async def get_public_active_lesson_visual(
    slug: str, slot: str, db: Session = Depends(get_db)
) -> dict:
    try:
        active = await run_in_threadpool(
            get_active_lesson_visual, slug=slug, slot=slot, db=db
        )
    except LessonVisualRegenerationError as exc:
        raise lesson_visual_http_error(exc) from exc
    if active is None:
        raise HTTPException(status_code=404, detail="lesson_visual_active_not_found")
    return {"data": active}


def lesson_visual_response(*, result: RegeneratedLessonVisual, generated_by: str) -> dict:
    return {
        "data": {
            "slug": result.slug,
            "slot": result.slot,
            "model": result.model,
            "version": result.version,
            "byte_count": result.byte_count,
            "library_asset_id": result.library_asset_id,
            "library_relative_path": result.library_relative_path,
            "asset_url": f"/lesson-visuals/{result.slug}/{result.slot}?v={result.version}",
            "generated_by": generated_by,
        }
    }


def lesson_visual_http_error(exc: LessonVisualRegenerationError) -> HTTPException:
    if exc.code == "uploaded_image_size_invalid":
        return HTTPException(status_code=413, detail=exc.code)
    if exc.code in {
        "invalid_lesson_slug",
        "invalid_visual_slot",
        "lesson_visual_prompt_invalid",
        "uploaded_image_format_invalid",
        "uploaded_image_aspect_ratio_invalid",
        "remote_image_url_invalid",
        "remote_image_url_forbidden",
        "remote_image_content_type_invalid",
    }:
        return HTTPException(status_code=400, detail=exc.code)
    if exc.code in {
        "lesson_visual_prompt_not_found",
        "lesson_visual_prompt_section_not_found",
        "lesson_visual_library_asset_not_found",
    }:
        return HTTPException(status_code=404, detail=exc.code)
    if exc.code in {"together_api_key_missing", "s3_config_missing"}:
        return HTTPException(status_code=503, detail=exc.code)
    if exc.code in {
        "remote_image_auth_required",
        "remote_image_download_failed",
        "remote_image_too_many_redirects",
    }:
        return HTTPException(status_code=502, detail=exc.code)
    if exc.code.startswith("together_") or exc.code.startswith("generated_image_"):
        return HTTPException(status_code=502, detail=exc.code)
    if exc.code.startswith("s3_visual_") or exc.code == "boto3_missing":
        return HTTPException(status_code=502, detail=exc.code)
    return HTTPException(status_code=500, detail="lesson_visual_regeneration_failed")
