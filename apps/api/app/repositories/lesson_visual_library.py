from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import (
    LessonVisualActiveModel,
    LessonVisualAssetModel,
    VisualPlacementModel,
)


def register_visual_asset(
    db: Session,
    *,
    asset_id: str,
    content_hash: str,
    storage_key: str,
    preview_storage_key: str,
    source_lesson_slug: Optional[str],
    source_slot: str,
    model: str,
    archive_reason: str,
    width: int,
    height: int,
    byte_count: int,
    description: dict,
    prompt_text: Optional[str],
    created_at: datetime,
) -> LessonVisualAssetModel:
    existing = db.scalar(
        select(LessonVisualAssetModel).where(
            LessonVisualAssetModel.content_hash == content_hash
        )
    )
    if existing is not None:
        return existing

    asset = LessonVisualAssetModel(
        id=asset_id,
        content_hash=content_hash,
        storage_key=storage_key,
        preview_storage_key=preview_storage_key,
        mime_type="image/png",
        source_lesson_slug=source_lesson_slug,
        source_slot=source_slot,
        model=model,
        archive_reason=archive_reason,
        width=width,
        height=height,
        byte_count=byte_count,
        description_json=description,
        prompt_text=prompt_text,
        created_at=created_at,
    )
    try:
        with db.begin_nested():
            db.add(asset)
            db.flush()
        return asset
    except IntegrityError:
        existing = db.scalar(
            select(LessonVisualAssetModel).where(
                LessonVisualAssetModel.content_hash == content_hash
            )
        )
        if existing is None:
            raise
        return existing


def activate_visual_asset(
    db: Session,
    *,
    lesson_slug: str,
    slot: str,
    asset_id: str,
    only_if_missing: bool = False,
) -> None:
    active = db.scalar(
        select(LessonVisualActiveModel).where(
            LessonVisualActiveModel.lesson_slug == lesson_slug,
            LessonVisualActiveModel.slot == slot,
        )
    )
    now = datetime.now(timezone.utc)
    if active is None:
        db.add(
            LessonVisualActiveModel(
                id=uuid4().hex,
                lesson_slug=lesson_slug,
                slot=slot,
                asset_id=asset_id,
                updated_at=now,
            )
        )
    else:
        if only_if_missing:
            return
        active.asset_id = asset_id
        active.updated_at = now
    sync_following_visual_placements(
        db,
        lesson_slug=lesson_slug,
        slot=slot,
        asset_id=asset_id,
        updated_at=now,
    )


def sync_following_visual_placements(
    db: Session,
    *,
    lesson_slug: str,
    slot: str,
    asset_id: str,
    updated_at: Optional[datetime] = None,
) -> int:
    placements = list(
        db.scalars(
            select(VisualPlacementModel).where(
                VisualPlacementModel.mode == "follow_lesson",
                VisualPlacementModel.source_lesson_slug == lesson_slug,
                VisualPlacementModel.source_slot == slot,
            )
        ).all()
    )
    now = updated_at or datetime.now(timezone.utc)
    for placement in placements:
        placement.asset_id = asset_id
        placement.updated_at = now
    return len(placements)


def list_visual_assets(db: Session, *, slot: str) -> list[LessonVisualAssetModel]:
    query = select(LessonVisualAssetModel)
    if slot == "hero":
        query = query.where(LessonVisualAssetModel.source_slot == "hero")
    else:
        query = query.where(LessonVisualAssetModel.source_slot.like("card-%"))
    return list(db.scalars(query.order_by(LessonVisualAssetModel.created_at.desc())).all())


def get_visual_asset(
    db: Session, *, asset_id: str
) -> Optional[LessonVisualAssetModel]:
    return db.get(LessonVisualAssetModel, asset_id)


def get_visual_asset_by_hash(
    db: Session, *, content_hash: str
) -> Optional[LessonVisualAssetModel]:
    return db.scalar(
        select(LessonVisualAssetModel).where(
            LessonVisualAssetModel.content_hash == content_hash
        )
    )


def get_active_visual_asset(
    db: Session, *, lesson_slug: str, slot: str
) -> Optional[LessonVisualAssetModel]:
    return db.scalar(
        select(LessonVisualAssetModel)
        .join(
            LessonVisualActiveModel,
            LessonVisualActiveModel.asset_id == LessonVisualAssetModel.id,
        )
        .where(
            LessonVisualActiveModel.lesson_slug == lesson_slug,
            LessonVisualActiveModel.slot == slot,
        )
    )


def assign_visual_placement(
    db: Session,
    *,
    owner_type: str,
    owner_key: str,
    slot: str,
    asset_id: str,
    mode: str = "follow_lesson",
    source_lesson_slug: Optional[str] = None,
    source_slot: Optional[str] = None,
) -> None:
    placement = db.scalar(
        select(VisualPlacementModel).where(
            VisualPlacementModel.owner_type == owner_type,
            VisualPlacementModel.owner_key == owner_key,
            VisualPlacementModel.slot == slot,
        )
    )
    now = datetime.now(timezone.utc)
    if placement is None:
        db.add(
            VisualPlacementModel(
                id=uuid4().hex,
                owner_type=owner_type,
                owner_key=owner_key,
                slot=slot,
                mode=mode,
                source_lesson_slug=source_lesson_slug,
                source_slot=source_slot,
                asset_id=asset_id,
                updated_at=now,
            )
        )
    else:
        if placement.mode == "pinned" and mode == "follow_lesson":
            return
        placement.asset_id = asset_id
        placement.mode = mode
        placement.source_lesson_slug = source_lesson_slug
        placement.source_slot = source_slot
        placement.updated_at = now


def list_visual_placements(
    db: Session,
) -> list[tuple[VisualPlacementModel, LessonVisualAssetModel]]:
    return list(
        db.execute(
            select(VisualPlacementModel, LessonVisualAssetModel)
            .join(
                LessonVisualAssetModel,
                LessonVisualAssetModel.id == VisualPlacementModel.asset_id,
            )
            .order_by(
                VisualPlacementModel.owner_type,
                VisualPlacementModel.owner_key,
                VisualPlacementModel.slot,
            )
        ).all()
    )
