#!/usr/bin/env python3
"""Generate the lesson array in apps/web/lib/data.ts from the curriculum files.

The curriculum under content/curriculum/<LANGUAGE>/<LEVEL> is the SINGLE SOURCE
OF TRUTH for lesson content. The web app renders static lessons/courses from
apps/web/lib/data.ts; this script regenerates generated blocks so the two never
drift.

Run after editing any lesson content:

    PYTHONPATH=apps/api apps/api/.venv/bin/python scripts/generate_web_lesson_data.py

A pytest (tests/test_web_lesson_data_in_sync.py) fails if data.ts is out of sync.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = REPO_ROOT / "apps" / "api"
DATA_TS = REPO_ROOT / "apps" / "web" / "lib" / "data.ts"

# Reuse the curriculum loader from the API package, plus the shared lesson
# content builder so data.ts and the runtime Pro-gated endpoint never drift.
sys.path.insert(0, str(API_ROOT))
from app.data.curriculum import all_authored_courses  # noqa: E402
from app.services.lesson_content import (  # noqa: E402
    LessonContentError as GeneratorError,
    build_lesson,
    language_label,
)

BEGIN_MARKER = "  // <generated:lessons>"
END_MARKER = "  // </generated:lessons>"

COURSES_BEGIN_MARKER = "  // <generated:courses>"
COURSES_END_MARKER = "  // </generated:courses>"

COACH_TURNS_BEGIN_MARKER = "  // <generated:coach_turns>"
COACH_TURNS_END_MARKER = "  // </generated:coach_turns>"

COACH_SCENARIOS_BEGIN_MARKER = "  // <generated:coach_scenarios>"
COACH_SCENARIOS_END_MARKER = "  // </generated:coach_scenarios>"


def extract_level_outcome(level_spec: Path) -> str:
    if not level_spec.exists():
        return ""
    text = level_spec.read_text(encoding="utf-8")
    match = re.search(r"^##\s+Level Outcome\s*$", text, re.MULTILINE)
    if not match:
        return ""
    rest = text[match.end() :]
    body = rest.split("\n##", 1)[0]
    paragraph = next((p.strip() for p in body.split("\n\n") if p.strip()), "")
    return paragraph.replace("\n", " ").strip()


def collect_lessons() -> list[dict[str, Any]]:
    lessons: list[dict[str, Any]] = []
    for course in all_authored_courses():
        for unit in course["units"]:
            for lesson in unit["lessons"]:
                lessons.append(build_lesson(course, unit["title"], lesson))
    return lessons


def collect_courses() -> list[dict[str, Any]]:
    courses: list[dict[str, Any]] = []
    for course in all_authored_courses():
        if not course.get("units"):
            continue
        language = str(course.get("language") or "english")
        level_code = str(course.get("level_code") or "")
        outcome = extract_level_outcome(
            REPO_ROOT / "content" / "curriculum" / language / level_code / "LEVEL_SPEC.md"
        )
        courses.append(
            {
                "slug": course.get("course_slug") or "",
                "language": language,
                "languageCode": course.get("language_code") or "",
                "languageLabel": language_label(language),
                "level": level_code,
                "title": course.get("course_title") or "",
                "outcome": outcome,
                "accessTier": course.get("access_tier") or "",
                "units": [
                    {
                        "slug": unit["slug"],
                        "title": unit["title"],
                        "outcome": unit.get("outcome") or "",
                        "progress": 0,
                        "lessons": [
                            {
                                "slug": lesson["slug"],
                                "title": lesson["title"],
                                "status": lesson.get("status") or "",
                                "minutes": int(lesson.get("estimated_minutes") or 0),
                            }
                            for lesson in unit.get("lessons", [])
                        ],
                    }
                    for unit in course.get("units", [])
                ],
            }
        )
    return courses


def collect_coach_turns() -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    turns_by_slug: dict[str, list[dict[str, Any]]] = {}
    scenario_by_slug: dict[str, dict[str, Any]] = {}
    for course in all_authored_courses():
        level_code = str(course.get("level_code") or "")
        for unit in course.get("units", []):
            for lesson in unit.get("lessons", []):
                roleplay = lesson.get("roleplay") or {}
                turns = roleplay.get("turns")
                if not isinstance(turns, list) or not turns:
                    continue
                scenario_by_slug[str(lesson["slug"])] = {
                    "slug": str(lesson["slug"]),
                    "label": str(lesson["title"]),
                    "description": str(unit["title"]),
                    "language": str(course.get("language") or "english"),
                    "languageLabel": language_label(str(course.get("language") or "english")),
                    "levelCode": str(roleplay.get("level_code") or level_code),
                    "scenarioKey": str(roleplay.get("scenario_key") or ""),
                    "mode": str(roleplay.get("mode") or "lesson_practice_coach"),
                }
                turns_by_slug[str(lesson["slug"])] = [
                    {
                        "coach": str(t.get("coach") or ""),
                        "hint": str(t.get("hint") or ""),
                        "sampleAnswer": str(t.get("sample_answer") or ""),
                        "focus": str(t.get("focus") or ""),
                        "expectedKeywords": [str(keyword) for keyword in (t.get("expected_keywords") or [])],
                        "indonesianExplanation": str(t.get("indonesian_explanation") or ""),
                    }
                    for t in turns
                ]
    return turns_by_slug, scenario_by_slug


def js_string(value: str) -> str:
    # JSON produces valid double-quoted JS string literals (escapes handled).
    return json.dumps(value, ensure_ascii=False)


def render_lessons(lessons: list[dict[str, Any]]) -> str:
    # Only a minimal lesson PREVIEW (title, one-line goal, hero) is emitted into
    # the client bundle. The gated body — including the goal details and
    # situation setup, plus dialogue, phrases, vocabulary, grammar, pronunciation,
    # prompts, quiz, reading/writing, and visual cards — is served at runtime by
    # the Pro-gated /lessons/{slug}/full endpoint and never bundled, so it cannot
    # be extracted from the browser by a free user.
    blocks: list[str] = []
    for lesson in lessons:
        lines = ["    {"]
        lines.append(f"      slug: {js_string(lesson['slug'])},")
        lines.append(f"      language: {js_string(lesson['language'])},")
        lines.append(f"      languageLabel: {js_string(lesson['languageLabel'])},")
        lines.append(f"      title: {js_string(lesson['title'])},")
        lines.append(f"      unit: {js_string(lesson['unit'])},")
        lines.append(f"      conversationGoal: {js_string(lesson['conversationGoal'])},")
        if lesson.get("visuals"):
            hero = lesson["visuals"]["hero"]
            lines.append("      visuals: {")
            lines.append(
                f"        hero: {{ src: {js_string(hero['src'])}, width: {int(hero['width'])}, "
                f"height: {int(hero['height'])}, alt: {js_string(hero['alt'])}, "
                f"caption: {js_string(hero['caption'])} }}"
            )
            lines.append("      },")
        lines.append("      sections: lessonSections")
        lines.append("    }")
        blocks.append("\n".join(lines))
    return ",\n".join(blocks)


def render_courses(courses: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for course in courses:
        lines = ["    {"]
        lines.append(f"      slug: {js_string(course['slug'])},")
        lines.append(f"      language: {js_string(course['language'])},")
        lines.append(f"      languageCode: {js_string(course['languageCode'])},")
        lines.append(f"      languageLabel: {js_string(course['languageLabel'])},")
        lines.append(f"      level: {js_string(course['level'])},")
        lines.append(f"      title: {js_string(course['title'])},")
        lines.append(f"      outcome: {js_string(course['outcome'])},")
        lines.append(f"      accessTier: {js_string(course['accessTier'])},")
        lines.append("      units: [")
        for unit in course["units"]:
            lines.append("        {")
            lines.append(f"          slug: {js_string(unit['slug'])},")
            lines.append(f"          title: {js_string(unit['title'])},")
            lines.append(f"          outcome: {js_string(unit['outcome'])},")
            lines.append("          progress: 0,")
            lines.append("          lessons: [")
            for lesson in unit["lessons"]:
                lines.append("            {")
                lines.append(f"              slug: {js_string(lesson['slug'])},")
                lines.append(f"              title: {js_string(lesson['title'])},")
                lines.append(f"              status: {js_string(lesson['status'])},")
                lines.append(f"              minutes: {int(lesson['minutes'])}")
                lines.append("            },")
            lines.append("          ]")
            lines.append("        },")
        lines.append("      ]")
        lines.append("    }")
        blocks.append("\n".join(lines))
    return ",\n".join(blocks)


def render_coach_turns(turns_by_slug: dict[str, list[dict[str, Any]]]) -> str:
    blocks: list[str] = []
    for slug in sorted(turns_by_slug):
        lines = [f"  {js_string(slug)}: ["]
        for turn in turns_by_slug[slug]:
            lines.append(
                f"    {{ coach: {js_string(turn['coach'])}, hint: {js_string(turn['hint'])}, "
                f"sampleAnswer: {js_string(turn['sampleAnswer'])}, focus: {js_string(turn['focus'])}, "
                f"expectedKeywords: {json.dumps(turn['expectedKeywords'], ensure_ascii=False)}, "
                f"indonesianExplanation: {js_string(turn['indonesianExplanation'])} }},"
            )
        lines.append("  ],")
        blocks.append("\n".join(lines))
    return "\n".join(blocks)


def render_coach_scenarios(scenario_by_slug: dict[str, dict[str, Any]]) -> str:
    blocks: list[str] = []
    for slug in sorted(scenario_by_slug):
        scenario = scenario_by_slug[slug]
        blocks.append(
            "  { "
            f"slug: {js_string(scenario['slug'])}, "
            f"label: {js_string(scenario['label'])}, "
            f"description: {js_string(scenario['description'])}, "
            f"language: {js_string(scenario['language'])}, "
            f"languageLabel: {js_string(scenario['languageLabel'])}, "
            f"levelCode: {js_string(scenario['levelCode'])}, "
            f"scenarioKey: {js_string(scenario['scenarioKey'])}, "
            f"mode: {js_string(scenario['mode'])} "
            "}"
        )
    return ",\n".join(blocks)


def render_block(lessons: list[dict[str, Any]]) -> str:
    return f"{BEGIN_MARKER}\n{render_lessons(lessons)}\n{END_MARKER}"


def splice_block(existing: str, begin_marker: str, end_marker: str, block: str) -> str:
    if begin_marker not in existing or end_marker not in existing:
        raise GeneratorError(
            f"data.ts is missing the {begin_marker} ... {end_marker} markers."
        )
    start = existing.index(begin_marker)
    end = existing.index(end_marker) + len(end_marker)
    return existing[:start] + block + existing[end:]


def render_courses_block(courses: list[dict[str, Any]]) -> str:
    return f"{COURSES_BEGIN_MARKER}\n{render_courses(courses)}\n{COURSES_END_MARKER}"


def render_coach_turns_block(turns_by_slug: dict[str, list[dict[str, Any]]]) -> str:
    return f"{COACH_TURNS_BEGIN_MARKER}\n{render_coach_turns(turns_by_slug)}\n{COACH_TURNS_END_MARKER}"


def render_coach_scenarios_block(scenario_by_slug: dict[str, dict[str, Any]]) -> str:
    return f"{COACH_SCENARIOS_BEGIN_MARKER}\n{render_coach_scenarios(scenario_by_slug)}\n{COACH_SCENARIOS_END_MARKER}"


def generate() -> str:
    """Return the full intended contents of data.ts (does not write)."""
    lessons = collect_lessons()
    courses = collect_courses()
    turns_by_slug, scenario_by_slug = collect_coach_turns()
    existing = DATA_TS.read_text(encoding="utf-8")
    existing = splice_block(existing, BEGIN_MARKER, END_MARKER, render_block(lessons))
    existing = splice_block(
        existing,
        COURSES_BEGIN_MARKER,
        COURSES_END_MARKER,
        render_courses_block(courses),
    )
    existing = splice_block(
        existing,
        COACH_TURNS_BEGIN_MARKER,
        COACH_TURNS_END_MARKER,
        render_coach_turns_block(turns_by_slug),
    )
    existing = splice_block(
        existing,
        COACH_SCENARIOS_BEGIN_MARKER,
        COACH_SCENARIOS_END_MARKER,
        render_coach_scenarios_block(scenario_by_slug),
    )
    return existing


def main() -> int:
    new_contents = generate()
    current_contents = DATA_TS.read_text(encoding="utf-8")
    check_only = "--check" in sys.argv[1:]

    if current_contents == new_contents:
        print("data.ts already in sync with curriculum.")
        return 0

    if check_only:
        print(
            "apps/web/lib/data.ts is out of sync with curriculum. Run:\n"
            "  PYTHONPATH=apps/api apps/api/.venv/bin/python "
            "scripts/generate_web_lesson_data.py",
            file=sys.stderr,
        )
        return 1

    DATA_TS.write_text(new_contents, encoding="utf-8")
    print(f"Regenerated {DATA_TS.relative_to(REPO_ROOT)} from curriculum.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
