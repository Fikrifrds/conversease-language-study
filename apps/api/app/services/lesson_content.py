"""Build the full, render-ready lesson body from curriculum content files.

The curriculum under content/curriculum/<LANGUAGE>/<LEVEL> is the single source
of truth. Both the build-time web data generator
(scripts/generate_web_lesson_data.py) and the runtime Pro-gated lesson endpoint
(GET /api/lessons/{slug}/full) use these helpers so the rendered shape never
drifts between them.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from app.data.curriculum import all_authored_courses, read_yaml, repo_root
from app.services.audio_generation import listening_script_to_dialogue_turns

# Audio-only markers that must be stripped from displayed dialogue text.
AUDIO_TAG_RE = re.compile(r"\((?:[a-z][a-z-]*)\)|<#\d+(?:\.\d+)?#>")


class LessonContentError(Exception):
    pass


def strip_audio_tags(text: str) -> str:
    cleaned = AUDIO_TAG_RE.sub("", text)
    return re.sub(r"\s{2,}", " ", cleaned).strip()


def lesson_dir_for(lesson: dict[str, Any]) -> Path:
    # content_files paths point inside the lesson directory.
    return Path(lesson["content_files"]["lesson"]).parent


def read_markdown(path: Path) -> str:
    if not path.exists():
        raise LessonContentError(f"Missing markdown file: {path}")
    return path.read_text(encoding="utf-8").strip()


def extract_patterns(grammar_notes_markdown: str) -> list[str]:
    match = re.search(r"```(?:txt)?\n([\s\S]*?)\n```", grammar_notes_markdown)
    if match:
        return [line.strip() for line in match.group(1).splitlines() if line.strip()][:12]

    fallback = re.search(
        r"^Pattern(?:s)?:\s*$([\s\S]*?)(?:\n\s*\n|^##\s+)",
        grammar_notes_markdown,
        re.MULTILINE,
    )
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


def parse_vocabulary(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []

    vocabulary_yaml = read_yaml(path)
    return [
        {
            "word": str(item.get("word") or ""),
            "meaning": str(item.get("meaning_id") or item.get("meaning") or ""),
            "usage": str(item.get("usage_note") or item.get("usage") or ""),
        }
        for item in vocabulary_yaml.get("vocabulary", [])
        if item.get("word")
    ]


def parse_visuals(path: Path, *, validate_assets: bool = True) -> dict[str, Any] | None:
    if not path.exists():
        return None

    visuals = read_yaml(path)
    hero = visuals.get("hero")
    cards = visuals.get("cards")
    if not isinstance(hero, dict):
        raise LessonContentError(f"{path}: visuals.hero must be a mapping")
    if not isinstance(cards, list) or len(cards) != 3:
        raise LessonContentError(f"{path}: visuals.cards must contain exactly 3 items")

    def clean_item(item: Any, label: str) -> dict[str, str]:
        if not isinstance(item, dict):
            raise LessonContentError(f"{path}: {label} must be a mapping")
        src = str(item.get("src") or "").strip()
        alt = str(item.get("alt") or "").strip()
        if not src.startswith("/images/"):
            raise LessonContentError(f"{path}: {label}.src must start with /images/")
        if not alt:
            raise LessonContentError(f"{path}: {label}.alt is required")
        width = int(item.get("width") or 0)
        height = int(item.get("height") or 0)
        if width < 1 or height < 1:
            raise LessonContentError(f"{path}: {label}.width and {label}.height are required")

        # The build-time generator validates the asset exists on disk; the
        # runtime endpoint skips this since web assets live in apps/web/public.
        if validate_assets:
            asset_path = repo_root() / "apps" / "web" / "public" / src.removeprefix("/")
            if not asset_path.exists():
                raise LessonContentError(f"{path}: visual asset does not exist: {asset_path}")

        return {
            "src": src,
            "width": width,
            "height": height,
            "alt": alt,
            "label": str(item.get("label") or "").strip(),
            "caption": str(item.get("caption") or "").strip(),
        }

    return {
        "hero": clean_item(hero, "hero"),
        "cards": [clean_item(card, f"cards[{index}]") for index, card in enumerate(cards)],
    }


def extract_situation(lesson_md: Path) -> str:
    text = lesson_md.read_text(encoding="utf-8")
    # Header is "## Situation" or "## Situation Setup".
    match = re.search(r"^##\s+Situation(?:\s+Setup)?\s*$", text, re.MULTILINE)
    if not match:
        raise LessonContentError(f"No Situation section in {lesson_md}")
    rest = text[match.end():]
    body = rest.split("\n##", 1)[0]
    paragraph = next((p.strip() for p in body.split("\n\n") if p.strip()), "")
    return paragraph.replace("\n", " ").strip()


def language_label(language: str) -> str:
    labels = {
        "english": "English",
        "arabic": "Arabic",
    }
    return labels.get(language, language.replace("-", " ").title())


def build_lesson(
    course: dict[str, Any],
    unit_title: str,
    lesson: dict[str, Any],
    *,
    validate_assets: bool = True,
) -> dict[str, Any]:
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
        raise LessonContentError(
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
    vocabulary = parse_vocabulary(lesson_dir / "vocabulary.yaml")

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
        raise LessonContentError(
            f"{slug}: lesson.yaml is missing grammar_summary (the 1-line text shown "
            f"in the 'Grammar for Conversation' box on the lesson page)."
        )

    return {
        "slug": slug,
        "language": course.get("language") or "english",
        "languageCode": course.get("language_code") or "",
        "languageLabel": language_label(str(course.get("language") or "english")),
        "courseSlug": course.get("course_slug") or "",
        "level": course.get("level_code") or "",
        "title": lesson["title"],
        "unit": unit_title,
        "conversationGoal": lesson["conversation_goal"],
        "conversationGoalDetails": conversation_goal_details,
        "setup": extract_situation(lesson_dir / "lesson.md"),
        "dialogue": dialogue,
        "translation": translation,
        "phrases": phrases,
        "vocabulary": vocabulary,
        "grammar": grammar,
        "grammarNotes": grammar_notes,
        "patterns": patterns,
        "pronunciationDrill": pronunciation_drill,
        "prompts": prompts,
        "quiz": quiz,
        "readingSupport": reading_support,
        "writingSupport": writing_support,
        "visuals": parse_visuals(lesson_dir / "visuals.yaml", validate_assets=validate_assets),
    }


def build_lesson_body_or_none(slug: str) -> dict[str, Any] | None:
    """Render-ready full lesson body for one slug, or None when it doesn't exist.

    Locates the lesson in the curriculum and builds it with the same shape the
    web app expects. Used by the runtime Pro-gated lesson endpoint, so visual
    assets (which live under apps/web/public, not the API) are not re-validated.
    """
    for course in all_authored_courses():
        for unit in course["units"]:
            for lesson in unit["lessons"]:
                if lesson["slug"] == slug:
                    return build_lesson(
                        course,
                        unit["title"],
                        lesson,
                        validate_assets=False,
                    )
    return None
