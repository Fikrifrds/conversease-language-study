from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import API_ROOT, settings
from app.core.observability import runtime_metrics
from app.db.migration_status import (
    build_config,
    load_applied_revisions_from_connection,
    migration_head_check,
)
from app.db.session import get_db

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
