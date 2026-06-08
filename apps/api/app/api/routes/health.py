import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import API_ROOT, settings
from app.core.observability import runtime_metrics
from app.db.migration_status import (
    build_config,
    load_applied_revisions_from_connection,
    migration_head_check,
)
from app.db.session import get_db
from app.domain.ai import ChatMessage, ModelConfig
from app.domain.users import User
from app.services.llm import LLMError, get_llm_provider

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    return {
        "status": "ok",
        "service": "conversease-api",
        "environment": settings.app_env,
        "release_version": settings.release_version,
    }


@router.get("/metrics")
async def metrics_check() -> dict:
    return {
        "service": "conversease-api",
        "environment": settings.app_env,
        "release_version": settings.release_version,
        **runtime_metrics.snapshot(),
    }


@router.get("/health/llm")
async def llm_health_check(
    current_user: User = Depends(get_current_user),
) -> dict:
    provider = get_llm_provider()
    if provider is None:
        api_key_configured = bool(settings.openai_api_key) if settings.llm_default_provider == "openai" else bool(settings.together_api_key)
        return {
            "status": "disabled",
            "provider": settings.llm_default_provider,
            "api_key_configured": api_key_configured,
        }

    model = (
        settings.openai_chat_model
        if settings.llm_default_provider == "openai"
        else settings.together_chat_model
    )
    model_config = ModelConfig(
        provider=settings.llm_default_provider,
        model=model,
        temperature=0.0,
        max_tokens=50,
    )

    schema = {
        "type": "object",
        "properties": {"ok": {"type": "boolean"}},
        "required": ["ok"],
    }

    started = time.perf_counter()
    try:
        result = await provider.generate_chat_completion(
            messages=[
                ChatMessage(
                    role="user",
                    content='Return JSON only: {"ok": true}',
                )
            ],
            model_config=model_config,
            response_schema=schema,
        )
        duration_ms = round((time.perf_counter() - started) * 1000)
        return {
            "status": "ok",
            "provider": settings.llm_default_provider,
            "model": model,
            "duration_ms": duration_ms,
            "sample": result.content[:120],
        }
    except LLMError as exc:
        duration_ms = round((time.perf_counter() - started) * 1000)
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "provider": settings.llm_default_provider,
                "model": model,
                "duration_ms": duration_ms,
                "error": str(exc),
            },
        ) from exc


@router.get("/ready")
async def readiness_check(db: Session = Depends(get_db)) -> dict:
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Database is not ready") from exc

    migration_check = migration_readiness_check(db)
    if not migration_check["ok"]:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "not_ready",
                "service": "conversease-api",
                "checks": {
                    "database": "ok",
                    "migrations": "pending",
                    "applied_heads": migration_check["applied_heads"],
                    "expected_heads": migration_check["expected_heads"],
                    "pending_heads": migration_check["pending_heads"],
                    "unexpected_heads": migration_check["unexpected_heads"],
                },
            },
        )

    return {
        "status": "ready",
        "service": "conversease-api",
        "environment": settings.app_env,
        "release_version": settings.release_version,
        "checks": {
            "database": "ok",
            "migrations": "ok",
            "applied_heads": migration_check["applied_heads"],
            "expected_heads": migration_check["expected_heads"],
        },
    }


def migration_readiness_check(db: Session) -> dict[str, object]:
    config = build_config(str(API_ROOT / "alembic.ini"))
    applied_heads = load_applied_revisions_from_connection(db.connection())
    return migration_head_check(config, applied_heads)
