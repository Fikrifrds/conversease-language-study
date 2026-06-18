from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import Any, Optional

import yaml

from app.data.curriculum import curriculum_root, production_tracker_path
from app.services.audio_generation import audio_playback_url


AUDIO_READY_STATUSES = {"done", "generated", "published"}
SUPPORTED_LEVEL_CODES = ("A1", "A2", "B1", "B2", "C1")

REQUIRED_CONTENT_ITEMS = (
    {
        "key": "lesson_yaml",
        "label": "Lesson metadata",
        "filename": "lesson.yaml",
        "tracker_column": None,
        "is_audio": False,
    },
    {
        "key": "lesson_md",
        "label": "Lesson body",
        "filename": "lesson.md",
        "tracker_column": "lesson_md",
        "is_audio": False,
    },
    {
        "key": "conversation_goal",
        "label": "Conversation goal",
        "filename": "conversation_goal.md",
        "tracker_column": None,
        "is_audio": False,
    },
    {
        "key": "listening_script",
        "label": "Listening script",
        "filename": "listening_script.md",
        "tracker_column": "listening_script",
        "is_audio": False,
    },
    {
        "key": "transcript_translation",
        "label": "Transcript translation",
        "filename": "transcript_translation.md",
        "tracker_column": None,
        "is_audio": False,
    },
    {
        "key": "useful_phrases",
        "label": "Useful phrases",
        "filename": "useful_phrases.yaml",
        "tracker_column": "phrases",
        "is_audio": False,
    },
    {
        "key": "vocabulary",
        "label": "Vocabulary",
        "filename": "vocabulary.yaml",
        "tracker_column": None,
        "is_audio": False,
    },
    {
        "key": "grammar",
        "label": "Grammar for conversation",
        "filename": "grammar_for_conversation.md",
        "tracker_column": "grammar",
        "is_audio": False,
    },
    {
        "key": "pronunciation",
        "label": "Pronunciation drill",
        "filename": "pronunciation_drill.md",
        "tracker_column": "pronunciation",
        "is_audio": False,
    },
    {
        "key": "response_prompts",
        "label": "Response prompts",
        "filename": "response_prompts.yaml",
        "tracker_column": "response_prompts",
        "is_audio": False,
    },
    {
        "key": "conversation_coach",
        "label": "Conversation Coach roleplay",
        "filename": "conversation_coach_roleplay.yaml",
        "tracker_column": "conversation_coach",
        "is_audio": False,
    },
    {
        "key": "quiz",
        "label": "Quiz",
        "filename": "quiz.yaml",
        "tracker_column": "quiz",
        "is_audio": False,
    },
    {
        "key": "reading",
        "label": "Reading support",
        "filename": "reading_support.md",
        "tracker_column": "reading",
        "is_audio": False,
    },
    {
        "key": "writing",
        "label": "Writing support",
        "filename": "writing_support.md",
        "tracker_column": "writing",
        "is_audio": False,
    },
    {
        "key": "audio_manifest",
        "label": "Audio manifest",
        "filename": "audio_manifest.yaml",
        "tracker_column": None,
        "is_audio": True,
    },
    {
        "key": "audio_generated",
        "label": "Listening audio generated",
        "filename": "audio_manifest.yaml",
        "tracker_column": "audio_generated",
        "is_audio": True,
    },
)


def required_content_items_for_language(language: str) -> list[dict[str, Any]]:
    return [
        item
        for item in REQUIRED_CONTENT_ITEMS
        if not item.get("languages") or language in item["languages"]
    ]


def content_plan_path(language: str = "english", level_code: str = "A1") -> Path:
    return curriculum_root() / language / level_code / "content_plan.yaml"


def discover_content_plan_paths(
    *,
    language: Optional[str] = None,
    level_code: Optional[str] = None,
) -> list[Path]:
    root = curriculum_root()
    if language and level_code:
        path = content_plan_path(language, level_code)
        return [path] if path.exists() else []

    if language:
        paths = sorted((root / language).glob("*/content_plan.yaml"))
    elif level_code:
        paths = sorted(root.glob(f"*/{level_code}/content_plan.yaml"))
    else:
        paths = sorted(root.glob("*/*/content_plan.yaml"))

    return [path for path in paths if path.is_file()]


def load_content_plan(language: str = "english", level_code: str = "A1") -> dict[str, Any]:
    path = content_plan_path(language, level_code)
    if not path.exists():
        return {
            "language": language,
            "language_code": "",
            "level_code": level_code,
            "course_slug": "",
            "course_title": "",
            "target_lesson_count": 0,
            "units": [],
        }

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Content plan must be a mapping: {path}")

    return data


def load_content_plan_from_path(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Content plan must be a mapping: {path}")

    language = path.parents[1].name
    level_code = path.parent.name
    return {
        "language": language,
        "level_code": level_code,
        **data,
    }


def content_readiness_summary(language: str = "english", level_code: str = "A1") -> dict[str, Any]:
    plan = load_content_plan(language, level_code)
    return content_readiness_from_plan(
        plan,
        language=language,
        level_code=level_code,
        plan_path=content_plan_path(language, level_code),
    )


def all_content_readiness_summary(
    *,
    language: Optional[str] = None,
    level_code: Optional[str] = None,
) -> dict[str, Any]:
    levels = [
        content_readiness_from_plan(
            load_content_plan_from_path(path),
            language=path.parents[1].name,
            level_code=path.parent.name,
            plan_path=path,
        )
        for path in discover_content_plan_paths(language=language, level_code=level_code)
    ]

    return {
        "summary": rollup_summary(levels),
        "level_count": len(levels),
        "levels": levels,
    }


def content_readiness_from_plan(
    plan: dict[str, Any],
    *,
    language: str,
    level_code: str,
    plan_path: Path,
) -> dict[str, Any]:
    tracker = load_tracker_rows()
    base_root = curriculum_root() / language / level_code
    units = []

    summary = {
        "planned_lesson_count": 0,
        "implemented_lesson_count": 0,
        "text_ready_count": 0,
        "audio_ready_count": 0,
        "beta_ready_count": 0,
        "production_ready_count": 0,
        "missing_content_count": 0,
        "missing_audio_count": 0,
    }

    for unit in plan.get("units", []):
        lesson_items = []
        for lesson in unit.get("lessons", []):
            summary["planned_lesson_count"] += 1
            lesson_report = lesson_readiness(
                base_root=base_root,
                language=language,
                level_code=level_code,
                unit=unit,
                lesson=lesson,
                tracker=tracker,
            )
            lesson_items.append(lesson_report)

            if lesson_report["implemented"]:
                summary["implemented_lesson_count"] += 1
            if lesson_report["text_ready"]:
                summary["text_ready_count"] += 1
            if lesson_report["audio_ready"]:
                summary["audio_ready_count"] += 1
            if lesson_report["beta_ready"]:
                summary["beta_ready_count"] += 1
            if lesson_report["production_ready"]:
                summary["production_ready_count"] += 1
            if not lesson_report["text_ready"]:
                summary["missing_content_count"] += 1
            if not lesson_report["audio_ready"]:
                summary["missing_audio_count"] += 1

        units.append(
            {
                "unit_key": unit.get("unit_key", ""),
                "title": unit.get("title", ""),
                "status": unit.get("status", ""),
                "main_conversation_outcome": unit.get("main_conversation_outcome", ""),
                "lesson_count": len(lesson_items),
                "text_ready_count": sum(1 for lesson in lesson_items if lesson["text_ready"]),
                "audio_ready_count": sum(1 for lesson in lesson_items if lesson["audio_ready"]),
                "production_ready_count": sum(1 for lesson in lesson_items if lesson["production_ready"]),
                "lessons": lesson_items,
            }
        )

    return {
        "course": {
            "language": plan.get("language", language),
            "language_code": plan.get("language_code", ""),
            "level_code": plan.get("level_code", level_code),
            "course_slug": plan.get("course_slug", ""),
            "course_title": plan.get("course_title", ""),
            "target_lesson_count": int(plan.get("target_lesson_count") or 0),
            "plan_path": str(plan_path),
        },
        "summary": summary,
        "required_items": required_content_items_for_language(language),
        "units": units,
    }


def rollup_summary(levels: list[dict[str, Any]]) -> dict[str, int]:
    summary = {
        "planned_lesson_count": 0,
        "implemented_lesson_count": 0,
        "text_ready_count": 0,
        "audio_ready_count": 0,
        "beta_ready_count": 0,
        "production_ready_count": 0,
        "missing_content_count": 0,
        "missing_audio_count": 0,
    }

    for level in levels:
        for key in summary:
            summary[key] += int(level.get("summary", {}).get(key, 0))

    return summary


def lesson_readiness(
    *,
    base_root: Path,
    language: str,
    level_code: str,
    unit: dict[str, Any],
    lesson: dict[str, Any],
    tracker: dict[tuple[str, str, str], dict[str, str]],
) -> dict[str, Any]:
    unit_key = unit.get("unit_key", "")
    lesson_key = lesson.get("lesson_key", "")
    lesson_dir = base_root / "units" / unit_key / lesson_key
    tracker_row = tracker.get((f"{language}/{level_code}", unit_key, lesson_key), {})
    if not tracker_row:
        tracker_row = tracker.get((level_code, unit_key, lesson_key), {})
    checks = []

    for item in required_content_items_for_language(language):
        checks.append(
            item_readiness(
                item=item,
                lesson_dir=lesson_dir,
                tracker_row=tracker_row,
            )
        )

    text_checks = [check for check in checks if not check["is_audio"]]
    audio_checks = [check for check in checks if check["is_audio"]]
    text_ready = all(check["ready"] for check in text_checks)
    audio_ready = all(check["ready"] for check in audio_checks)
    publish_status = tracker_row.get("publish_status", "")
    review_status = tracker_row.get("review_status", "")
    implemented = lesson_dir.exists()
    beta_ready = implemented and text_ready and publish_status in {"published", "beta", ""}
    production_ready = beta_ready and audio_ready and review_status in {"ready", ""}
    missing_items = [check["label"] for check in checks if not check["ready"]]

    if production_ready:
        status = "production_ready"
    elif beta_ready:
        status = "beta_ready_needs_audio"
    elif implemented:
        status = "implemented_needs_content"
    else:
        status = "planned_missing_content"

    return {
        "lesson_key": lesson_key,
        "slug": lesson.get("slug", ""),
        "title": lesson.get("title", ""),
        "plan_status": lesson.get("status", ""),
        "lesson_dir": str(lesson_dir),
        "implemented": implemented,
        "text_ready": text_ready,
        "audio_ready": audio_ready,
        "beta_ready": beta_ready,
        "production_ready": production_ready,
        "review_status": review_status,
        "publish_status": publish_status,
        "status": status,
        "missing_items": missing_items,
        "audio_asset": lesson_audio_asset(lesson_dir),
        "checks": checks,
    }


def item_readiness(
    *,
    item: dict[str, Any],
    lesson_dir: Path,
    tracker_row: dict[str, str],
) -> dict[str, Any]:
    path = lesson_dir / item["filename"]
    file_exists = path.exists() and path.is_file()
    non_empty = file_exists and path.read_text(encoding="utf-8").strip() != ""
    tracker_column = item.get("tracker_column")
    tracker_value = tracker_row.get(str(tracker_column), "") if tracker_column else ""

    if item["key"] == "audio_generated":
        manifest_ready = audio_manifest_ready(path)
        ready = manifest_ready
    else:
        ready = bool(non_empty)
        if tracker_column:
            ready = ready and tracker_value == "done"

    return {
        "key": item["key"],
        "label": item["label"],
        "filename": item["filename"],
        "is_audio": item["is_audio"],
        "ready": ready,
        "file_exists": file_exists,
        "non_empty": non_empty,
        "tracker_column": tracker_column or "",
        "tracker_value": tracker_value,
    }


def audio_manifest_ready(path: Path) -> bool:
    if not path.exists():
        return False

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return False

    if not isinstance(data, dict):
        return False

    if str(data.get("status", "")).strip() not in AUDIO_READY_STATUSES:
        return False

    dialogue_asset = dialogue_audio_manifest_asset(data)
    if not dialogue_asset:
        return False

    if not dialogue_asset.get("audio_url"):
        return False
    if not dialogue_asset.get("duration_seconds"):
        return False
    if not audio_manifest_script_matches(path, dialogue_asset):
        return False

    return True


def dialogue_audio_manifest_asset(data: dict[str, Any]) -> Optional[dict[str, Any]]:
    assets = data.get("assets", [])
    if not isinstance(assets, list) or not assets:
        return None

    dialogue_asset = next(
        (
            asset
            for asset in assets
            if isinstance(asset, dict) and asset.get("key") == "dialogue_main"
        ),
        None,
    )
    if dialogue_asset:
        return dialogue_asset

    return next((asset for asset in assets if isinstance(asset, dict) and asset.get("audio_url")), None)


def lesson_audio_asset(lesson_dir: Path) -> Optional[dict[str, Any]]:
    path = lesson_dir / "audio_manifest.yaml"
    if not path.exists():
        return None

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return None

    if not isinstance(data, dict):
        return None
    if str(data.get("status", "")).strip() not in AUDIO_READY_STATUSES:
        return None

    dialogue_asset = dialogue_audio_manifest_asset(data)
    if not dialogue_asset:
        return None
    if not audio_manifest_script_matches(path, dialogue_asset):
        return None

    audio_url = str(dialogue_asset.get("audio_url") or "")
    if not audio_url:
        return None
    storage_key = str(dialogue_asset.get("storage_key") or "")
    playback_url = audio_playback_url(audio_url=audio_url, storage_key=storage_key)

    return {
        "key": str(dialogue_asset.get("key") or ""),
        "type": str(dialogue_asset.get("type") or ""),
        "audio_url": audio_url,
        "playback_url": playback_url,
        "duration_seconds": float(dialogue_asset.get("duration_seconds") or 0),
        "provider": str(dialogue_asset.get("provider") or data.get("provider") or ""),
        "model": str(dialogue_asset.get("model") or ""),
        "voice_id": str(dialogue_asset.get("voice_id") or ""),
        "speaker_voices": dialogue_asset.get("speaker_voices") or {},
        "line_count": int(dialogue_asset.get("line_count") or 0),
        "audio_format": str(dialogue_asset.get("audio_format") or ""),
        "storage_key": storage_key,
        "generated_at": str(dialogue_asset.get("generated_at") or ""),
        "generated_by": str(dialogue_asset.get("generated_by") or ""),
    }


def audio_manifest_script_matches(path: Path, dialogue_asset: dict[str, Any]) -> bool:
    expected_hash = str(dialogue_asset.get("script_content_hash") or "").strip()
    if not expected_hash:
        return True

    script_file = str(dialogue_asset.get("script_file") or "listening_script.md").strip()
    if not script_file:
        return False
    script_path = path.parent / script_file
    if not script_path.exists():
        return False
    actual_hash = hashlib.sha256(script_path.read_bytes()).hexdigest()
    return actual_hash == expected_hash


def load_tracker_rows() -> dict[tuple[str, str, str], dict[str, str]]:
    path = production_tracker_path()
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    return {
        (row.get("level", ""), row.get("unit", ""), row.get("lesson", "")): row
        for row in rows
        if row.get("level") and row.get("unit") and row.get("lesson")
    }


def render_markdown_report(readiness: Optional[dict[str, Any]] = None) -> str:
    source = readiness or all_content_readiness_summary()
    if "levels" in source:
        return render_markdown_collection(source)

    return render_markdown_level(source)


def render_markdown_collection(source: dict[str, Any]) -> str:
    summary = source["summary"]
    lines = [
        "# Content Readiness Report",
        "",
        f"- Levels tracked: {source['level_count']}",
        f"- Planned lessons: {summary['planned_lesson_count']}",
        f"- Implemented lessons: {summary['implemented_lesson_count']}",
        f"- Text-ready lessons: {summary['text_ready_count']}",
        f"- Audio-ready lessons: {summary['audio_ready_count']}",
        f"- Beta-ready lessons: {summary['beta_ready_count']}",
        f"- Production-ready lessons: {summary['production_ready_count']}",
        f"- Lessons missing content: {summary['missing_content_count']}",
        f"- Lessons missing audio: {summary['missing_audio_count']}",
        "",
    ]

    for level in source["levels"]:
        lines.append(render_markdown_level(level, heading_level=2).strip())
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def render_markdown_level(source: dict[str, Any], *, heading_level: int = 1) -> str:
    summary = source["summary"]
    heading = "#" * heading_level
    subheading = "#" * (heading_level + 1)
    lines = [
        f"{heading} {source['course']['course_title']} ({source['course']['level_code']})",
        "",
        f"{subheading} Summary",
        "",
        f"- Planned lessons: {summary['planned_lesson_count']}",
        f"- Implemented lessons: {summary['implemented_lesson_count']}",
        f"- Text-ready lessons: {summary['text_ready_count']}",
        f"- Audio-ready lessons: {summary['audio_ready_count']}",
        f"- Beta-ready lessons: {summary['beta_ready_count']}",
        f"- Production-ready lessons: {summary['production_ready_count']}",
        f"- Lessons missing content: {summary['missing_content_count']}",
        f"- Lessons missing audio: {summary['missing_audio_count']}",
        "",
    ]

    for unit in source["units"]:
        lines.extend(
            [
                f"{subheading} {unit['unit_key']} - {unit['title']}",
                "",
                "| Lesson | Status | Missing |",
                "|---|---|---|",
            ]
        )
        for lesson in unit["lessons"]:
            missing = ", ".join(lesson["missing_items"]) if lesson["missing_items"] else "-"
            lines.append(f"| {lesson['lesson_key']} - {lesson['title']} | {lesson['status']} | {missing} |")
        lines.append("")

    return "\n".join(lines).strip() + "\n"
