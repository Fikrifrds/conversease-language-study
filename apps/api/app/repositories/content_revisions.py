from __future__ import annotations

from datetime import datetime
from hashlib import sha256
import json
from typing import Any, Optional
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import ContentRevisionModel


class ContentRevisionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def record_revision(
        self,
        *,
        resource_type: str,
        resource_key: str,
        action: str,
        changed_by: str,
        after_payload: dict[str, Any],
        before_payload: Optional[dict[str, Any]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> ContentRevisionModel:
        next_version = self._next_version(resource_type, resource_key)
        clean_before_payload = (
            revision_content_payload(before_payload) if before_payload is not None else None
        )
        clean_after_payload = revision_content_payload(after_payload)
        revision = ContentRevisionModel(
            id=f"rev-{uuid4().hex[:16]}",
            resource_type=resource_type,
            resource_key=resource_key,
            version=next_version,
            action=action,
            changed_by=(changed_by.strip() or "admin")[:160],
            content_hash=content_hash(clean_after_payload),
            before_json=clean_before_payload,
            after_json=clean_after_payload,
            metadata_json=metadata or {},
            created_at=datetime.utcnow(),
        )
        self.db.add(revision)
        self.db.commit()
        return revision

    def latest_revision(
        self,
        *,
        resource_type: str,
        resource_key: str,
    ) -> Optional[ContentRevisionModel]:
        return self.db.execute(
            select(ContentRevisionModel)
            .where(
                ContentRevisionModel.resource_type == resource_type,
                ContentRevisionModel.resource_key == resource_key,
            )
            .order_by(ContentRevisionModel.version.desc())
            .limit(1)
        ).scalar_one_or_none()

    def get_revision(self, revision_id: str) -> ContentRevisionModel:
        revision = self.db.get(ContentRevisionModel, revision_id)
        if revision is None:
            raise KeyError(revision_id)
        return revision

    def list_revisions(
        self,
        *,
        resource_type: Optional[str] = None,
        resource_key: Optional[str] = None,
        limit: int = 50,
    ) -> list[ContentRevisionModel]:
        query = select(ContentRevisionModel)
        if resource_type:
            query = query.where(ContentRevisionModel.resource_type == resource_type)
        if resource_key:
            query = query.where(ContentRevisionModel.resource_key == resource_key)

        return (
            self.db.execute(query.order_by(ContentRevisionModel.created_at.desc()).limit(limit))
            .scalars()
            .all()
        )

    def _next_version(self, resource_type: str, resource_key: str) -> int:
        current_version = self.db.execute(
            select(func.max(ContentRevisionModel.version)).where(
                ContentRevisionModel.resource_type == resource_type,
                ContentRevisionModel.resource_key == resource_key,
            )
        ).scalar_one()
        return int(current_version or 0) + 1


def revision_payload(revision: ContentRevisionModel) -> dict[str, Any]:
    return {
        "id": revision.id,
        "resource_type": revision.resource_type,
        "resource_key": revision.resource_key,
        "version": revision.version,
        "action": revision.action,
        "changed_by": revision.changed_by,
        "content_hash": revision.content_hash,
        "metadata": revision.metadata_json,
        "created_at": revision.created_at.isoformat(),
    }


def content_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        revision_content_payload(payload),
        sort_keys=True,
        default=str,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def revision_content_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key != "content_hash"}
