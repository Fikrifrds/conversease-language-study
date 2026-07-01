#!/usr/bin/env python3
"""Migrate legacy local lesson visuals into the S3 visual library.

Runs as a dry-run unless --execute is supplied. Library assets are migrated
first; active overrides are migrated last so they remain the active pointer.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from app.core.config import settings
from app.services.lesson_visual_regeneration import (
    LessonVisualRegenerationError,
    VALID_SLOTS,
    ensure_visual_s3_configured,
    store_uploaded_lesson_visual,
)


def migration_targets(source_dir: Path) -> list[dict]:
    targets: list[dict] = []
    library_root = source_dir / "_library"
    if library_root.exists():
        for image_path in sorted(library_root.glob("*/*/*/image.png")):
            slug, slot, legacy_asset_id = image_path.relative_to(library_root).parts[:3]
            if slot not in VALID_SLOTS:
                continue
            targets.append(
                {
                    "slug": slug,
                    "slot": slot,
                    "path": image_path,
                    "model": "legacy-local-library",
                    "archive_reason": "migrated_local_library",
                    "legacy_asset_id": legacy_asset_id,
                    "active": False,
                }
            )

    for slug_dir in sorted(source_dir.iterdir() if source_dir.exists() else []):
        if not slug_dir.is_dir() or slug_dir.name.startswith("_"):
            continue
        for slot in VALID_SLOTS:
            image_path = slug_dir / f"{slot}.png"
            if image_path.exists():
                targets.append(
                    {
                        "slug": slug_dir.name,
                        "slot": slot,
                        "path": image_path,
                        "model": "legacy-local-active",
                        "archive_reason": "migrated_local_active",
                        "legacy_asset_id": "",
                        "active": True,
                    }
                )
    return targets


def migrate(*, source_dir: Path, execute: bool) -> dict:
    targets = migration_targets(source_dir)
    result = {
        "source_dir": str(source_dir),
        "dry_run": not execute,
        "target_count": len(targets),
        "migrated_count": 0,
        "failed": [],
        "targets": [
            {
                **{key: value for key, value in target.items() if key != "path"},
                "path": str(target["path"]),
            }
            for target in targets
        ],
    }
    if not execute:
        return result

    ensure_visual_s3_configured()
    for target in targets:
        try:
            stored = store_uploaded_lesson_visual(
                slug=target["slug"],
                slot=target["slot"],
                image_bytes=target["path"].read_bytes(),
                model=target["model"],
                archive_reason=target["archive_reason"],
            )
            result["migrated_count"] += 1
            target["new_asset_id"] = stored.library_asset_id
        except (OSError, LessonVisualRegenerationError) as exc:
            result["failed"].append(
                {
                    "path": str(target["path"]),
                    "error": str(exc),
                }
            )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path(settings.lesson_visual_overrides_dir),
        help="Legacy lesson-visual-overrides directory or mounted Docker volume.",
    )
    parser.add_argument("--execute", action="store_true", help="Perform S3 uploads.")
    args = parser.parse_args()
    result = migrate(source_dir=args.source_dir, execute=args.execute)
    print(json.dumps(result, indent=2, default=str))
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
