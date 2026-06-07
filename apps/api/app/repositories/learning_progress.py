from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.curriculum import (
    A1_COURSE,
    all_courses,
    get_lesson_or_none,
    published_lessons,
)
from app.db.models import LessonProgressModel, UserOnboardingProfileModel


DEFAULT_COURSE_SLUG = A1_COURSE["course_slug"]
DEFAULT_LEVEL_CODE = A1_COURSE["level_code"]


class LearningProgressRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def save_onboarding(
        self,
        user_id: str,
        primary_goal: str,
        confidence_level: str,
        daily_target_minutes: int,
    ) -> UserOnboardingProfileModel:
        now = datetime.utcnow()
        profile = self.db.get(UserOnboardingProfileModel, user_id)

        if profile is None:
            profile = UserOnboardingProfileModel(
                user_id=user_id,
                primary_goal=primary_goal,
                confidence_level=confidence_level,
                daily_target_minutes=daily_target_minutes,
                recommended_course_slug=DEFAULT_COURSE_SLUG,
                recommended_level_code=DEFAULT_LEVEL_CODE,
                completed=True,
                created_at=now,
                updated_at=now,
            )
            self.db.add(profile)
        else:
            profile.primary_goal = primary_goal
            profile.confidence_level = confidence_level
            profile.daily_target_minutes = daily_target_minutes
            profile.recommended_course_slug = DEFAULT_COURSE_SLUG
            profile.recommended_level_code = DEFAULT_LEVEL_CODE
            profile.completed = True
            profile.updated_at = now

        self.db.commit()
        return profile

    def get_onboarding(self, user_id: str) -> Optional[UserOnboardingProfileModel]:
        return self.db.get(UserOnboardingProfileModel, user_id)

    def start_lesson(self, user_id: str, lesson_slug: str) -> LessonProgressModel:
        lesson = get_lesson_or_none(lesson_slug)
        if lesson is None:
            raise KeyError(lesson_slug)

        now = datetime.utcnow()
        progress = self._get_lesson_progress_model(user_id=user_id, lesson_slug=lesson_slug)

        if progress is None:
            progress = LessonProgressModel(
                user_id=user_id,
                course_slug=lesson.get("course_slug", DEFAULT_COURSE_SLUG),
                lesson_slug=lesson_slug,
                status="in_progress",
                completed_sections=[],
                started_at=now,
                completed_at=None,
                updated_at=now,
            )
            self.db.add(progress)
        elif progress.status != "completed":
            progress.status = "in_progress"
            progress.updated_at = now

        self.db.commit()
        return progress

    def complete_lesson(
        self,
        user_id: str,
        lesson_slug: str,
        completed_sections: Optional[list[str]] = None,
    ) -> LessonProgressModel:
        lesson = get_lesson_or_none(lesson_slug)
        if lesson is None:
            raise KeyError(lesson_slug)

        now = datetime.utcnow()
        progress = self._get_lesson_progress_model(user_id=user_id, lesson_slug=lesson_slug)
        sections = completed_sections if completed_sections is not None else lesson.get("sections", [])

        if progress is None:
            progress = LessonProgressModel(
                user_id=user_id,
                course_slug=lesson.get("course_slug", DEFAULT_COURSE_SLUG),
                lesson_slug=lesson_slug,
                status="completed",
                completed_sections=sections,
                started_at=now,
                completed_at=now,
                updated_at=now,
            )
            self.db.add(progress)
        else:
            progress.status = "completed"
            progress.completed_sections = sections
            progress.completed_at = progress.completed_at or now
            progress.updated_at = now

        self.db.commit()
        return progress

    def get_lesson_progress(
        self,
        user_id: str,
        lesson_slug: str,
    ) -> Optional[LessonProgressModel]:
        return self._get_lesson_progress_model(user_id=user_id, lesson_slug=lesson_slug)

    def summary(self, user_id: str) -> dict:
        onboarding = self.get_onboarding(user_id)
        progress_by_lesson = {
            progress.lesson_slug: progress
            for progress in self.db.execute(
                select(LessonProgressModel).where(
                    LessonProgressModel.user_id == user_id,
                    LessonProgressModel.course_slug == DEFAULT_COURSE_SLUG,
                )
            )
            .scalars()
            .all()
        }
        lessons = published_lessons(DEFAULT_LEVEL_CODE)
        total_lessons = len(lessons)
        completed_lessons = sum(
            1
            for lesson in lessons
            if progress_by_lesson.get(lesson["slug"])
            and progress_by_lesson[lesson["slug"]].status == "completed"
        )
        completion_percent = (
            round((completed_lessons / total_lessons) * 100) if total_lessons else 0
        )
        current_lesson = first_incomplete_lesson(lessons, progress_by_lesson) or (
            lessons[-1] if lessons else None
        )

        return {
            "onboarding": onboarding,
            "course": {
                "slug": DEFAULT_COURSE_SLUG,
                "title": A1_COURSE["course_title"],
                "level_code": DEFAULT_LEVEL_CODE,
                "completion_percent": completion_percent,
                "completed_lessons": completed_lessons,
                "total_lessons": total_lessons,
            },
            "current_mission": lesson_summary(current_lesson, progress_by_lesson)
            if current_lesson
            else None,
            "lessons": [lesson_summary(lesson, progress_by_lesson) for lesson in lessons],
        }

    def completed_lesson_slugs(self, user_id: str) -> set[str]:
        return {
            progress.lesson_slug
            for progress in self.db.execute(
                select(LessonProgressModel).where(
                    LessonProgressModel.user_id == user_id,
                    LessonProgressModel.status == "completed",
                )
            )
            .scalars()
            .all()
        }

    def is_level_complete(self, user_id: str, level_code: str) -> bool:
        """True if every published lesson in the level is completed by the user."""
        slugs = [lesson["slug"] for lesson in published_lessons(level_code)]
        if not slugs:
            return False
        completed = self.completed_lesson_slugs(user_id)
        return all(s in completed for s in slugs)

    def level_unlock_map(self, user_id: str) -> dict[str, bool]:
        """Per-level unlock state. A level is unlocked if it is the first level,
        or every published lesson in the previous level is completed."""
        completed = self.completed_lesson_slugs(user_id)
        unlocked: dict[str, bool] = {}
        prev_complete = True  # first level is always unlocked
        for course in all_courses():
            unlocked[course["level_code"]] = prev_complete
            slugs = [
                lesson["slug"]
                for unit in course["units"]
                for lesson in unit["lessons"]
                if lesson.get("status") == "published"
            ]
            prev_complete = bool(slugs) and all(s in completed for s in slugs)
        return unlocked

    def _get_lesson_progress_model(
        self,
        user_id: str,
        lesson_slug: str,
    ) -> Optional[LessonProgressModel]:
        return self.db.execute(
            select(LessonProgressModel).where(
                LessonProgressModel.user_id == user_id,
                LessonProgressModel.lesson_slug == lesson_slug,
            )
        ).scalar_one_or_none()

def first_incomplete_lesson(
    lessons: list[dict],
    progress_by_lesson: dict[str, LessonProgressModel],
) -> Optional[dict]:
    for lesson in lessons:
        progress = progress_by_lesson.get(lesson["slug"])
        if progress is None or progress.status != "completed":
            return lesson
    return None


def lesson_summary(
    lesson: dict,
    progress_by_lesson: dict[str, LessonProgressModel],
) -> dict:
    progress = progress_by_lesson.get(lesson["slug"])
    total_sections = len(lesson.get("sections", []))
    completed_sections = progress.completed_sections if progress else []

    return {
        "slug": lesson["slug"],
        "title": lesson["title"],
        "unit_title": lesson["unit_title"],
        "conversation_goal": lesson["conversation_goal"],
        "estimated_minutes": lesson["estimated_minutes"],
        "status": lesson["status"],
        "progress_status": progress.status if progress else "not_started",
        "completed_sections": completed_sections,
        "total_sections": total_sections,
        "updated_at": progress.updated_at.isoformat() if progress else None,
    }
