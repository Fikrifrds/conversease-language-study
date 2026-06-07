#!/usr/bin/env python3
"""Generate the lesson array in apps/web/lib/data.ts from the curriculum files.

The curriculum under content/curriculum/english/<LEVEL> is the SINGLE SOURCE OF TRUTH
for lesson content. The web app renders a static lessons array from
apps/web/lib/data.ts; this script regenerates that array (and only that array,
between the // <generated:lessons> markers) so the two never drift.

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

# Reuse the curriculum loader and dialogue parser from the API package.
sys.path.insert(0, str(API_ROOT))
from app.data.curriculum import load_course, read_yaml  # noqa: E402
from app.services.audio_generation import (  # noqa: E402
    listening_script_to_dialogue_turns,
)

BEGIN_MARKER = "  // <generated:lessons>"
END_MARKER = "  // </generated:lessons>"

COURSES_BEGIN_MARKER = "  // <generated:courses>"
COURSES_END_MARKER = "  // </generated:courses>"

COACH_TURNS_BEGIN_MARKER = "  // <generated:coach_turns>"
COACH_TURNS_END_MARKER = "  // </generated:coach_turns>"

COACH_SCENARIOS_BEGIN_MARKER = "  // <generated:coach_scenarios>"
COACH_SCENARIOS_END_MARKER = "  // </generated:coach_scenarios>"

# Audio-only markers that must be stripped from displayed dialogue text.
AUDIO_TAG_RE = re.compile(r"\((?:[a-z][a-z-]*)\)|<#\d+(?:\.\d+)?#>")


class GeneratorError(Exception):
    pass


def strip_audio_tags(text: str) -> str:
    cleaned = AUDIO_TAG_RE.sub("", text)
    return re.sub(r"\s{2,}", " ", cleaned).strip()


def lesson_dir_for(lesson: dict[str, Any]) -> Path:
    # content_files paths point inside the lesson directory.
    return Path(lesson["content_files"]["lesson"]).parent


def read_markdown(path: Path) -> str:
    if not path.exists():
        raise GeneratorError(f"Missing markdown file: {path}")
    return path.read_text(encoding="utf-8").strip()


def extract_patterns(grammar_notes_markdown: str) -> list[str]:
    match = re.search(r"```(?:txt)?\n([\s\S]*?)\n```", grammar_notes_markdown)
    if match:
        return [line.strip() for line in match.group(1).splitlines() if line.strip()][:12]

    fallback = re.search(r"^Pattern(?:s)?:\s*$([\s\S]*?)(?:\n\s*\n|^##\s+)", grammar_notes_markdown, re.MULTILINE)
    if fallback:
        raw = fallback.group(1)
        lines = []
        for line in raw.splitlines():
            cleaned = line.strip().lstrip("-").strip()
            if cleaned:
                lines.append(cleaned)
        return lines[:12]

    return []


def parse_translations(path: Path) -> list[str]:
    """Return the Indonesian side of transcript_translation.md, in order.

    Supports both formats present in the repo:
      - `- **Speaker:** English -> Indonesian`
      - `| English | Indonesian |` table rows (skips header/separator).
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    for raw in lines:
        line = raw.strip()
        if line.startswith("- ") and "->" in line:
            out.append(line.split("->", 1)[1].strip())
        elif line.startswith("|") and line.count("|") >= 3:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 2:
                continue
            english = cells[0].lower()
            # skip header row and markdown separator row
            if english in {"english", "english phrase"} or set(cells[0]) <= {"-", " ", ":"}:
                continue
            out.append(cells[1])
    return out


def extract_situation(lesson_md: Path) -> str:
    text = lesson_md.read_text(encoding="utf-8")
    # Header is "## Situation" or "## Situation Setup".
    match = re.search(r"^##\s+Situation(?:\s+Setup)?\s*$", text, re.MULTILINE)
    if not match:
        raise GeneratorError(f"No Situation section in {lesson_md}")
    rest = text[match.end():]
    body = rest.split("\n##", 1)[0]
    paragraph = next((p.strip() for p in body.split("\n\n") if p.strip()), "")
    return paragraph.replace("\n", " ").strip()


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


def build_lesson(unit_title: str, lesson: dict[str, Any]) -> dict[str, Any]:
    lesson_dir = lesson_dir_for(lesson)
    slug = lesson["slug"]

    conversation_goal_details = read_markdown(lesson_dir / "conversation_goal.md")
    grammar_notes = read_markdown(lesson_dir / "grammar_for_conversation.md")
    pronunciation_drill = read_markdown(lesson_dir / "pronunciation_drill.md")
    reading_support = read_markdown(lesson_dir / "reading_support.md")
    writing_support = read_markdown(lesson_dir / "writing_support.md")
    patterns = extract_patterns(grammar_notes)

    turns = listening_script_to_dialogue_turns(lesson_dir / "listening_script.md")
    dialogue = [
        {"speaker": t.speaker, "text": strip_audio_tags(t.text)} for t in turns
    ]
    translation = parse_translations(lesson_dir / "transcript_translation.md")

    if len(dialogue) != len(translation):
        raise GeneratorError(
            f"{slug}: dialogue has {len(dialogue)} lines but transcript_translation "
            f"has {len(translation)}. Re-sync listening_script.md and "
            f"transcript_translation.md so they line up 1:1."
        )

    phrases_yaml = read_yaml(lesson_dir / "useful_phrases.yaml")
    phrases = [
        {
            "phrase": p["phrase"],
            "meaning": p["meaning_id"],
            "usage": p["usage_note"],
        }
        for p in phrases_yaml.get("phrases", [])
    ]

    # Two authoring formats exist across the curriculum; accept both.
    prompts_yaml = read_yaml(lesson_dir / "response_prompts.yaml")
    prompts = [
        p.get("prompt") or p.get("prompt_en")
        for p in prompts_yaml.get("prompts", [])
    ]

    quiz_yaml = read_yaml(lesson_dir / "quiz.yaml")
    quiz = [
        {
            "question": q["prompt"],
            "answer": q.get("answer") or q.get("correct_answer"),
        }
        for q in quiz_yaml.get("questions", [])
    ]

    lesson_yaml = read_yaml(lesson_dir / "lesson.yaml")
    grammar = lesson_yaml.get("grammar_summary")
    if not grammar:
        raise GeneratorError(
            f"{slug}: lesson.yaml is missing grammar_summary (the 1-line text shown "
            f"in the 'Grammar for Conversation' box on the lesson page)."
        )

    return {
        "slug": slug,
        "title": lesson["title"],
        "unit": unit_title,
        "conversationGoal": lesson["conversation_goal"],
        "conversationGoalDetails": conversation_goal_details,
        "setup": extract_situation(lesson_dir / "lesson.md"),
        "dialogue": dialogue,
        "translation": translation,
        "phrases": phrases,
        "grammar": grammar,
        "grammarNotes": grammar_notes,
        "patterns": patterns,
        "pronunciationDrill": pronunciation_drill,
        "prompts": prompts,
        "quiz": quiz,
        "readingSupport": reading_support,
        "writingSupport": writing_support,
    }


def collect_lessons() -> list[dict[str, Any]]:
    lessons: list[dict[str, Any]] = []
    for level_code in ("A1", "A2", "B1", "B2", "C1"):
        course = load_course(level_code=level_code)
        for unit in course["units"]:
            for lesson in unit["lessons"]:
                lessons.append(build_lesson(unit["title"], lesson))
    return lessons


def collect_courses() -> list[dict[str, Any]]:
    courses: list[dict[str, Any]] = []
    for level_code in ("A1", "A2", "B1", "B2", "C1"):
        course = load_course(level_code=level_code)
        if not course.get("units"):
            continue
        outcome = extract_level_outcome(
            REPO_ROOT / "content" / "curriculum" / "english" / level_code / "LEVEL_SPEC.md"
        )
        courses.append(
            {
                "slug": course.get("course_slug") or "",
                "level": level_code,
                "title": course.get("course_title") or "",
                "outcome": outcome,
                "units": [
                    {
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
    for level_code in ("A1", "A2", "B1", "B2", "C1"):
        course = load_course(level_code=level_code)
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
                    }
                    for t in turns
                ]
    return turns_by_slug, scenario_by_slug


def js_string(value: str) -> str:
    # JSON produces valid double-quoted JS string literals (escapes handled).
    return json.dumps(value, ensure_ascii=False)


def render_lessons(lessons: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for lesson in lessons:
        lines = ["    {"]
        lines.append(f"      slug: {js_string(lesson['slug'])},")
        lines.append(f"      title: {js_string(lesson['title'])},")
        lines.append(f"      unit: {js_string(lesson['unit'])},")
        lines.append(f"      conversationGoal: {js_string(lesson['conversationGoal'])},")
        lines.append(f"      conversationGoalDetails: {js_string(lesson['conversationGoalDetails'])},")
        lines.append(f"      setup: {js_string(lesson['setup'])},")
        lines.append("      dialogue: [")
        for d in lesson["dialogue"]:
            lines.append(
                f"        {{ speaker: {js_string(d['speaker'])}, text: {js_string(d['text'])} }},"
            )
        lines.append("      ],")
        lines.append("      translation: [")
        for t in lesson["translation"]:
            lines.append(f"        {js_string(t)},")
        lines.append("      ],")
        lines.append("      phrases: [")
        for p in lesson["phrases"]:
            lines.append(
                f"        {{ phrase: {js_string(p['phrase'])}, meaning: {js_string(p['meaning'])}, "
                f"usage: {js_string(p['usage'])} }},"
            )
        lines.append("      ],")
        lines.append(f"      grammar: {js_string(lesson['grammar'])},")
        lines.append(f"      grammarNotes: {js_string(lesson['grammarNotes'])},")
        lines.append("      patterns: [")
        for pattern in lesson["patterns"]:
            lines.append(f"        {js_string(pattern)},")
        lines.append("      ],")
        lines.append(f"      pronunciationDrill: {js_string(lesson['pronunciationDrill'])},")
        lines.append("      prompts: [")
        for prompt in lesson["prompts"]:
            lines.append(f"        {js_string(prompt)},")
        lines.append("      ],")
        lines.append("      quiz: [")
        for q in lesson["quiz"]:
            lines.append(
                f"        {{ question: {js_string(q['question'])}, answer: {js_string(q['answer'])} }},"
            )
        lines.append("      ],")
        lines.append(f"      readingSupport: {js_string(lesson['readingSupport'])},")
        lines.append(f"      writingSupport: {js_string(lesson['writingSupport'])},")
        lines.append("      sections: lessonSections")
        lines.append("    }")
        blocks.append("\n".join(lines))
    return ",\n".join(blocks)


def render_courses(courses: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for course in courses:
        lines = ["    {"]
        lines.append(f"      slug: {js_string(course['slug'])},")
        lines.append(f"      level: {js_string(course['level'])},")
        lines.append(f"      title: {js_string(course['title'])},")
        lines.append(f"      outcome: {js_string(course['outcome'])},")
        lines.append("      units: [")
        for unit in course["units"]:
            lines.append("        {")
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
                f"sampleAnswer: {js_string(turn['sampleAnswer'])}, focus: {js_string(turn['focus'])} }},"
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
    if DATA_TS.read_text(encoding="utf-8") == new_contents:
        print("data.ts already in sync with curriculum.")
        return 0
    DATA_TS.write_text(new_contents, encoding="utf-8")
    print(f"Regenerated {DATA_TS.relative_to(REPO_ROOT)} from curriculum.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
