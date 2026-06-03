from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.admin_deps import require_admin_api_key
from app.api.deps import get_current_user
from app.data.curriculum import (
    A1_COURSE,
    load_a1_final_evaluation,
    public_course_payload,
    public_final_evaluation_payload,
    public_lesson_payload,
)
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


class LevelTestSubmitPayload(BaseModel):
    lesson_completion_percent: int = Field(ge=0, le=100)
    scores: dict[str, int]
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
    return {
        "data": [
            {
                "code": "A1",
                "name": "Start Simple Conversations",
                "status": "active",
                "language_code": "en",
            },
            {
                "code": "A2",
                "name": "Everyday Conversations",
                "status": "coming_soon",
                "language_code": "en",
            },
        ]
    }


@router.get("/courses")
async def list_courses() -> dict:
    return {"data": [public_course_payload(A1_COURSE)]}


@router.get("/courses/{slug}")
async def get_course(slug: str) -> dict:
    if slug != A1_COURSE["course_slug"]:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"data": public_course_payload(A1_COURSE)}


@router.get("/lessons/{slug}")
async def get_lesson(slug: str) -> dict:
    for unit in A1_COURSE["units"]:
        for lesson in unit["lessons"]:
            if lesson["slug"] == slug:
                return {
                    "data": {
                        **public_lesson_payload(lesson),
                        "unit": unit["title"],
                        "course": A1_COURSE["course_title"],
                    }
                }
    raise HTTPException(status_code=404, detail="Lesson not found")


@router.get("/level-tests/{level_code}")
async def get_level_test(level_code: str) -> dict:
    if level_code.upper() != "A1":
        raise HTTPException(status_code=404, detail="Level test not found")
    return {"data": public_final_evaluation_payload(load_a1_final_evaluation())}


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


@router.post("/lessons/{slug}/progress/start")
async def start_my_lesson_progress(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
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
    try:
        progress = LearningProgressRepository(db).complete_lesson(
            user_id=current_user.id,
            lesson_slug=slug,
            completed_sections=payload.completed_sections,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Lesson not found") from exc

    lesson = get_lesson_or_none(slug)
    return {"data": lesson_progress_payload(progress, lesson)}


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
    _: bool = Depends(require_admin_api_key),
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
    _: bool = Depends(require_admin_api_key),
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
    _: bool = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    try:
        attempt = LevelTestAttemptRepository(db).admin_score_attempt(
            attempt_id=attempt_id,
            reviewed_by=payload.reviewed_by,
            scores=payload.scores,
            lesson_completion_percent=payload.lesson_completion_percent,
            notes=payload.notes,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Level test attempt not found") from exc
    except InvalidLevelTestAttemptStateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return {"data": level_test_attempt_payload(attempt)}


@router.post("/level-tests/{level_code}/attempts")
async def start_level_test_attempt(
    level_code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    try:
        attempt = LevelTestAttemptRepository(db).create_attempt(
            user_id=current_user.id,
            level_code=level_code,
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


@router.post("/level-tests/A1/attempts/preview")
async def preview_a1_level_attempt(payload: dict) -> dict:
    evaluation = load_a1_final_evaluation()
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
