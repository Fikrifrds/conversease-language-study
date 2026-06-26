from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.admin_deps import AdminActor, require_admin_api_key
from app.api.deps import get_current_user
from app.data.content_readiness import lesson_audio_asset
from app.data.curriculum import (
    all_authored_courses,
    all_courses,
    course_requires_pro,
    get_course_by_slug,
    lesson_requires_pro,
    load_final_evaluation,
    public_course_payload,
    public_final_evaluation_payload,
    public_lesson_payload,
    track_requires_admin,
)
from app.repositories.billing import BillingRepository
from app.services.lesson_content import build_lesson_body_or_none
from app.db.models import LessonProgressModel, UserOnboardingProfileModel
from app.db.session import get_db
from app.domain.users import User
from app.repositories.level_test_attempts import (
    InvalidLevelTestAttemptStateError,
    LevelTestAttemptRepository,
    level_test_attempt_payload,
    sanitize_scores,
    score_attempt,
)
from app.repositories.learning_progress import LearningProgressRepository, get_lesson_or_none
from app.services.learning_email import LearningEmailService

router = APIRouter()


class OnboardingPayload(BaseModel):
    primary_goal: str = Field(min_length=2, max_length=120)
    confidence_level: str = Field(min_length=2, max_length=160)
    daily_target_minutes: int = Field(ge=5, le=120)


class OnboardingResponse(BaseModel):
    primary_goal: str
    confidence_level: str
    daily_target_minutes: int
    recommended_course_slug: str
    recommended_level_code: str
    completed: bool
    updated_at: str


class LessonProgressPayload(BaseModel):
    completed_sections: Optional[list[str]] = None


class ReviewContentPayload(BaseModel):
    slugs: list[str] = Field(default_factory=list, max_length=200)


class LevelTestSubmitPayload(BaseModel):
    lesson_completion_percent: int = Field(ge=0, le=100)
    scores: dict[str, int]
    responses: Optional[dict] = None


class LevelTestDraftPayload(BaseModel):
    lesson_completion_percent: Optional[int] = Field(default=None, ge=0, le=100)
    scores: Optional[dict[str, int]] = None
    responses: Optional[dict] = None


class AdminLevelTestScorePayload(BaseModel):
    reviewed_by: str = Field(default="admin", min_length=2, max_length=160)
    lesson_completion_percent: Optional[int] = Field(default=None, ge=0, le=100)
    scores: dict[str, int]
    notes: Optional[str] = Field(default=None, max_length=1000)


def onboarding_payload(model: UserOnboardingProfileModel) -> OnboardingResponse:
    return OnboardingResponse(
        primary_goal=model.primary_goal,
        confidence_level=model.confidence_level,
        daily_target_minutes=model.daily_target_minutes,
        recommended_course_slug=model.recommended_course_slug,
        recommended_level_code=model.recommended_level_code,
        completed=model.completed,
        updated_at=model.updated_at.isoformat(),
    )


def lesson_progress_payload(model: LessonProgressModel, lesson: dict) -> dict:
    return {
        "lesson_slug": model.lesson_slug,
        "course_slug": model.course_slug,
        "title": lesson["title"],
        "status": model.status,
        "completed_sections": model.completed_sections,
        "total_sections": len(lesson.get("sections", [])),
        "started_at": model.started_at.isoformat(),
        "completed_at": model.completed_at.isoformat() if model.completed_at else None,
        "updated_at": model.updated_at.isoformat(),
    }


@router.get("/levels")
async def list_levels() -> dict:
    entries = []
    for course in all_courses():
        evaluation = load_final_evaluation(course["level_code"])
        evaluation_status = (evaluation or {}).get("status", "planned")
        entries.append(
            {
                "code": course["level_code"],
                "name": course["course_title"],
                "status": "active" if evaluation_status == "published" else "beta",
                "language_code": course["language_code"],
            }
        )

    return {
        "data": entries
    }


def course_access_payload(course: dict, *, unlocked: bool, is_pro: bool, is_admin: bool) -> dict:
    needs_pro = course_requires_pro(course)
    return {
        **public_course_payload(course),
        "unlocked": unlocked,
        "requires_pro": needs_pro,
        # Fully usable when the prerequisite level is done AND the user has the
        # right tier (A1 free, A2+ require Pro). Admins can access everything.
        "accessible": is_admin or (unlocked and (not needs_pro or is_pro)),
    }


@router.get("/courses")
async def list_courses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    is_admin = current_user.is_admin
    is_pro = BillingRepository(db).is_pro(current_user.id)
    unlock = LearningProgressRepository(db).level_unlock_map(current_user.id, is_admin=is_admin)
    return {
        "data": [
            course_access_payload(
                course,
                unlocked=unlock.get(course["level_code"], False),
                is_pro=is_pro,
                is_admin=is_admin,
            )
            for course in all_authored_courses()
        ]
    }


@router.get("/courses/{slug}")
async def get_course(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    course = get_course_by_slug(slug)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    is_admin = current_user.is_admin
    is_pro = BillingRepository(db).is_pro(current_user.id)
    unlock = LearningProgressRepository(db).level_unlock_map(current_user.id, is_admin=is_admin)
    return {
        "data": course_access_payload(
            course,
            unlocked=unlock.get(course["level_code"], False),
            is_pro=is_pro,
            is_admin=is_admin,
        )
    }


@router.get("/courses/{slug}/progress")
async def get_course_progress(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    if get_course_by_slug(slug) is None:
        raise HTTPException(status_code=404, detail="Course not found")
    summary = LearningProgressRepository(db).summary(current_user.id, course_slug=slug)
    onboarding = summary["onboarding"]
    return {
        "data": {
            "onboarding": onboarding_payload(onboarding) if onboarding else None,
            "course": summary["course"],
            "current_mission": summary["current_mission"],
            "lessons": summary["lessons"],
        }
    }


@router.get("/lessons/{slug}")
async def get_lesson(slug: str) -> dict:
    lesson = get_lesson_or_none(slug)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {
        "data": {
            **public_lesson_payload(lesson),
            "unit": lesson["unit_title"],
            "course": lesson.get("course_slug", ""),
            "level_code": lesson.get("level_code", ""),
        }
    }


@router.get("/lessons/{slug}/full")
async def get_lesson_full(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Full, render-ready lesson body, gated behind a Pro subscription.

    The paywalled sections (dialogue, phrases, vocabulary, roleplay prompts,
    quiz, reading/writing support, etc.) are served only to Pro or admin users.
    Free users get a 403 and never receive the content, so the paywall is
    enforced server-side rather than only hidden in the browser.
    """
    lesson = get_lesson_or_none(slug)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if not current_user.is_admin:
        if track_requires_admin(str(lesson.get("language") or "")):
            raise HTTPException(status_code=403, detail="track_not_available")
        if not BillingRepository(db).is_pro(current_user.id):
            raise HTTPException(status_code=403, detail="lesson_requires_pro")

    body = build_lesson_body_or_none(slug)
    if body is None:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return {"data": body}


# Fields the Review feature needs client-side. Kept narrow so only what Review
# renders is exposed, and gated like the full lesson body.
_REVIEW_CONTENT_FIELDS = (
    "dialogue",
    "translation",
    "phrases",
    "patterns",
    "prompts",
    "writingSupport",
)


@router.post("/lessons/review-content")
async def get_review_content(
    payload: ReviewContentPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Review-only lesson fields for the given slugs, gated behind Pro.

    Returns a slug -> {fields} map so the Review feature can render its prompts
    without bundling lesson content into the browser. Free users (non-Pro,
    non-admin) get an empty map, so no content leaves the server for them.
    """
    if not current_user.is_admin and not BillingRepository(db).is_pro(current_user.id):
        return {"data": {}}

    content: dict[str, dict] = {}
    for slug in dict.fromkeys(payload.slugs):
        lesson = get_lesson_or_none(slug)
        if lesson is None:
            continue
        # Skip coming-soon tracks for non-admins, even if they are Pro.
        if not current_user.is_admin and track_requires_admin(str(lesson.get("language") or "")):
            continue
        body = build_lesson_body_or_none(slug)
        if body is None:
            continue
        content[slug] = {field: body[field] for field in _REVIEW_CONTENT_FIELDS}

    return {"data": content}


@router.get("/lessons/{slug}/audio")
async def get_lesson_audio(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    lesson = get_lesson_or_none(slug)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    ensure_lesson_access(db, current_user, lesson)

    lesson_dir = Path(lesson["content_files"]["lesson"]).parent
    return {"data": lesson_audio_asset(lesson_dir)}


def level_test_payload_or_404(*, language: str, level_code: str) -> dict:
    evaluation = load_final_evaluation(level_code.upper(), language=language)
    if evaluation is None:
        raise HTTPException(status_code=404, detail="Level test not found")
    return {"data": public_final_evaluation_payload(evaluation)}


def level_test_attempt_code_or_404(*, language: str, level_code: str) -> str:
    evaluation = load_final_evaluation(level_code.upper(), language=language)
    if evaluation is None:
        raise HTTPException(status_code=404, detail="Level test not found")
    return str(evaluation["attempt_level_code"])


@router.get("/level-tests/{level_code}")
async def get_level_test(level_code: str) -> dict:
    return level_test_payload_or_404(language="english", level_code=level_code)


@router.get("/level-tests/{language}/{level_code}")
async def get_language_level_test(language: str, level_code: str) -> dict:
    return level_test_payload_or_404(language=language, level_code=level_code)


@router.get("/me/onboarding")
async def get_my_onboarding(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    profile = LearningProgressRepository(db).get_onboarding(current_user.id)
    return {"data": onboarding_payload(profile) if profile else None}


@router.put("/me/onboarding")
async def save_my_onboarding(
    payload: OnboardingPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    profile = LearningProgressRepository(db).save_onboarding(
        user_id=current_user.id,
        primary_goal=payload.primary_goal,
        confidence_level=payload.confidence_level,
        daily_target_minutes=payload.daily_target_minutes,
    )
    return {"data": onboarding_payload(profile)}


@router.get("/me/learning-progress")
async def get_my_learning_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    summary = LearningProgressRepository(db).summary(current_user.id)
    onboarding = summary["onboarding"]
    return {
        "data": {
            "onboarding": onboarding_payload(onboarding) if onboarding else None,
            "course": summary["course"],
            "current_mission": summary["current_mission"],
            "lessons": summary["lessons"],
        }
    }


@router.get("/lessons/{slug}/progress")
async def get_my_lesson_progress(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    lesson = get_lesson_or_none(slug)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")

    progress = LearningProgressRepository(db).get_lesson_progress(
        user_id=current_user.id,
        lesson_slug=slug,
    )
    return {"data": lesson_progress_payload(progress, lesson) if progress else None}


def ensure_lesson_access(db: Session, user: User, lesson: Optional[dict]) -> None:
    """Block coming-soon tracks and Pro-tier lessons for regular users (A1 is
    free). Admins bypass both gates so they can QA every track and level."""
    if user.is_admin:
        return
    if track_requires_admin(str((lesson or {}).get("language") or "")):
        raise HTTPException(status_code=403, detail="track_not_available")
    level_code = (lesson or {}).get("level_code", "")
    if level_code and lesson_requires_pro(lesson) and not BillingRepository(db).is_pro(user.id):
        raise HTTPException(
            status_code=403,
            detail="Pro subscription required for this level",
        )


@router.post("/lessons/{slug}/progress/start")
async def start_my_lesson_progress(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    ensure_lesson_access(db, current_user, get_lesson_or_none(slug))
    try:
        progress = LearningProgressRepository(db).start_lesson(
            user_id=current_user.id,
            lesson_slug=slug,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Lesson not found") from exc

    lesson = get_lesson_or_none(slug)
    return {"data": lesson_progress_payload(progress, lesson)}


@router.post("/lessons/{slug}/progress/complete")
async def complete_my_lesson_progress(
    slug: str,
    payload: LessonProgressPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    ensure_lesson_access(db, current_user, get_lesson_or_none(slug))
    repository = LearningProgressRepository(db)
    try:
        progress = repository.complete_lesson(
            user_id=current_user.id,
            lesson_slug=slug,
            completed_sections=payload.completed_sections,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Lesson not found") from exc

    lesson = get_lesson_or_none(slug)
    await maybe_send_level_completed_email(
        repository, current_user, level_code=(lesson or {}).get("level_code")
    )
    return {"data": lesson_progress_payload(progress, lesson)}


async def maybe_send_level_completed_email(
    repository: LearningProgressRepository,
    user: User,
    *,
    level_code: Optional[str],
) -> None:
    """Send a level-completed email when the level just became 100% complete.

    The email service dedupes per user+level (idempotency_key), so re-completing
    a lesson in an already-finished level will not re-send. Email failures must
    never break lesson completion.
    """
    if not level_code or not repository.is_level_complete(user.id, level_code):
        return
    courses = all_courses()
    levels = [course["level_code"] for course in courses]
    try:
        index = levels.index(level_code)
    except ValueError:
        return
    completed_course = courses[index]
    next_course = courses[index + 1] if index + 1 < len(courses) else None
    try:
        await LearningEmailService().send_level_completed_email(
            user,
            completed_level=level_code,
            completed_level_title=completed_course["course_title"],
            next_level=next_course["level_code"] if next_course else None,
            next_level_title=next_course["course_title"] if next_course else None,
        )
    except Exception:  # never break lesson completion on email failure
        pass


@router.get("/me/level-test-attempts")
async def list_my_level_test_attempts(
    level_code: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    attempts = LevelTestAttemptRepository(db).latest_attempts(
        user_id=current_user.id,
        level_code=level_code,
    )
    return {"data": [level_test_attempt_payload(attempt) for attempt in attempts]}


@router.get("/admin/level-test-attempts")
async def list_admin_level_test_attempts(
    level_code: Optional[str] = Query(default="A1", max_length=16),
    status: Optional[str] = Query(default=None, max_length=32),
    limit: int = Query(default=50, ge=1, le=100),
    _: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    attempts = LevelTestAttemptRepository(db).list_attempts_for_admin(
        level_code=level_code,
        status=status,
        limit=limit,
    )
    return {"data": [level_test_attempt_payload(attempt) for attempt in attempts]}


@router.get("/admin/level-test-attempts/{attempt_id}")
async def get_admin_level_test_attempt(
    attempt_id: str,
    _: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    try:
        attempt = LevelTestAttemptRepository(db).get_attempt_for_admin(attempt_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Level test attempt not found") from exc

    return {"data": level_test_attempt_payload(attempt)}


@router.post("/admin/level-test-attempts/{attempt_id}/score")
async def score_admin_level_test_attempt(
    attempt_id: str,
    payload: AdminLevelTestScorePayload,
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    try:
        attempt = LevelTestAttemptRepository(db).admin_score_attempt(
            attempt_id=attempt_id,
            reviewed_by=admin_display_name(payload.reviewed_by, admin),
            scores=payload.scores,
            lesson_completion_percent=payload.lesson_completion_percent,
            notes=payload.notes,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Level test attempt not found") from exc
    except InvalidLevelTestAttemptStateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return {"data": level_test_attempt_payload(attempt)}


def admin_display_name(value: Optional[str], admin: AdminActor) -> str:
    clean_value = (value or "").strip()
    if clean_value and clean_value.lower() != "admin":
        return clean_value
    return admin.display_name


@router.post("/level-tests/{level_code}/attempts")
async def start_level_test_attempt(
    level_code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return start_level_test_attempt_for(
        attempt_code=level_test_attempt_code_or_404(language="english", level_code=level_code),
        current_user=current_user,
        db=db,
    )


@router.post("/level-tests/{language}/{level_code}/attempts")
async def start_language_level_test_attempt(
    language: str,
    level_code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    return start_level_test_attempt_for(
        attempt_code=level_test_attempt_code_or_404(language=language, level_code=level_code),
        current_user=current_user,
        db=db,
    )


def start_level_test_attempt_for(
    *, attempt_code: str, current_user: User, db: Session
) -> dict:
    try:
        attempt = LevelTestAttemptRepository(db).create_attempt(
            user_id=current_user.id,
            level_code=attempt_code,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Level test not found") from exc
    except InvalidLevelTestAttemptStateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return {"data": level_test_attempt_payload(attempt)}


@router.post("/level-test-attempts/{attempt_id}/submit")
async def submit_level_test_attempt(
    attempt_id: str,
    payload: LevelTestSubmitPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    try:
        attempt = LevelTestAttemptRepository(db).submit_attempt(
            user_id=current_user.id,
            attempt_id=attempt_id,
            lesson_completion_percent=payload.lesson_completion_percent,
            scores=payload.scores,
            responses=payload.responses,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Level test attempt not found") from exc
    except InvalidLevelTestAttemptStateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return {"data": level_test_attempt_payload(attempt)}


@router.patch("/level-test-attempts/{attempt_id}/draft")
async def save_level_test_attempt_draft(
    attempt_id: str,
    payload: LevelTestDraftPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    try:
        attempt = LevelTestAttemptRepository(db).save_draft_attempt(
            user_id=current_user.id,
            attempt_id=attempt_id,
            lesson_completion_percent=payload.lesson_completion_percent,
            scores=payload.scores,
            responses=payload.responses,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Level test attempt not found") from exc
    except InvalidLevelTestAttemptStateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return {"data": level_test_attempt_payload(attempt)}


@router.get("/level-test-attempts/{attempt_id}/report")
async def get_level_test_attempt_report(
    attempt_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    try:
        attempt = LevelTestAttemptRepository(db).get_attempt(
            user_id=current_user.id,
            attempt_id=attempt_id,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Level test attempt not found") from exc

    return {"data": level_test_attempt_payload(attempt)}


@router.post("/level-tests/{level_code}/attempts/preview")
async def preview_level_attempt(level_code: str, payload: dict) -> dict:
    return preview_level_attempt_for(language="english", level_code=level_code, payload=payload)


@router.post("/level-tests/{language}/{level_code}/attempts/preview")
async def preview_language_level_attempt(language: str, level_code: str, payload: dict) -> dict:
    return preview_level_attempt_for(language=language, level_code=level_code, payload=payload)


def preview_level_attempt_for(*, language: str, level_code: str, payload: dict) -> dict:
    evaluation = load_final_evaluation(level_code.upper(), language=language)
    if evaluation is None:
        raise HTTPException(status_code=404, detail="Level test not found")
    scores = sanitize_scores(payload.get("scores", {}), evaluation)
    lesson_completion_percent = int(payload.get("lesson_completion_percent", 0))
    result = score_attempt(
        evaluation=evaluation,
        scores=scores,
        lesson_completion_percent=lesson_completion_percent,
    )
    return {
        "data": {
            "overall_score": result.overall_score,
            "passed": result.passed,
            "missing_requirements": result.missing_requirements,
            "weak_skills": result.weak_skills,
        }
    }
