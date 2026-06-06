#!/usr/bin/env python3
"""Generate the lesson array in apps/web/lib/data.ts from the curriculum files.

The curriculum under content/curriculum/english/A1 is the SINGLE SOURCE OF TRUTH
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
from app.data.curriculum import load_a1_course, read_yaml  # noqa: E402
from app.services.audio_generation import (  # noqa: E402
    listening_script_to_dialogue_turns,
)

BEGIN_MARKER = "  // <generated:lessons>"
END_MARKER = "  // </generated:lessons>"

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


def build_lesson(unit_title: str, lesson: dict[str, Any]) -> dict[str, Any]:
    lesson_dir = lesson_dir_for(lesson)
    slug = lesson["slug"]

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
        "setup": extract_situation(lesson_dir / "lesson.md"),
        "dialogue": dialogue,
        "translation": translation,
        "phrases": phrases,
        "grammar": grammar,
        "prompts": prompts,
        "quiz": quiz,
    }


def collect_lessons() -> list[dict[str, Any]]:
    course = load_a1_course()
    lessons: list[dict[str, Any]] = []
    for unit in course["units"]:
        for lesson in unit["lessons"]:
            lessons.append(build_lesson(unit["title"], lesson))
    return lessons


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
        lines.append("      sections: lessonSections")
        lines.append("    }")
        blocks.append("\n".join(lines))
    return ",\n".join(blocks)


def render_block(lessons: list[dict[str, Any]]) -> str:
    return f"{BEGIN_MARKER}\n{render_lessons(lessons)}\n{END_MARKER}"


def splice_into_data_ts(existing: str, block: str) -> str:
    if BEGIN_MARKER not in existing or END_MARKER not in existing:
        raise GeneratorError(
            "data.ts is missing the // <generated:lessons> ... // </generated:lessons> "
            "markers. Add them around the lesson array before running the generator."
        )
    start = existing.index(BEGIN_MARKER)
    end = existing.index(END_MARKER) + len(END_MARKER)
    return existing[:start] + block + existing[end:]


def generate() -> str:
    """Return the full intended contents of data.ts (does not write)."""
    lessons = collect_lessons()
    block = render_block(lessons)
    return splice_into_data_ts(DATA_TS.read_text(encoding="utf-8"), block)


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
