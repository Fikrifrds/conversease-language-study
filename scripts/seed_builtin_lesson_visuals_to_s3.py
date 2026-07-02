#!/usr/bin/env python3
"""Seed built-in lesson visuals into the global S3-backed visual library.

Runs as a dry-run unless --execute is supplied. Binary files are deduplicated
by SHA-256 in the database, while every lesson/slot receives its own active
assignment. Re-running --execute is safe.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys

import yaml

from app.db.session import get_sessionmaker
from app.repositories.lesson_visual_library import (
    activate_visual_asset,
    assign_visual_placement,
    get_active_visual_asset,
    get_visual_asset,
)
from app.services.lesson_visual_regeneration import (
    LessonVisualRegenerationError,
    REPO_ROOT,
    ensure_visual_s3_configured,
    store_uploaded_lesson_visual,
)


CURRICULUM_ROOT = REPO_ROOT / "content" / "curriculum"
PUBLIC_ROOT = REPO_ROOT / "apps" / "web" / "public"


def seed_targets() -> list[dict]:
    targets: list[dict] = []
    for lesson_yaml in sorted(
        (CURRICULUM_ROOT / "english").glob("*/units/*/*/lesson.yaml")
    ):
        lesson = yaml.safe_load(lesson_yaml.read_text(encoding="utf-8")) or {}
        slug = str(lesson.get("slug") or "").strip()
        visuals_path = lesson_yaml.parent / "visuals.yaml"
        if not slug or not visuals_path.exists():
            continue
        visuals = yaml.safe_load(visuals_path.read_text(encoding="utf-8")) or {}
        items = [("hero", visuals.get("hero"))]
        items.extend(
            (f"card-{index}", item)
            for index, item in enumerate(visuals.get("cards") or [], start=1)
        )
        for slot, item in items:
            if not isinstance(item, dict):
                continue
            source_url = str(item.get("src") or "")
            if not source_url.startswith("/images/"):
                continue
            source_path = PUBLIC_ROOT / source_url.lstrip("/")
            if not source_path.is_file():
                continue
            targets.append(
                {
                    "slug": slug,
                    "slot": slot,
                    "source_url": source_url,
                    "source_path": source_path,
                }
            )
    return targets


def course_placement_sources() -> list[dict]:
    visuals_by_slug: dict[str, dict[str, str]] = {}
    for lesson_yaml in sorted(CURRICULUM_ROOT.glob("*/*/units/*/*/lesson.yaml")):
        lesson = yaml.safe_load(lesson_yaml.read_text(encoding="utf-8")) or {}
        slug = str(lesson.get("slug") or "").strip()
        visuals_path = lesson_yaml.parent / "visuals.yaml"
        if not slug or not visuals_path.exists():
            continue
        visuals = yaml.safe_load(visuals_path.read_text(encoding="utf-8")) or {}
        hero = visuals.get("hero") or {}
        cards = visuals.get("cards") or []
        slot_sources = {"hero": str(hero.get("src") or "")}
        slot_sources.update(
            {
                f"card-{index}": str(item.get("src") or "")
                for index, item in enumerate(cards, start=1)
                if isinstance(item, dict)
            }
        )
        visuals_by_slug[slug] = slot_sources

    placements: list[dict] = []
    for plan_path in sorted(CURRICULUM_ROOT.glob("*/*/content_plan.yaml")):
        plan = yaml.safe_load(plan_path.read_text(encoding="utf-8")) or {}
        course_slug = str(plan.get("course_slug") or "").strip()
        units = plan.get("units") or []
        if not course_slug or not isinstance(units, list):
            continue

        course_visuals: list[dict] = []
        for unit in units:
            if not isinstance(unit, dict):
                continue
            unit_key = str(unit.get("unit_key") or "").strip()
            lessons = unit.get("lessons") or []
            lesson_slugs = [
                str(item.get("slug") or "").strip()
                for item in lessons
                if isinstance(item, dict) and item.get("slug")
            ]
            sources: list[dict] = []
            seen_urls: set[str] = set()
            for lesson_slug in lesson_slugs:
                hero_source = visuals_by_slug.get(lesson_slug, {}).get("hero", "")
                if hero_source and hero_source not in seen_urls:
                    sources.append(
                        {
                            "source_url": hero_source,
                            "source_lesson_slug": lesson_slug,
                            "source_slot": "hero",
                        }
                    )
                    seen_urls.add(hero_source)
                if len(sources) == 3:
                    break
            if lesson_slugs and len(sources) < 3:
                first_visuals = visuals_by_slug.get(lesson_slugs[0], {})
                for card_slot in ("card-1", "card-2", "card-3"):
                    source = first_visuals.get(card_slot, "")
                    if source and source not in seen_urls:
                        sources.append(
                            {
                                "source_url": source,
                                "source_lesson_slug": lesson_slugs[0],
                                "source_slot": card_slot,
                            }
                        )
                        seen_urls.add(source)
                    if len(sources) == 3:
                        break
            if not unit_key or not sources:
                continue
            owner_key = f"{course_slug}:{unit_key}"
            for index, source in enumerate(sources[:3], start=1):
                placements.append(
                    {
                        "owner_type": "unit",
                        "owner_key": owner_key,
                        "slot": f"thumbnail-{index}",
                        **source,
                    }
                )
            if not course_visuals:
                course_visuals = sources[:3]

        if course_visuals:
            placements.append(
                {
                    "owner_type": "course",
                    "owner_key": course_slug,
                    "slot": "detail-hero",
                    **course_visuals[0],
                }
            )
            for index, source in enumerate(course_visuals[:3], start=1):
                placements.append(
                    {
                        "owner_type": "course",
                        "owner_key": course_slug,
                        "slot": f"cover-{index}",
                        **source,
                    }
                )
    return placements


def seed(*, execute: bool) -> dict:
    targets = seed_targets()
    placement_sources = course_placement_sources()
    unique_sources: dict[str, dict] = {}
    for target in targets:
        content_hash = hashlib.sha256(target["source_path"].read_bytes()).hexdigest()
        target["content_hash"] = content_hash
        target["referenced"] = True
        unique_sources.setdefault(content_hash, target)

    fallback_by_slot = {target["slot"]: target["slug"] for target in targets}
    for source_path in sorted(
        (PUBLIC_ROOT / "images" / "lesson-visual-library").glob("*/*.png")
    ):
        slot = source_path.stem
        if slot not in fallback_by_slot:
            continue
        content_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
        unique_sources.setdefault(
            content_hash,
            {
                "slug": fallback_by_slot[slot],
                "slot": slot,
                "source_url": f"/{source_path.relative_to(PUBLIC_ROOT).as_posix()}",
                "source_path": source_path,
                "content_hash": content_hash,
                "referenced": False,
            },
        )

    result = {
        "dry_run": not execute,
        "assignment_count": len(targets),
        "unique_asset_count": len(unique_sources),
        "placement_count": len(placement_sources),
        "uploaded_or_reused_count": 0,
        "activated_count": 0,
        "failed": [],
        "unique_sources": [
            {
                "content_hash": content_hash,
                "source_url": target["source_url"],
                "source_path": str(target["source_path"]),
                "first_lesson_slug": target["slug"],
                "slot": target["slot"],
            }
            for content_hash, target in unique_sources.items()
        ],
    }
    if not execute:
        return result

    ensure_visual_s3_configured()
    db = get_sessionmaker()()
    try:
        asset_ids: dict[str, str] = {}
        for content_hash, target in unique_sources.items():
            try:
                stored = store_uploaded_lesson_visual(
                    slug=target["slug"],
                    slot=target["slot"],
                    image_bytes=target["source_path"].read_bytes(),
                    model="builtin-static",
                    archive_reason="builtin_asset_seed",
                    db=db,
                    activate=False,
                )
                asset_ids[content_hash] = stored.library_asset_id
                if not target["referenced"]:
                    asset = get_visual_asset(db, asset_id=stored.library_asset_id)
                    if asset is not None:
                        scene = target["source_path"].parent.name.replace("-", " ")
                        asset.description_json = {
                            "subject": f"Reusable {scene} lesson visual",
                            "context": "Built-in visual library asset",
                            "setting": scene,
                            "people": [],
                        }
                result["uploaded_or_reused_count"] += 1
            except (OSError, LessonVisualRegenerationError) as exc:
                result["failed"].append(
                    {"source_path": str(target["source_path"]), "error": str(exc)}
                )

        asset_ids_by_url: dict[str, str] = {}
        for content_hash, target in unique_sources.items():
            asset_id = asset_ids.get(content_hash)
            if asset_id:
                asset_ids_by_url[target["source_url"]] = asset_id
        for target in targets:
            asset_id = asset_ids.get(target["content_hash"])
            if asset_id:
                asset_ids_by_url[target["source_url"]] = asset_id

        for target in targets:
            asset_id = asset_ids.get(target["content_hash"])
            if not asset_id:
                continue
            activate_visual_asset(
                db,
                lesson_slug=target["slug"],
                slot=target["slot"],
                asset_id=asset_id,
                only_if_missing=True,
            )
            result["activated_count"] += 1
        db.flush()
        for placement in placement_sources:
            active_asset = get_active_visual_asset(
                db,
                lesson_slug=placement["source_lesson_slug"],
                slot=placement["source_slot"],
            )
            asset_id = (
                active_asset.id
                if active_asset is not None
                else asset_ids_by_url.get(placement["source_url"])
            )
            if not asset_id:
                result["failed"].append(
                    {
                        "source_url": placement["source_url"],
                        "error": "placement_asset_not_found",
                    }
                )
                continue
            assign_visual_placement(
                db,
                owner_type=placement["owner_type"],
                owner_key=placement["owner_key"],
                slot=placement["slot"],
                asset_id=asset_id,
                mode="pinned",
                source_lesson_slug=placement["source_lesson_slug"],
                source_slot=placement["source_slot"],
                only_if_missing=True,
            )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Upload and seed the database.")
    args = parser.parse_args()
    result = seed(execute=args.execute)
    print(json.dumps(result, indent=2, default=str))
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
