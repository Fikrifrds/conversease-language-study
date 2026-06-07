from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

import yaml


COURSE_SLUG = "english-a1-start-simple-conversations"
COURSE_TITLE = "Start Simple Conversations"
LEVEL_CODE = "A1"
LEVEL_NAME = "A1 - Start Simple Conversations"
LANGUAGE_CODE = "en"

SECTION_LABELS = {
    "conversation_goal": "Conversation Goal",
    "situation_setup": "Situation Setup",
    "listening": "Listen to a Dialogue",
    "comprehension_check": "Understand the Conversation",
    "useful_phrases": "Useful Phrases",
    "grammar_for_conversation": "Grammar for Conversation",
    "speak_clearly": "Speak Clearly",
    "response_practice": "Respond Practice",
    "conversation_coach_roleplay": "Conversation Coach Roleplay",
    "conversation_feedback": "Conversation Feedback",
    "conversation_check": "Conversation Check",
}

REQUIRED_LESSON_FILES = (
    "audio_manifest.yaml",
    "conversation_goal.md",
    "grammar_for_conversation.md",
    "lesson.md",
    "lesson.yaml",
    "listening_script.md",
    "pronunciation_drill.md",
    "reading_support.md",
    "transcript_translation.md",
    "useful_phrases.yaml",
    "response_prompts.yaml",
    "quiz.yaml",
    "conversation_coach_roleplay.yaml",
    "writing_support.md",
)

FINAL_EVALUATION_REQUIRED_FIELDS = (
    "level_code",
    "title",
    "status",
    "overall_threshold",
    "lesson_completion_required_percent",
    "critical_skills",
    "sections",
)

PRODUCTION_TRACKER_COLUMNS = (
    "level",
    "unit",
    "lesson",
    "lesson_md",
    "listening_script",
    "audio_generated",
    "phrases",
    "grammar",
    "pronunciation",
    "response_prompts",
    "conversation_coach",
    "quiz",
    "reading",
    "writing",
    "review_status",
    "publish_status",
)

PRODUCTION_TRACKER_DONE_COLUMNS = (
    "lesson_md",
    "listening_script",
    "phrases",
    "grammar",
    "pronunciation",
    "response_prompts",
    "conversation_coach",
    "quiz",
    "reading",
    "writing",
)

PRODUCTION_TRACKER_ALLOWED_AUDIO_STATUS = {"done", "no", "not_generated"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def curriculum_root() -> Path:
    return repo_root() / "content" / "curriculum"


def production_tracker_path() -> Path:
    return repo_root() / "content" / "production_tracker.csv"


def level_root(*, language: str = "english", level_code: str) -> Path:
    return curriculum_root() / language / level_code


def a1_root() -> Path:
    return level_root(language="english", level_code=LEVEL_CODE)


@lru_cache(maxsize=1)
def load_a1_course() -> dict[str, Any]:
    return load_course(level_code=LEVEL_CODE)


@lru_cache(maxsize=8)
def load_course(*, language: str = "english", level_code: str) -> dict[str, Any]:
    root = level_root(language=language, level_code=level_code)
    units_root = root / "units"
    units = (
        [load_unit(unit_dir) for unit_dir in sorted(units_root.iterdir()) if unit_dir.is_dir()]
        if units_root.exists()
        else []
    )

    plan_path = root / "content_plan.yaml"
    plan = read_yaml(plan_path) if plan_path.exists() else {}
    course_slug = plan.get("course_slug") or (COURSE_SLUG if level_code == "A1" else "")
    course_title = plan.get("course_title") or (COURSE_TITLE if level_code == "A1" else "")
    language_code = plan.get("language_code") or (LANGUAGE_CODE if level_code == "A1" else "")
    level_name = LEVEL_NAME if level_code == "A1" else level_code

    return {
        "language_code": language_code,
        "level_code": level_code,
        "level_name": level_name,
        "course_slug": course_slug,
        "course_title": course_title,
        "units": units,
    }


def load_unit(unit_dir: Path) -> dict[str, Any]:
    unit_data = read_yaml(unit_dir / "unit.yaml")
    lesson_dirs = [unit_dir / lesson_key for lesson_key in unit_data.get("lessons", [])]
    lessons = [load_lesson(lesson_dir) for lesson_dir in lesson_dirs]

    return {
        "slug": unit_data["unit_key"],
        "title": unit_data["title"],
        "outcome": unit_data["main_conversation_outcome"],
        "status": unit_data["status"],
        "lessons": lessons,
    }


def load_lesson(lesson_dir: Path) -> dict[str, Any]:
    lesson_data = read_yaml(lesson_dir / "lesson.yaml")
    roleplay = read_yaml(lesson_dir / "conversation_coach_roleplay.yaml")
    sections = [
        SECTION_LABELS.get(section_key, section_key.replace("_", " ").title())
        for section_key in lesson_data.get("required_sections", [])
    ]

    return {
        "lesson_key": lesson_data["lesson_key"],
        "slug": lesson_data["slug"],
        "title": lesson_data["title"],
        "conversation_goal": lesson_data["conversation_goal"],
        "conversation_situation": lesson_data["conversation_situation"],
        "status": lesson_data["status"],
        "estimated_minutes": lesson_data["estimated_minutes"],
        "sections": sections,
        "required_section_keys": lesson_data.get("required_sections", []),
        "completion_rules": lesson_data.get("completion_rules", {}),
        "roleplay": {
            "scenario_key": roleplay["scenario_key"],
            "mode": roleplay["mode"],
            "level_code": roleplay.get("level_code", ""),
            "opening_line": roleplay["opening_line"],
            "learner_goal": roleplay["learner_goal"],
            "max_turns": roleplay["max_turns"],
            "target_phrases": roleplay.get("target_phrases", []),
            "rubric": roleplay.get("rubric", {}),
            "turns": roleplay.get("turns", []),
        },
        "content_files": {
            "lesson": str(lesson_dir / "lesson.md"),
            "useful_phrases": str(lesson_dir / "useful_phrases.yaml"),
            "response_prompts": str(lesson_dir / "response_prompts.yaml"),
            "quiz": str(lesson_dir / "quiz.yaml"),
            "conversation_coach_roleplay": str(lesson_dir / "conversation_coach_roleplay.yaml"),
        },
    }


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")
    return data


@lru_cache(maxsize=1)
def load_a1_final_evaluation() -> dict[str, Any]:
    data = read_yaml(a1_root() / "final_evaluation.yaml")
    return {
        **data,
        "sections": data.get("sections", []),
        "critical_skills": data.get("critical_skills", []),
    }


def get_lesson_or_none(lesson_slug: str) -> Optional[dict[str, Any]]:
    for unit in A1_COURSE["units"]:
        for lesson in unit["lessons"]:
            if lesson["slug"] == lesson_slug:
                return {**lesson, "unit_slug": unit["slug"], "unit_title": unit["title"]}
    return None


def public_course_payload(course: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    source = course or A1_COURSE
    return {
        **source,
        "units": [
            {
                **unit,
                "lessons": [public_lesson_payload(lesson) for lesson in unit["lessons"]],
            }
            for unit in source["units"]
        ],
    }


def public_lesson_payload(lesson: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in lesson.items() if key != "content_files"}


def public_final_evaluation_payload(evaluation: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    source = evaluation or load_a1_final_evaluation()
    return {
        "level_code": source["level_code"],
        "title": source["title"],
        "status": source["status"],
        "description": source.get("description", ""),
        "overall_threshold": source["overall_threshold"],
        "lesson_completion_required_percent": source["lesson_completion_required_percent"],
        "critical_skills": source.get("critical_skills", []),
        "sections": source.get("sections", []),
    }


def published_lessons() -> list[dict[str, Any]]:
    lessons = []
    for unit in A1_COURSE["units"]:
        for lesson in unit["lessons"]:
            if lesson.get("status") == "published":
                lessons.append({**lesson, "unit_slug": unit["slug"], "unit_title": unit["title"]})
    return lessons


def validate_curriculum_content() -> list[str]:
    issues: list[str] = []
    course = load_a1_course()
    seen_slugs: set[str] = set()
    final_evaluation = a1_root() / "final_evaluation.yaml"

    if not final_evaluation.exists():
        issues.append(f"Missing final evaluation file: {final_evaluation}")
    else:
        issues.extend(validate_final_evaluation(load_a1_final_evaluation()))

    for unit in course["units"]:
        if unit.get("status") != "published":
            issues.append(f"Unit is not published: {unit['slug']}")

        for lesson in unit["lessons"]:
            slug = lesson["slug"]
            if slug in seen_slugs:
                issues.append(f"Duplicate lesson slug: {slug}")
            seen_slugs.add(slug)

            if lesson.get("status") != "published":
                issues.append(f"Lesson is not published: {slug}")

            if not lesson.get("sections"):
                issues.append(f"Lesson has no required sections: {slug}")

            if not lesson.get("roleplay", {}).get("opening_line"):
                issues.append(f"Lesson has no roleplay opening line: {slug}")

            lesson_dir = Path(lesson["content_files"]["lesson"]).parent
            for filename in REQUIRED_LESSON_FILES:
                file_path = lesson_dir / filename
                if not file_path.exists():
                    issues.append(f"Missing lesson content file for {slug}: {file_path}")

    issues.extend(validate_production_tracker(course))
    return issues


def validate_production_tracker(course: Optional[dict[str, Any]] = None) -> list[str]:
    issues: list[str] = []
    tracker_path = production_tracker_path()
    source = course or load_a1_course()

    if not tracker_path.exists():
        return [f"Missing production tracker: {tracker_path}"]

    with tracker_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != list(PRODUCTION_TRACKER_COLUMNS):
            issues.append("Production tracker columns do not match the release schema")
            return issues
        rows = list(reader)

    tracker_by_key = {
        (row["level"], row["unit"], row["lesson"]): row
        for row in rows
        if row.get("level") and row.get("unit") and row.get("lesson")
    }

    expected_keys: set[tuple[str, str, str]] = set()
    for unit in source["units"]:
        for lesson in unit["lessons"]:
            if lesson.get("status") != "published":
                continue

            key = (source["level_code"], unit["slug"], lesson["lesson_key"])
            expected_keys.add(key)
            row = tracker_by_key.get(key)
            if row is None:
                issues.append(f"Production tracker missing published lesson: {lesson['lesson_key']}")
                continue

            for column in PRODUCTION_TRACKER_DONE_COLUMNS:
                if row[column] != "done":
                    issues.append(
                        f"Production tracker {lesson['lesson_key']} column {column} must be done"
                    )

            if row["audio_generated"] not in PRODUCTION_TRACKER_ALLOWED_AUDIO_STATUS:
                issues.append(
                    f"Production tracker {lesson['lesson_key']} audio_generated has invalid status"
                )

            if row["review_status"] != "ready":
                issues.append(f"Production tracker {lesson['lesson_key']} review_status must be ready")

            if row["publish_status"] != "published":
                issues.append(
                    f"Production tracker {lesson['lesson_key']} publish_status must be published"
                )

    extra_keys = {key for key in tracker_by_key if key[0] == source["level_code"]} - expected_keys
    for level, unit, lesson in sorted(extra_keys):
        issues.append(f"Production tracker has extra lesson row: {level}/{unit}/{lesson}")

    if len(tracker_by_key) != len(rows):
        issues.append("Production tracker has rows with missing level, unit, or lesson")

    return issues


def validate_final_evaluation(evaluation: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    for field in FINAL_EVALUATION_REQUIRED_FIELDS:
        if field not in evaluation:
            issues.append(f"Final evaluation missing field: {field}")

    if issues:
        return issues

    if evaluation.get("level_code") != LEVEL_CODE:
        issues.append("Final evaluation level_code must be A1")

    if evaluation.get("status") != "published":
        issues.append("Final evaluation must be published")

    overall_threshold = int(evaluation.get("overall_threshold", 0))
    if overall_threshold < 1 or overall_threshold > 100:
        issues.append("Final evaluation overall_threshold must be 1-100")

    completion_required = int(evaluation.get("lesson_completion_required_percent", 0))
    if completion_required < 0 or completion_required > 100:
        issues.append("Final evaluation lesson_completion_required_percent must be 0-100")

    sections = evaluation.get("sections", [])
    if not isinstance(sections, list) or not sections:
        issues.append("Final evaluation sections are required")
        return issues

    seen_keys: set[str] = set()
    weight_total = 0
    minimums: dict[str, int] = {}

    for section in sections:
        key = section.get("key")
        if not key:
            issues.append("Final evaluation section key is required")
            continue
        if key in seen_keys:
            issues.append(f"Duplicate final evaluation section: {key}")
        seen_keys.add(key)

        weight = int(section.get("weight", 0))
        if weight < 1 or weight > 100:
            issues.append(f"Invalid final evaluation section weight: {key}")
        weight_total += weight

        minimum_score = int(section.get("minimum_score", 0))
        if minimum_score < 1 or minimum_score > 100:
            issues.append(f"Invalid final evaluation minimum score: {key}")
        minimums[key] = minimum_score

        task = section.get("task", {})
        if not isinstance(task, dict) or not task.get("prompt"):
            issues.append(f"Final evaluation section has no task prompt: {key}")
        if not task.get("success_criteria"):
            issues.append(f"Final evaluation section has no success criteria: {key}")

    if weight_total != 100:
        issues.append(f"Final evaluation section weights must total 100, got {weight_total}")

    for skill in evaluation.get("critical_skills", []):
        if skill not in minimums:
            issues.append(f"Critical skill has no final evaluation section: {skill}")

    return issues


A1_COURSE = load_a1_course()


def refresh_a1_course() -> dict[str, Any]:
    load_a1_course.cache_clear()
    load_course.cache_clear()
    load_a1_final_evaluation.cache_clear()
    fresh_course = load_a1_course()
    A1_COURSE.clear()
    A1_COURSE.update(fresh_course)
    return A1_COURSE
