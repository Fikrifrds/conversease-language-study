from __future__ import annotations

import argparse
import asyncio
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = REPO_ROOT / "apps" / "api"
CURRICULUM_ROOT = REPO_ROOT / "content" / "curriculum"


def ensure_api_import_path() -> None:
    api_path = str(API_ROOT)
    if api_path not in sys.path:
        sys.path.insert(0, api_path)


@dataclass(frozen=True)
class AudioTarget:
    language: str
    level: str
    unit_key: str
    lesson_key: str
    slug: str
    title: str
    status: str
    manifest_path: Path


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Regenerate listening audio for lesson manifests marked needs_regeneration."
    )
    parser.add_argument("--language", choices=("english", "arabic"), help="Optional language filter.")
    parser.add_argument("--level", help="Optional level filter, for example A1.")
    parser.add_argument("--lesson", help="Optional lesson slug or lesson key filter.")
    parser.add_argument("--limit", type=int, help="Maximum number of lessons to process.")
    parser.add_argument("--provider", help="Optional TTS provider override.")
    parser.add_argument("--model", help="Optional TTS model override.")
    parser.add_argument("--speed", type=float, default=1.0, help="TTS speed passed to the audio service.")
    parser.add_argument(
        "--generated-by",
        default="script:regenerate_lesson_audio",
        help="Value written to the generated_by manifest field.",
    )
    parser.add_argument("--format", choices=("table", "json"), default="table")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually call the TTS provider and upload audio. Without this flag, the script is dry-run only.",
    )
    args = parser.parse_args(argv)

    ensure_api_import_path()
    from app.services.audio_generation import read_yaml_mapping

    targets = discover_targets(
        read_yaml_mapping=read_yaml_mapping,
        language=args.language,
        level=args.level,
        lesson=args.lesson,
    )
    if args.limit is not None:
        targets = targets[: max(args.limit, 0)]

    if not args.execute:
        print(render_targets(targets, output_format=args.format, dry_run=True))
        return 0

    return asyncio.run(execute_targets(targets, args=args))


def discover_targets(
    *,
    read_yaml_mapping,
    language: Optional[str],
    level: Optional[str],
    lesson: Optional[str],
) -> list[AudioTarget]:
    normalized_lesson = (lesson or "").strip().lower()
    normalized_level = (level or "").strip().upper()
    targets: list[AudioTarget] = []

    for manifest_path in sorted(CURRICULUM_ROOT.glob("*/*/units/*/*/audio_manifest.yaml")):
        parts = manifest_path.relative_to(CURRICULUM_ROOT).parts
        target_language, target_level, _, unit_key, lesson_key, _ = parts
        if language and target_language != language:
            continue
        if normalized_level and target_level.upper() != normalized_level:
            continue

        manifest = read_yaml_mapping(manifest_path)
        status = str(manifest.get("status") or "").strip()
        if status != "needs_regeneration":
            continue

        lesson_yaml_path = manifest_path.parent / "lesson.yaml"
        lesson_yaml = read_yaml_mapping(lesson_yaml_path)
        slug = str(lesson_yaml.get("slug") or "")
        title = str(lesson_yaml.get("title") or "")
        if normalized_lesson and normalized_lesson not in {slug.lower(), lesson_key.lower()}:
            continue

        targets.append(
            AudioTarget(
                language=target_language,
                level=target_level,
                unit_key=unit_key,
                lesson_key=lesson_key,
                slug=slug,
                title=title,
                status=status,
                manifest_path=manifest_path,
            )
        )

    return targets


async def execute_targets(targets: list[AudioTarget], *, args: argparse.Namespace) -> int:
    from app.services.audio_generation import AudioGenerationError, generate_lesson_listening_audio

    failures: list[dict[str, str]] = []
    for index, target in enumerate(targets, start=1):
        print(f"[{index}/{len(targets)}] generating {target.language} {target.level} {target.slug}")
        try:
            result = await generate_lesson_listening_audio(
                lesson_slug=target.slug,
                provider=args.provider,
                model=args.model,
                speed=args.speed,
                generated_by=args.generated_by,
            )
        except AudioGenerationError as exc:
            failures.append({"slug": target.slug, "error": str(exc)})
            print(f"  failed: {exc}")
            continue
        except Exception as exc:  # pragma: no cover - production safety surface
            failures.append({"slug": target.slug, "error": repr(exc)})
            print(f"  failed: {exc!r}")
            continue

        print(
            "  ok: "
            f"{result.get('duration_seconds', 0)}s "
            f"{result.get('provider', '')}/{result.get('model', '')}"
        )

    if failures:
        print(json.dumps({"failed": failures}, indent=2, sort_keys=True))
        return 1
    return 0


def render_targets(targets: list[AudioTarget], *, output_format: str, dry_run: bool) -> str:
    rows = [
        {
            "language": target.language,
            "level": target.level,
            "unit": target.unit_key,
            "lesson_key": target.lesson_key,
            "slug": target.slug,
            "title": target.title,
            "status": target.status,
        }
        for target in targets
    ]
    if output_format == "json":
        return json.dumps({"dry_run": dry_run, "count": len(rows), "targets": rows}, indent=2)

    if not rows:
        return "No matching stale audio manifests."

    summary: dict[str, int] = {}
    for row in rows:
        key = f"{row['language']} {row['level']}"
        summary[key] = summary.get(key, 0) + 1

    lines = ["DRY RUN: no audio generated.", f"Targets: {len(rows)}"]
    lines.extend(f"- {key}: {count}" for key, count in sorted(summary.items()))
    lines.append("")
    lines.append("Language  Level  Lesson")
    lines.append("--------  -----  ------")
    lines.extend(f"{row['language']:<8}  {row['level']:<5}  {row['slug']}" for row in rows)
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
