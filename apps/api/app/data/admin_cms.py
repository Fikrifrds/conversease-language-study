from __future__ import annotations

from pathlib import Path
from re import match
from typing import Any, Optional

import yaml

from app.data.content_readiness import all_content_readiness_summary, content_readiness_summary
from app.data.curriculum import (
    all_authored_courses,
    get_lesson_or_none,
    load_a1_course,
    public_lesson_payload,
    refresh_a1_course,
    repo_root,
    validate_curriculum_content,
)
from app.repositories.content_revisions import content_hash


EMAIL_TEMPLATE_KEY_PATTERN = r"^[a-z0-9_]+$"
PUBLISHED_STATUSES = {"draft", "review", "published", "archived"}


class AdminCmsError(Exception):
    pass


def curriculum_summary() -> dict[str, Any]:
    a1_course = load_a1_course()
    lessons = []
    for unit in a1_course["units"]:
        for lesson in unit["lessons"]:
            lessons.append(
                admin_lesson_payload(
                    lesson,
                    unit_slug=unit["slug"],
                    unit_title=unit["title"],
                )
            )

    all_readiness = all_content_readiness_summary()
    return {
        "course": {
            "slug": a1_course["course_slug"],
            "title": a1_course["course_title"],
            "level_code": a1_course["level_code"],
            "unit_count": len(a1_course["units"]),
            "lesson_count": len(lessons),
        },
        "lessons": lessons,
        "readiness": content_readiness_summary(),
        "readiness_overview": all_readiness["summary"],
        "readiness_levels": all_readiness["levels"],
        "validation_issues": validate_curriculum_content(),
    }


def curriculum_overview(*, language: Optional[str] = None) -> dict[str, Any]:
    readiness = all_content_readiness_summary(language=language)
    return {
        "readiness_overview": readiness["summary"],
        "level_count": readiness["level_count"],
        "languages": curriculum_language_options(),
        "validation_issues": validate_curriculum_content(),
    }


def curriculum_readiness(*, language: Optional[str] = None) -> dict[str, Any]:
    readiness = all_content_readiness_summary(language=language)
    return {
        "readiness_overview": readiness["summary"],
        "level_count": readiness["level_count"],
        "readiness_levels": readiness["levels"],
    }


def curriculum_lesson_index(*, language: Optional[str] = None) -> dict[str, Any]:
    courses = [course for course in all_authored_courses() if not language or course["language"] == language]
    lessons = []
    course_items = []

    for course in courses:
        course_lesson_count = 0
        for unit in course["units"]:
            for lesson in unit["lessons"]:
                course_lesson_count += 1
                lessons.append(
                    admin_lesson_payload(
                        {
                            **lesson,
                            "language": course.get("language", ""),
                            "language_code": course.get("language_code", ""),
                            "level_code": course.get("level_code", ""),
                            "course_slug": course.get("course_slug", ""),
                            "access_tier": course.get("access_tier", ""),
                        },
                        unit_slug=unit["slug"],
                        unit_title=unit["title"],
                    )
                )

        course_items.append(
            {
                "language": course.get("language", ""),
                "language_code": course.get("language_code", ""),
                "level_code": course.get("level_code", ""),
                "course_slug": course.get("course_slug", ""),
                "course_title": course.get("course_title", ""),
                "unit_count": len(course.get("units", [])),
                "lesson_count": course_lesson_count,
            }
        )

    return {"courses": course_items, "lessons": lessons}


def curriculum_language_options() -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for course in all_authored_courses():
        language = str(course.get("language") or "")
        if not language:
            continue
        current = grouped.setdefault(
            language,
            {
                "language": language,
                "language_code": course.get("language_code", ""),
                "level_count": 0,
                "lesson_count": 0,
            },
        )
        current["level_count"] += 1
        current["lesson_count"] += sum(len(unit.get("lessons", [])) for unit in course.get("units", []))

    return sorted(grouped.values(), key=lambda item: item["language"])


def get_admin_lesson(lesson_slug: str) -> dict[str, Any]:
    lesson = get_lesson_or_none(lesson_slug)
    if lesson is None:
        raise AdminCmsError("lesson_not_found")

    return admin_lesson_payload(lesson)


def admin_lesson_payload(
    lesson: dict[str, Any],
    *,
    unit_slug: Optional[str] = None,
    unit_title: Optional[str] = None,
) -> dict[str, Any]:
    payload = {
        **public_lesson_payload(lesson),
        "unit_slug": lesson.get("unit_slug") or unit_slug or "",
        "unit_title": lesson.get("unit_title") or unit_title or "",
        "source": {
            "lesson_yaml": lesson["content_files"]["lesson"].replace("lesson.md", "lesson.yaml"),
            "roleplay_yaml": lesson["content_files"]["conversation_coach_roleplay"],
        },
    }
    return with_content_hash(payload)


def update_lesson_metadata(
    lesson_slug: str,
    *,
    title: Optional[str] = None,
    status: Optional[str] = None,
    estimated_minutes: Optional[int] = None,
    conversation_goal: Optional[str] = None,
    roleplay_opening_line: Optional[str] = None,
    roleplay_learner_goal: Optional[str] = None,
    roleplay_max_turns: Optional[int] = None,
    roleplay_target_phrases: Optional[list[str]] = None,
) -> dict[str, Any]:
    lesson = get_lesson_or_none(lesson_slug)
    if lesson is None:
        raise AdminCmsError("lesson_not_found")

    lesson_dir = Path(lesson["content_files"]["lesson"]).parent
    lesson_yaml_path = lesson_dir / "lesson.yaml"
    roleplay_yaml_path = lesson_dir / "conversation_coach_roleplay.yaml"

    lesson_data = read_yaml_file(lesson_yaml_path)
    roleplay_data = read_yaml_file(roleplay_yaml_path)

    if title is not None:
        lesson_data["title"] = clean_text(title, "title", min_length=2, max_length=120)

    if status is not None:
        if status not in PUBLISHED_STATUSES:
            raise AdminCmsError("invalid_lesson_status")
        lesson_data["status"] = status

    if estimated_minutes is not None:
        if estimated_minutes < 1 or estimated_minutes > 120:
            raise AdminCmsError("invalid_estimated_minutes")
        lesson_data["estimated_minutes"] = estimated_minutes

    if conversation_goal is not None:
        lesson_data["conversation_goal"] = clean_text(
            conversation_goal,
            "conversation_goal",
            min_length=8,
            max_length=260,
        )

    if roleplay_opening_line is not None:
        roleplay_data["opening_line"] = clean_text(
            roleplay_opening_line,
            "roleplay_opening_line",
            min_length=2,
            max_length=260,
        )

    if roleplay_learner_goal is not None:
        roleplay_data["learner_goal"] = clean_text(
            roleplay_learner_goal,
            "roleplay_learner_goal",
            min_length=8,
            max_length=320,
        )

    if roleplay_max_turns is not None:
        if roleplay_max_turns < 1 or roleplay_max_turns > 20:
            raise AdminCmsError("invalid_roleplay_max_turns")
        roleplay_data["max_turns"] = roleplay_max_turns

    if roleplay_target_phrases is not None:
        cleaned_phrases = [
            clean_text(phrase, "target_phrase", min_length=1, max_length=80)
            for phrase in roleplay_target_phrases
            if phrase.strip()
        ]
        if not cleaned_phrases:
            raise AdminCmsError("target_phrases_required")
        roleplay_data["target_phrases"] = cleaned_phrases

    original_lesson_yaml = lesson_yaml_path.read_text(encoding="utf-8")
    original_roleplay_yaml = roleplay_yaml_path.read_text(encoding="utf-8")

    try:
        write_yaml_file(lesson_yaml_path, lesson_data)
        write_yaml_file(roleplay_yaml_path, roleplay_data)
        refresh_a1_course()

        issues = validate_curriculum_content()
        if issues:
            raise AdminCmsError("; ".join(issues))
    except Exception:
        lesson_yaml_path.write_text(original_lesson_yaml, encoding="utf-8")
        roleplay_yaml_path.write_text(original_roleplay_yaml, encoding="utf-8")
        refresh_a1_course()
        raise

    return get_admin_lesson(lesson_slug)


def restore_lesson_from_snapshot(lesson_slug: str, snapshot: dict[str, Any]) -> dict[str, Any]:
    if snapshot.get("slug") != lesson_slug:
        raise AdminCmsError("revision_lesson_mismatch")

    roleplay = snapshot.get("roleplay") or {}
    required_lesson_keys = ["title", "status", "estimated_minutes", "conversation_goal"]
    required_roleplay_keys = ["opening_line", "learner_goal", "max_turns", "target_phrases"]
    if any(snapshot.get(key) is None for key in required_lesson_keys) or any(
        roleplay.get(key) is None for key in required_roleplay_keys
    ):
        raise AdminCmsError("revision_lesson_snapshot_incomplete")

    return update_lesson_metadata(
        lesson_slug,
        title=snapshot.get("title"),
        status=snapshot.get("status"),
        estimated_minutes=snapshot.get("estimated_minutes"),
        conversation_goal=snapshot.get("conversation_goal"),
        roleplay_opening_line=roleplay.get("opening_line"),
        roleplay_learner_goal=roleplay.get("learner_goal"),
        roleplay_max_turns=roleplay.get("max_turns"),
        roleplay_target_phrases=roleplay.get("target_phrases"),
    )


def email_templates_root() -> Path:
    return repo_root() / "content" / "email_templates"


def list_email_template_files() -> list[dict[str, Any]]:
    templates = []
    for path in sorted(email_templates_root().glob("*.md")):
        templates.append(email_template_payload(path))
    return templates


def get_email_template(template_key: str) -> dict[str, Any]:
    return email_template_payload(email_template_path(template_key))


def update_email_template(template_key: str, raw_body: str) -> dict[str, Any]:
    path = email_template_path(template_key)
    clean_body = raw_body.strip() + "\n"

    validate_email_template_markdown(template_key, clean_body)
    path.write_text(clean_body, encoding="utf-8")
    return email_template_payload(path)


def restore_email_template_from_snapshot(template_key: str, snapshot: dict[str, Any]) -> dict[str, Any]:
    if snapshot.get("template_key") != template_key:
        raise AdminCmsError("revision_template_mismatch")

    raw_body = snapshot.get("raw_body")
    if not isinstance(raw_body, str):
        raise AdminCmsError("revision_template_body_missing")

    return update_email_template(template_key, raw_body)


def email_template_path(template_key: str) -> Path:
    if not match(EMAIL_TEMPLATE_KEY_PATTERN, template_key):
        raise AdminCmsError("invalid_template_key")

    path = email_templates_root() / f"{template_key}.md"
    if not path.exists():
        raise AdminCmsError("template_not_found")

    return path


def email_template_payload(path: Path) -> dict[str, Any]:
    raw_body = path.read_text(encoding="utf-8")
    payload = {
        "template_key": path.stem,
        "subject": extract_markdown_value(raw_body, "Subject"),
        "preheader": extract_markdown_value(raw_body, "Preheader"),
        "cta_label": extract_markdown_value(raw_body, "CTA"),
        "raw_body": raw_body,
        "updated_hint": "file-backed",
    }
    return with_content_hash(payload)


def with_content_hash(payload: dict[str, Any]) -> dict[str, Any]:
    return {**payload, "content_hash": content_hash(payload)}


def validate_email_template_markdown(template_key: str, raw_body: str) -> None:
    if not raw_body.startswith(f"# {template_key}"):
        raise AdminCmsError("template_heading_mismatch")

    for label in ["Subject", "Preheader", "CTA"]:
        if not extract_markdown_value(raw_body, label):
            raise AdminCmsError(f"missing_{label.lower()}")

    if "```html" not in raw_body or "```txt" not in raw_body:
        raise AdminCmsError("template_requires_html_and_text_blocks")


def extract_markdown_value(raw_body: str, label: str) -> str:
    prefix = f"{label}:"
    for line in raw_body.splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip()
    return ""


def read_yaml_file(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    if not isinstance(data, dict):
        raise AdminCmsError(f"invalid_yaml:{path.name}")
    return data


def write_yaml_file(path: Path, data: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(data, allow_unicode=False, sort_keys=False, width=100),
        encoding="utf-8",
    )


def clean_text(value: str, field: str, *, min_length: int, max_length: int) -> str:
    cleaned = value.strip()
    if len(cleaned) < min_length:
        raise AdminCmsError(f"{field}_too_short")
    if len(cleaned) > max_length:
        raise AdminCmsError(f"{field}_too_long")
    return cleaned
