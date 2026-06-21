from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Optional, Sequence

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = REPO_ROOT / "apps" / "api"
CURRICULUM_ROOT = REPO_ROOT / "content" / "curriculum"
VISUAL_LIBRARY_ROOT = REPO_ROOT / "apps" / "web" / "public" / "images" / "lesson-visual-library"

HERO_WIDTH = 1672
HERO_HEIGHT = 941
CARD_WIDTH = 1254
CARD_HEIGHT = 1254


def ensure_api_import_path() -> None:
    api_path = str(API_ROOT)
    if api_path not in sys.path:
        sys.path.insert(0, api_path)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate lesson visual metadata for all curriculum lessons.")
    parser.add_argument("--language", choices=("english", "arabic"), help="Optional language filter.")
    parser.add_argument("--level", help="Optional level filter, for example A1.")
    parser.add_argument("--check", action="store_true", help="Report files that would change without writing.")
    args = parser.parse_args(argv)

    ensure_api_import_path()
    changed: list[Path] = []
    lessons = lesson_dirs(language=args.language, level=args.level)

    for lesson_dir in lessons:
        next_yaml = build_visuals_yaml(lesson_dir)
        visuals_path = lesson_dir / "visuals.yaml"
        current = visuals_path.read_text(encoding="utf-8") if visuals_path.exists() else ""
        if current != next_yaml:
            changed.append(visuals_path)
            if not args.check:
                visuals_path.write_text(next_yaml, encoding="utf-8")

    if args.check:
        if changed:
            print(f"{len(changed)} visuals.yaml files need regeneration:")
            for path in changed[:40]:
                print(path.relative_to(REPO_ROOT))
            if len(changed) > 40:
                print(f"... and {len(changed) - 40} more")
            return 1
        print(f"All {len(lessons)} lesson visual files are current.")
        return 0

    print(f"Generated visuals.yaml for {len(lessons)} lessons ({len(changed)} changed).")
    return 0


def lesson_dirs(*, language: Optional[str], level: Optional[str]) -> list[Path]:
    pattern = "*/*/units/*/*/lesson.yaml"
    dirs: list[Path] = []
    normalized_level = (level or "").upper()
    for lesson_yaml in sorted(CURRICULUM_ROOT.glob(pattern)):
        parts = lesson_yaml.relative_to(CURRICULUM_ROOT).parts
        lesson_language, lesson_level = parts[0], parts[1]
        if language and lesson_language != language:
            continue
        if normalized_level and lesson_level.upper() != normalized_level:
            continue
        dirs.append(lesson_yaml.parent)
    return dirs


def build_visuals_yaml(lesson_dir: Path) -> str:
    lesson = read_yaml(lesson_dir / "lesson.yaml")
    useful_phrases = read_yaml(lesson_dir / "useful_phrases.yaml")
    language, level, unit_key, lesson_key = lesson_identity(lesson_dir)
    slug = str(lesson.get("slug") or lesson_key)
    title = str(lesson.get("title") or slug.replace("-", " ").title())
    gender = lesson_visual_gender(lesson_dir)
    scene = classify_scene(lesson_dir, lesson, language=language, gender=gender)
    labels = phrase_labels(useful_phrases, fallback=title)
    scene_label = scene.replace("-", " ")
    group_label = "perempuan" if gender == "female" else "laki-laki"

    data = {
        "hero": {
            "src": f"/images/lesson-visual-library/{scene}/hero.png",
            "width": HERO_WIDTH,
            "height": HERO_HEIGHT,
            "alt": f"Ilustrasi cartoon faceless {group_label} untuk konteks {title} di Indonesia.",
            "caption": f"Konteks percakapan nyata: {title}.",
        },
        "cards": [
            {
                "src": f"/images/lesson-visual-library/{scene}/card-{index}.png",
                "width": CARD_WIDTH,
                "height": CARD_HEIGHT,
                "label": label,
                "alt": f"Cuplikan visual {scene_label} untuk frasa {plain_label(label)}.",
            }
            for index, label in enumerate(labels, start=1)
        ],
    }
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100)


def lesson_identity(lesson_dir: Path) -> tuple[str, str, str, str]:
    parts = lesson_dir.relative_to(CURRICULUM_ROOT).parts
    return parts[0], parts[1], parts[3], parts[4]


def read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return {}
    return data


def lesson_visual_gender(lesson_dir: Path) -> str:
    from app.services.audio_generation import infer_speaker_gender

    genders: set[str] = set()
    for speaker in dialogue_speakers(lesson_dir / "listening_script.md"):
        gender = infer_speaker_gender(speaker)
        if gender in {"male", "female"}:
            genders.add(gender)

    if genders == {"female"}:
        return "female"
    return "male"


def dialogue_speakers(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    text = text.split("## Audio Direction", 1)[0]
    speakers: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^\s*(?:[-*]\s*)?\*{0,2}([^:*#][^:*]{1,40}):\*{0,2}\s+", line)
        if match:
            speaker = re.sub(r"[^A-Za-z ]", "", match.group(1)).strip()
            if speaker:
                speakers.append(speaker)
    return speakers


def classify_scene(lesson_dir: Path, lesson: dict[str, Any], *, language: str, gender: str) -> str:
    title = str(lesson.get("title") or "")
    slug = str(lesson.get("slug") or "")
    unit = lesson_dir.parent.name
    text = f"{language} {unit} {lesson_dir.name} {slug} {title}".lower()

    if has_any(text, ("health", "symptom", "appointment", "clinic", "doctor", "nurse")):
        category = "health"
    elif has_any(text, ("travel", "transport", "ticket", "departure", "driver", "direction", "place", "where", "route")):
        category = "travel"
    elif has_any(text, ("food", "shopping", "shop", "price", "drink", "item", "service", "customer", "client", "buying", "cafe")):
        category = "service"
    elif has_any(
        text,
        (
            "workplace",
            "meeting",
            "presentation",
            "argument",
            "negotiation",
            "proposal",
            "feedback",
            "decision",
            "problem",
            "solution",
            "goals",
            "progress",
            "article",
            "source",
            "viewpoint",
            "leadership",
            "coaching",
            "stakeholder",
            "risk",
            "debate",
            "discussion",
            "professional",
            "task",
            "update",
            "priorities",
            "options",
        ),
    ):
        category = "workplace"
    else:
        category = "classroom"

    return f"{category}-{gender}"


def has_any(text: str, needles: tuple[str, ...]) -> bool:
    return any(needle in text for needle in needles)


def phrase_labels(useful_phrases: dict[str, Any], *, fallback: str) -> list[str]:
    raw_phrases = useful_phrases.get("phrases") or []
    labels = [
        str(item.get("phrase") or "").strip()
        for item in raw_phrases
        if isinstance(item, dict) and str(item.get("phrase") or "").strip()
    ]
    while len(labels) < 3:
        labels.append(fallback)
    return labels[:3]


def plain_label(label: str) -> str:
    return re.sub(r"\s+", " ", label).strip()


if __name__ == "__main__":
    raise SystemExit(main())
