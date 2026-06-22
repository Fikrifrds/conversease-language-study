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
FALLBACK_SCENE_ROTATION = ("classroom", "service", "travel", "workplace", "health")

SCENE_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "health",
        (
            r"\bhealth\b",
            r"\bsymptoms?\b",
            r"\bappointment\b",
            r"\bclinic\b",
            r"\bdoctor\b",
            r"\bnurse\b",
            r"\bmedicine\b",
            r"\bsick\b",
            r"\bpain\b",
        ),
    ),
    (
        "service",
        (
            r"\bphone\b",
            r"\bemail\b",
            r"\bcontact\b",
            r"\bnumbers?\b",
            r"\bclarif(?:y|ication)\b",
            r"\brequests?\b",
            r"\bhelp\b",
            r"\bproblem\b",
            r"\bfood\b",
            r"\bdrinks?\b",
            r"\bshopping\b",
            r"\bshops?\b",
            r"\bprices?\b",
            r"\bitems?\b",
            r"\bservice\b",
            r"\bcustomer\b",
            r"\bclient\b",
            r"\bbuying\b",
            r"\bcaf[ée]?\b",
        ),
    ),
    (
        "travel",
        (
            r"\borigin\b",
            r"\bfrom\b",
            r"\bplaces?\b",
            r"\bwhere\b",
            r"\bdirections?\b",
            r"\broute\b",
            r"\btravel\b",
            r"\btransport\b",
            r"\btickets?\b",
            r"\bdeparture\b",
            r"\bdriver\b",
            r"\bweekend\b",
            r"\byesterday\b",
            r"\bpast\b",
            r"\bexperience\b",
            r"\bstor(?:y|ies)\b",
            r"\bcommunity\b",
            r"\bculture\b",
            r"\blocal\b",
        ),
    ),
    (
        "workplace",
        (
            r"\bwork(?:ing)?\b",
            r"\bworkplace\b",
            r"\bmeeting\b",
            r"\bpresentation\b",
            r"\bargument\b",
            r"\bnegotiation\b",
            r"\bproposal\b",
            r"\bfeedback\b",
            r"\bdecision\b",
            r"\bsolution\b",
            r"\bgoals?\b",
            r"\bprogress\b",
            r"\barticle\b",
            r"\bsources?\b",
            r"\bviewpoint\b",
            r"\bleadership\b",
            r"\bcoaching\b",
            r"\bstakeholder\b",
            r"\brisk\b",
            r"\bdebate\b",
            r"\bdiscussion\b",
            r"\bprofessional\b",
            r"\btasks?\b",
            r"\bupdates?\b",
            r"\bpriorit(?:y|ies)\b",
        ),
    ),
    (
        "classroom",
        (
            r"\bclass\b",
            r"\bstudy\b",
            r"\binstructions?\b",
            r"\bgreetings?\b",
            r"\bsal[au]m\b",
            r"\bhello\b",
            r"\bname\b",
            r"\bspell(?:ing)?\b",
            r"\bletters?\b",
            r"\brepeat(?:ing)?\b",
            r"\bunderstand\b",
            r"\bintroduc(?:e|ing|tion)\b",
            r"\btime\b",
            r"\bdays?\b",
            r"\broutine\b",
            r"\bschedules?\b",
            r"\breview\b",
            r"\btest\b",
            r"\bfinal\b",
            r"\bgrammar\b",
        ),
    ),
)


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
    category = scene_category(text, lesson_dir)
    return f"{category}-{gender}"


def scene_category(text: str, lesson_dir: Path) -> str:
    lesson_number = numeric_part(lesson_dir.name)
    for category, patterns in SCENE_RULES:
        if has_any_pattern(text, patterns):
            if "mission" in text:
                return mission_scene_category(text, category, lesson_number)
            return category

    return FALLBACK_SCENE_ROTATION[(lesson_number - 1) % len(FALLBACK_SCENE_ROTATION)]


def mission_scene_category(text: str, category: str, lesson_number: int) -> str:
    if category == "classroom" and has_any_pattern(text, (r"\bcontact\b", r"\bphone\b", r"\bemail\b")):
        return "service"
    if category == "classroom" and has_any_pattern(text, (r"\bplaces?\b", r"\bdirections?\b", r"\btravel\b")):
        return "travel"
    if category == "classroom" and has_any_pattern(text, (r"\bwork\b", r"\bstudy\b", r"\bprofessional\b")):
        return "workplace"

    rotation = mission_rotation_for_category(category)
    return rotation[(lesson_number - 1) % len(rotation)]


def mission_rotation_for_category(category: str) -> tuple[str, ...]:
    if category == "service":
        return ("service", "workplace", "travel")
    if category == "travel":
        return ("travel", "service", "classroom")
    if category == "workplace":
        return ("workplace", "classroom", "service")
    if category == "health":
        return ("health", "service", "classroom")
    return ("classroom", "service", "travel")


def has_any_pattern(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def numeric_part(value: str) -> int:
    match = re.search(r"(\d+)", value)
    if not match:
        return 1
    return int(match.group(1))


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
