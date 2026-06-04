from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = REPO_ROOT / "apps" / "api"


def ensure_api_import_path() -> None:
    api_path = str(API_ROOT)
    if api_path not in sys.path:
        sys.path.insert(0, api_path)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Audit Conversease generated lesson audio.")
    parser.add_argument("--language", default="english", help="Curriculum language folder.")
    parser.add_argument("--level", default=None, help="Optional level code filter, for example A1.")
    parser.add_argument(
        "--lesson",
        default=None,
        help="Optional lesson slug or lesson key, for example spelling-your-name.",
    )
    parser.add_argument("--missing-only", action="store_true", help="Show only lessons without generated audio.")
    parser.add_argument("--text-ready-only", action="store_true", help="Show only lessons with complete reviewed text.")
    parser.add_argument("--format", choices=("table", "json"), default="table")
    args = parser.parse_args(argv)

    ensure_api_import_path()
    from app.data.content_readiness import all_content_readiness_summary

    readiness = all_content_readiness_summary(language=args.language, level_code=args.level)
    rows = audio_rows(
        readiness,
        lesson_filter=args.lesson,
        missing_only=args.missing_only,
        text_ready_only=args.text_ready_only,
    )

    if args.format == "json":
        print(json.dumps(rows, indent=2, sort_keys=True))
        return 0

    print(render_table(rows))
    return 0


def audio_rows(
    readiness: dict[str, Any],
    *,
    lesson_filter: Optional[str],
    missing_only: bool,
    text_ready_only: bool,
) -> list[dict[str, Any]]:
    normalized_filter = (lesson_filter or "").strip().lower()
    rows: list[dict[str, Any]] = []

    for level in readiness.get("levels", []):
        course = level.get("course", {})
        for unit in level.get("units", []):
            for lesson in unit.get("lessons", []):
                if normalized_filter and normalized_filter not in {
                    str(lesson.get("slug", "")).lower(),
                    str(lesson.get("lesson_key", "")).lower(),
                }:
                    continue
                if missing_only and lesson.get("audio_ready"):
                    continue
                if text_ready_only and not lesson.get("text_ready"):
                    continue

                audio_asset = lesson.get("audio_asset") or {}
                checks = {
                    str(check.get("key", "")): check
                    for check in lesson.get("checks", [])
                    if isinstance(check, dict)
                }
                audio_check = checks.get("audio_generated", {})
                rows.append(
                    {
                        "language": course.get("language", ""),
                        "level": course.get("level_code", ""),
                        "unit": unit.get("unit_key", ""),
                        "lesson_key": lesson.get("lesson_key", ""),
                        "slug": lesson.get("slug", ""),
                        "title": lesson.get("title", ""),
                        "text_ready": bool(lesson.get("text_ready")),
                        "audio_ready": bool(lesson.get("audio_ready")),
                        "production_ready": bool(lesson.get("production_ready")),
                        "status": lesson.get("status", ""),
                        "tracker_audio": audio_check.get("tracker_value", ""),
                        "audio_url": audio_asset.get("audio_url", ""),
                        "playback_url": audio_asset.get("playback_url", ""),
                        "storage_key": audio_asset.get("storage_key", ""),
                        "duration_seconds": audio_asset.get("duration_seconds", 0),
                        "model": audio_asset.get("model", ""),
                        "voice_id": audio_asset.get("voice_id", ""),
                        "speaker_voices": audio_asset.get("speaker_voices", {}),
                        "generated_at": audio_asset.get("generated_at", ""),
                        "generated_by": audio_asset.get("generated_by", ""),
                    }
                )

    return rows


def render_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "No matching lessons."

    headers = ["Level", "Lesson", "Text", "Audio", "Tracker", "Duration", "Storage key"]
    table_rows = [
        [
            str(row["level"]),
            str(row["slug"] or row["lesson_key"]),
            "yes" if row["text_ready"] else "no",
            "yes" if row["audio_ready"] else "no",
            str(row["tracker_audio"] or "-"),
            format_duration(float(row["duration_seconds"] or 0)),
            str(row["storage_key"] or "-"),
        ]
        for row in rows
    ]

    widths = [
        max(len(headers[index]), *(len(row[index]) for row in table_rows))
        for index in range(len(headers))
    ]
    lines = [
        "  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)),
        "  ".join("-" * width for width in widths),
    ]
    lines.extend(
        "  ".join(value.ljust(widths[index]) for index, value in enumerate(row))
        for row in table_rows
    )
    return "\n".join(lines)


def format_duration(value: float) -> str:
    if value <= 0:
        return "-"
    minutes = int(value // 60)
    seconds = int(round(value % 60))
    if minutes:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"


if __name__ == "__main__":
    raise SystemExit(main())
