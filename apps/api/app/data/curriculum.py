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
SUPPORTED_LEVEL_CODES = ("A1", "A2", "B1", "B2", "C1")
SUPPORTED_LANGUAGE_ORDER = ("english", "arabic")
LANGUAGE_CODES = {"english": "en", "arabic": "ar"}
LEVEL_TEST_LANGUAGE_PREFIXES = {"arabic": "AR"}
# Levels free to all users; everything else requires a Pro subscription.
FREE_LEVEL_CODES = ("A1",)


def requires_pro(level_code: str) -> bool:
    return level_code.upper() not in FREE_LEVEL_CODES


def course_requires_pro(course: dict[str, Any]) -> bool:
    access_tier = str(course.get("access_tier") or "").strip().lower()
    if access_tier in {"pro", "pro_beta"}:
        return True
    if access_tier in {"free", "public"}:
        return False
    return requires_pro(str(course.get("level_code") or ""))


def lesson_requires_pro(lesson: Optional[dict[str, Any]]) -> bool:
    if not lesson:
        return False
    access_tier = str(lesson.get("access_tier") or "").strip().lower()
    if access_tier in {"pro", "pro_beta"}:
        return True
    if access_tier in {"free", "public"}:
        return False
    return requires_pro(str(lesson.get("level_code") or ""))

SECTION_LABELS = {
    "conversation_goal": "Conversation Goal",
    "situation_setup": "Situation Setup",
    "listening": "Listen to a Dialogue",
    "comprehension_check": "Understand the Conversation",
    "useful_phrases": "Useful Phrases",
    "vocabulary": "Vocabulary",
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
    "visuals.yaml",
)

REQUIRED_COMPLETION_RULES = (
    "listening_completed",
    "quiz_required",
    "speaking_attempt_required",
    "minimum_score",
)

REQUIRED_ROLEPLAY_RUBRIC_KEYS = (
    "speaking",
    "relevance",
    "grammar",
)

MIN_VOCABULARY_ITEMS = 3
MIN_RESPONSE_PROMPTS = 3
MIN_QUIZ_QUESTIONS = 2
MIN_QUIZ_OPTIONS = 3

REQUIRED_LEVEL_SPEC_SECTIONS = (
    "## Level Outcome",
    "## Passing Threshold",
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


def normalize_language(language: str = "english") -> str:
    normalized = (language or "english").strip().lower()
    if normalized in {"en", "eng"}:
        return "english"
    if normalized in {"ar", "ara"}:
        return "arabic"
    return normalized


def level_test_attempt_code(*, language: str = "english", level_code: str) -> str:
    normalized_language = normalize_language(language)
    normalized_level = level_code.upper()
    prefix = LEVEL_TEST_LANGUAGE_PREFIXES.get(normalized_language)
    return f"{prefix}-{normalized_level}" if prefix else normalized_level


def parse_level_test_attempt_code(level_code: str) -> tuple[str, str]:
    normalized = level_code.upper()
    for language, prefix in LEVEL_TEST_LANGUAGE_PREFIXES.items():
        marker = f"{prefix}-"
        if normalized.startswith(marker):
            return language, normalized[len(marker):]
    return "english", normalized


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
        "language": language,
        "language_code": language_code,
        "level_code": level_code,
        "level_name": level_name,
        "course_slug": course_slug,
        "course_title": course_title,
        "access_tier": plan.get("access_tier") or "",
        "units": units,
    }


@lru_cache(maxsize=1)
def all_courses() -> tuple[dict[str, Any], ...]:
    """English levels that have authored content, in level order (A1 -> C1).

    This preserves the existing English learning-progress and unlock behavior.
    Use all_authored_courses() for cross-language discovery.
    """
    courses = []
    for level_code in SUPPORTED_LEVEL_CODES:
        course = load_course(level_code=level_code)
        if course["units"]:
            courses.append(course)
    return tuple(courses)


@lru_cache(maxsize=1)
def all_authored_courses() -> tuple[dict[str, Any], ...]:
    """All authored courses across language folders.

    Course ordering is product-stable: English remains first, then other
    authored languages. English-only flows should keep using all_courses()
    until product-scoped access is added.
    """
    courses = []
    for plan_path in sorted(curriculum_root().glob("*/*/content_plan.yaml"), key=authored_plan_sort_key):
        language = plan_path.parents[1].name
        level_code = plan_path.parent.name
        course = load_course(language=language, level_code=level_code)
        if course["units"]:
            courses.append(course)
    return tuple(courses)


def authored_plan_sort_key(path: Path) -> tuple[int, int, str, str]:
    language = path.parents[1].name
    level_code = path.parent.name
    try:
        language_index = SUPPORTED_LANGUAGE_ORDER.index(language)
    except ValueError:
        language_index = len(SUPPORTED_LANGUAGE_ORDER)
    try:
        level_index = SUPPORTED_LEVEL_CODES.index(level_code)
    except ValueError:
        level_index = len(SUPPORTED_LEVEL_CODES)
    return (language_index, level_index, language, level_code)


def get_course_by_slug(slug: str) -> Optional[dict[str, Any]]:
    for course in all_authored_courses():
        if course["course_slug"] == slug:
            return course
    return None


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
            "vocabulary": str(lesson_dir / "vocabulary.yaml"),
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


def has_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def normalized_text(value: Any) -> str:
    return " ".join(str(value or "").split()).casefold()


def validate_lesson_practice_files(slug: str, lesson_dir: Path) -> list[str]:
    issues: list[str] = []
    issues.extend(validate_vocabulary(slug, lesson_dir / "vocabulary.yaml"))
    issues.extend(validate_response_prompts(slug, lesson_dir / "response_prompts.yaml"))
    issues.extend(validate_quiz(slug, lesson_dir / "quiz.yaml"))
    return issues


def validate_vocabulary(slug: str, path: Path) -> list[str]:
    if not path.exists():
        return []

    issues: list[str] = []
    items = read_yaml(path).get("vocabulary")
    if not isinstance(items, list):
        return [f"Vocabulary file must contain a vocabulary list: {slug}"]
    if len(items) < MIN_VOCABULARY_ITEMS:
        issues.append(
            f"Lesson vocabulary has fewer than {MIN_VOCABULARY_ITEMS} items: {slug}"
        )

    seen_words: set[str] = set()
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            issues.append(f"Vocabulary item {index} must be a mapping: {slug}")
            continue

        word = item.get("word")
        if not has_text(word):
            issues.append(f"Vocabulary item {index} missing word: {slug}")
        else:
            normalized_word = normalized_text(word)
            if normalized_word in seen_words:
                issues.append(f"Duplicate vocabulary word in lesson: {slug}")
            seen_words.add(normalized_word)

        for field in ("meaning_id", "usage_note"):
            if not has_text(item.get(field)):
                issues.append(f"Vocabulary item {index} missing {field}: {slug}")

    return issues


def validate_response_prompts(slug: str, path: Path) -> list[str]:
    if not path.exists():
        return []

    issues: list[str] = []
    prompts = read_yaml(path).get("prompts")
    if not isinstance(prompts, list):
        return [f"Response prompts file must contain a prompts list: {slug}"]
    if len(prompts) < MIN_RESPONSE_PROMPTS:
        issues.append(
            f"Lesson response practice has fewer than {MIN_RESPONSE_PROMPTS} prompts: {slug}"
        )

    seen_prompts: set[str] = set()
    seen_targets: set[str] = set()
    for index, item in enumerate(prompts, start=1):
        if not isinstance(item, dict):
            issues.append(f"Response prompt {index} must be a mapping: {slug}")
            continue

        prompt_text = item.get("prompt") or item.get("instruction_id") or item.get("prompt_en")
        if not has_text(prompt_text):
            issues.append(f"Response prompt {index} missing prompt text: {slug}")
        else:
            normalized_prompt = normalized_text(prompt_text)
            if normalized_prompt in seen_prompts:
                issues.append(f"Duplicate response prompt in lesson: {slug}")
            seen_prompts.add(normalized_prompt)

        target_response = item.get("target_response")
        if target_response is not None:
            if not has_text(target_response):
                issues.append(f"Response prompt {index} missing target response: {slug}")
                continue

            accepted = item.get("acceptable_responses", item.get("acceptable_variations"))
            if not isinstance(accepted, list) or not any(has_text(option) for option in accepted):
                issues.append(f"Response prompt {index} missing acceptable responses: {slug}")
            elif normalized_text(target_response) not in {
                normalized_text(option) for option in accepted
            }:
                issues.append(
                    f"Response prompt {index} target response not listed as acceptable: {slug}"
                )

            normalized_target = normalized_text(target_response)
            if normalized_target in seen_targets:
                issues.append(f"Duplicate response target in lesson: {slug}")
            seen_targets.add(normalized_target)
            continue

        examples = item.get("expected_response_examples")
        if not isinstance(examples, list) or not any(has_text(option) for option in examples):
            issues.append(f"Response prompt {index} missing response examples: {slug}")
            continue

        normalized_example = normalized_text(next(option for option in examples if has_text(option)))
        if normalized_example in seen_targets:
            issues.append(f"Duplicate response target in lesson: {slug}")
        seen_targets.add(normalized_example)

    return issues


def validate_quiz(slug: str, path: Path) -> list[str]:
    if not path.exists():
        return []

    issues: list[str] = []
    questions = read_yaml(path).get("questions")
    if not isinstance(questions, list):
        return [f"Quiz file must contain a questions list: {slug}"]
    if len(questions) < MIN_QUIZ_QUESTIONS:
        issues.append(f"Lesson quiz has fewer than {MIN_QUIZ_QUESTIONS} questions: {slug}")

    seen_prompts: set[str] = set()
    for index, item in enumerate(questions, start=1):
        if not isinstance(item, dict):
            issues.append(f"Quiz question {index} must be a mapping: {slug}")
            continue

        prompt = item.get("prompt")
        if not has_text(prompt):
            issues.append(f"Quiz question {index} missing prompt: {slug}")
        else:
            normalized_prompt = normalized_text(prompt)
            if normalized_prompt in seen_prompts:
                issues.append(f"Duplicate quiz question in lesson: {slug}")
            seen_prompts.add(normalized_prompt)

        options = item.get("options", item.get("choices"))
        answer = item.get("correct_answer", item.get("answer"))
        if not isinstance(options, list):
            issues.append(f"Quiz question {index} missing options: {slug}")
            continue
        if len(options) < MIN_QUIZ_OPTIONS:
            issues.append(
                f"Quiz question {index} has fewer than {MIN_QUIZ_OPTIONS} options: {slug}"
            )

        normalized_options = [normalized_text(option) for option in options if has_text(option)]
        if len(normalized_options) != len(options):
            issues.append(f"Quiz question {index} has an empty option: {slug}")
        if len(set(normalized_options)) != len(normalized_options):
            issues.append(f"Quiz question {index} has duplicate options: {slug}")
        if not has_text(answer):
            issues.append(f"Quiz question {index} missing answer: {slug}")
        elif normalized_text(answer) not in set(normalized_options):
            issues.append(f"Quiz question {index} answer is not in options: {slug}")

    return issues


@lru_cache(maxsize=16)
def load_final_evaluation(
    level_code: str = LEVEL_CODE, *, language: str = "english"
) -> Optional[dict[str, Any]]:
    normalized_language = normalize_language(language)
    normalized_level = level_code.upper()
    path = level_root(language=normalized_language, level_code=normalized_level) / "final_evaluation.yaml"
    if not path.exists():
        return None
    data = read_yaml(path)
    return {
        **data,
        "language": normalized_language,
        "language_code": data.get("language_code") or LANGUAGE_CODES.get(normalized_language, ""),
        "level_code": data.get("level_code") or normalized_level,
        "attempt_level_code": level_test_attempt_code(
            language=normalized_language, level_code=normalized_level
        ),
        "sections": data.get("sections", []),
        "critical_skills": data.get("critical_skills", []),
    }


def load_a1_final_evaluation() -> dict[str, Any]:
    return load_final_evaluation(LEVEL_CODE)


def get_lesson_or_none(lesson_slug: str) -> Optional[dict[str, Any]]:
    for course in all_authored_courses():
        for unit in course["units"]:
            for lesson in unit["lessons"]:
                if lesson["slug"] == lesson_slug:
                    return {
                        **lesson,
                        "language": course.get("language", "english"),
                        "language_code": course.get("language_code", ""),
                        "access_tier": course.get("access_tier", ""),
                        "unit_slug": unit["slug"],
                        "unit_title": unit["title"],
                        "level_code": course["level_code"],
                        "course_slug": course["course_slug"],
                    }
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
        "language": source.get("language", "english"),
        "language_code": source.get("language_code", LANGUAGE_CODE),
        "level_code": source["level_code"],
        "attempt_level_code": source.get("attempt_level_code", source["level_code"]),
        "title": source["title"],
        "status": source["status"],
        "description": source.get("description", ""),
        "overall_threshold": source["overall_threshold"],
        "lesson_completion_required_percent": source["lesson_completion_required_percent"],
        "critical_skills": source.get("critical_skills", []),
        "sections": source.get("sections", []),
    }


def published_lessons(level_code: Optional[str] = None) -> list[dict[str, Any]]:
    """Published lessons across all levels, or one level when level_code is given."""
    lessons = []
    for course in all_courses():
        if level_code and course["level_code"] != level_code:
            continue
        for unit in course["units"]:
            for lesson in unit["lessons"]:
                if lesson.get("status") == "published":
                    lessons.append(
                        {
                            **lesson,
                            "unit_slug": unit["slug"],
                            "unit_title": unit["title"],
                            "level_code": course["level_code"],
                            "course_slug": course["course_slug"],
                        }
                    )
    return lessons


def validate_curriculum_content() -> list[str]:
    issues: list[str] = []
    seen_slugs: set[str] = set()

    # Content structure and final evaluations are validated for every authored
    # course, including language-scoped level tests.
    for course in all_authored_courses():
        language = str(course.get("language") or "english")
        level_code = course["level_code"]
        is_production_level = language == "english" and level_code == LEVEL_CODE
        level_spec_path = level_root(language=language, level_code=level_code) / "LEVEL_SPEC.md"
        if not level_spec_path.exists():
            issues.append(f"Missing level spec for {language} level: {level_code}")
        else:
            level_spec_content = level_spec_path.read_text(encoding="utf-8")
            for section_heading in REQUIRED_LEVEL_SPEC_SECTIONS:
                if section_heading not in level_spec_content:
                    issues.append(
                        f"Level spec {language} {level_code} missing section: {section_heading}"
                    )

        evaluation = load_final_evaluation(level_code, language=language)
        if evaluation is None:
            issues.append(f"Missing final evaluation file for {language} level: {level_code}")
        else:
            issues.extend(validate_final_evaluation(evaluation, level_code))

        for unit in course["units"]:
            if is_production_level and unit.get("status") != "published":
                issues.append(f"Unit is not published: {unit['slug']}")

            for lesson in unit["lessons"]:
                slug = lesson["slug"]
                if slug in seen_slugs:
                    issues.append(f"Duplicate lesson slug: {slug}")
                seen_slugs.add(slug)

                if is_production_level and lesson.get("status") != "published":
                    issues.append(f"Lesson is not published: {slug}")

                if not lesson.get("sections"):
                    issues.append(f"Lesson has no required sections: {slug}")

                completion_rules = lesson.get("completion_rules", {})
                for rule_key in REQUIRED_COMPLETION_RULES:
                    if rule_key not in completion_rules:
                        issues.append(f"Lesson missing completion rule {rule_key}: {slug}")

                roleplay = lesson.get("roleplay", {})
                if not roleplay.get("opening_line"):
                    issues.append(f"Lesson has no roleplay opening line: {slug}")
                if len(roleplay.get("turns", [])) < 3:
                    issues.append(f"Lesson roleplay has fewer than 3 guided turns: {slug}")
                if len(roleplay.get("target_phrases", [])) < 3:
                    issues.append(f"Lesson roleplay has fewer than 3 target phrases: {slug}")

                rubric = roleplay.get("rubric", {})
                for rubric_key in REQUIRED_ROLEPLAY_RUBRIC_KEYS:
                    if rubric_key not in rubric:
                        issues.append(f"Lesson roleplay missing {rubric_key} rubric: {slug}")
                    elif "minimum_score" not in rubric.get(rubric_key, {}):
                        issues.append(
                            f"Lesson roleplay rubric {rubric_key} missing minimum_score: {slug}"
                        )

                lesson_dir = Path(lesson["content_files"]["lesson"]).parent
                for filename in REQUIRED_LESSON_FILES:
                    file_path = lesson_dir / filename
                    if not file_path.exists():
                        issues.append(f"Missing lesson content file for {slug}: {file_path}")
                issues.extend(validate_lesson_practice_files(slug, lesson_dir))

    issues.extend(validate_production_tracker(load_a1_course()))
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


def validate_final_evaluation(
    evaluation: dict[str, Any], expected_level_code: str = LEVEL_CODE
) -> list[str]:
    issues: list[str] = []

    for field in FINAL_EVALUATION_REQUIRED_FIELDS:
        if field not in evaluation:
            issues.append(f"Final evaluation missing field: {field}")

    if issues:
        return issues

    if evaluation.get("level_code") != expected_level_code:
        issues.append(f"Final evaluation level_code must be {expected_level_code}")

    if evaluation.get("status") != "published":
        issues.append(f"Final evaluation must be published for {expected_level_code}")

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
    load_final_evaluation.cache_clear()
    all_courses.cache_clear()
    all_authored_courses.cache_clear()
    fresh_course = load_a1_course()
    A1_COURSE.clear()
    A1_COURSE.update(fresh_course)
    return A1_COURSE
