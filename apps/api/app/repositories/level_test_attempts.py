from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.curriculum import load_final_evaluation, public_final_evaluation_payload
from app.db.models import LevelTestAttemptModel
from app.domain.evaluation import evaluate_level_attempt


class InvalidLevelTestAttemptStateError(Exception):
    pass


class LevelTestAttemptRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_attempt(self, user_id: str, level_code: str) -> LevelTestAttemptModel:
        evaluation = evaluation_for_level(level_code)
        now = datetime.utcnow()
        attempt = LevelTestAttemptModel(
            id=f"lta-{uuid4().hex[:16]}",
            user_id=user_id,
            level_code=evaluation["level_code"],
            status="in_progress",
            lesson_completion_percent=None,
            scores_json={},
            responses_json={},
            evaluation_snapshot_json=public_final_evaluation_payload(evaluation),
            overall_score=None,
            passed=None,
            missing_requirements_json=[],
            weak_skills_json=[],
            started_at=now,
            submitted_at=None,
            reviewed_at=None,
            reviewed_by=None,
            admin_notes=None,
            updated_at=now,
        )
        self.db.add(attempt)
        self.db.commit()
        return attempt

    def submit_attempt(
        self,
        *,
        user_id: str,
        attempt_id: str,
        lesson_completion_percent: int,
        scores: dict[str, int],
        responses: Optional[dict[str, Any]] = None,
    ) -> LevelTestAttemptModel:
        attempt = self.get_attempt(user_id=user_id, attempt_id=attempt_id)
        if attempt.status == "submitted":
            raise InvalidLevelTestAttemptStateError("Level test attempt has already been submitted")

        sanitized_scores = sanitize_scores(scores, attempt.evaluation_snapshot_json)
        result = score_attempt(
            evaluation=attempt.evaluation_snapshot_json,
            scores=sanitized_scores,
            lesson_completion_percent=lesson_completion_percent,
        )
        now = datetime.utcnow()
        attempt.status = "submitted"
        attempt.lesson_completion_percent = lesson_completion_percent
        attempt.scores_json = sanitized_scores
        attempt.responses_json = responses or {}
        attempt.overall_score = result.overall_score
        attempt.passed = result.passed
        attempt.missing_requirements_json = result.missing_requirements
        attempt.weak_skills_json = result.weak_skills
        attempt.submitted_at = now
        attempt.updated_at = now

        self.db.commit()
        return attempt

    def admin_score_attempt(
        self,
        *,
        attempt_id: str,
        reviewed_by: str,
        scores: dict[str, int],
        lesson_completion_percent: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> LevelTestAttemptModel:
        attempt = self.get_attempt_for_admin(attempt_id)
        if attempt.status == "in_progress":
            raise InvalidLevelTestAttemptStateError("Level test attempt must be submitted first")

        completion_percent = (
            lesson_completion_percent
            if lesson_completion_percent is not None
            else attempt.lesson_completion_percent
        )
        if completion_percent is None:
            raise InvalidLevelTestAttemptStateError("Lesson completion percent is required")

        sanitized_scores = sanitize_scores(scores, attempt.evaluation_snapshot_json)
        result = score_attempt(
            evaluation=attempt.evaluation_snapshot_json,
            scores=sanitized_scores,
            lesson_completion_percent=completion_percent,
        )
        now = datetime.utcnow()
        attempt.status = "reviewed"
        attempt.lesson_completion_percent = completion_percent
        attempt.scores_json = sanitized_scores
        attempt.overall_score = result.overall_score
        attempt.passed = result.passed
        attempt.missing_requirements_json = result.missing_requirements
        attempt.weak_skills_json = result.weak_skills
        attempt.reviewed_at = now
        attempt.reviewed_by = reviewed_by.strip() or "admin"
        attempt.admin_notes = (notes or "").strip() or None
        attempt.updated_at = now

        self.db.commit()
        return attempt

    def get_attempt(self, user_id: str, attempt_id: str) -> LevelTestAttemptModel:
        attempt = self.db.get(LevelTestAttemptModel, attempt_id)
        if attempt is None or attempt.user_id != user_id:
            raise KeyError(attempt_id)
        return attempt

    def get_attempt_for_admin(self, attempt_id: str) -> LevelTestAttemptModel:
        attempt = self.db.get(LevelTestAttemptModel, attempt_id)
        if attempt is None:
            raise KeyError(attempt_id)
        return attempt

    def latest_attempts(
        self,
        *,
        user_id: str,
        level_code: Optional[str] = None,
        limit: int = 5,
    ) -> list[LevelTestAttemptModel]:
        query = select(LevelTestAttemptModel).where(LevelTestAttemptModel.user_id == user_id)
        if level_code:
            query = query.where(LevelTestAttemptModel.level_code == level_code.upper())

        return (
            self.db.execute(query.order_by(LevelTestAttemptModel.updated_at.desc()).limit(limit))
            .scalars()
            .all()
        )

    def list_attempts_for_admin(
        self,
        *,
        level_code: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> list[LevelTestAttemptModel]:
        query = select(LevelTestAttemptModel)
        if level_code:
            query = query.where(LevelTestAttemptModel.level_code == level_code.upper())
        if status:
            query = query.where(LevelTestAttemptModel.status == status)

        return (
            self.db.execute(query.order_by(LevelTestAttemptModel.updated_at.desc()).limit(limit))
            .scalars()
            .all()
        )


def evaluation_for_level(level_code: str) -> dict[str, Any]:
    evaluation = load_final_evaluation(level_code.upper())
    if evaluation is None:
        raise KeyError(level_code)
    if evaluation.get("status") != "published":
        raise InvalidLevelTestAttemptStateError("Level test is not published")
    return evaluation


def score_attempt(
    *,
    evaluation: dict[str, Any],
    scores: dict[str, int],
    lesson_completion_percent: int,
):
    skill_minimums = {
        section["key"]: int(section["minimum_score"])
        for section in evaluation.get("sections", [])
    }
    skill_weights = {
        section["key"]: int(section["weight"]) / 100
        for section in evaluation.get("sections", [])
    }
    return evaluate_level_attempt(
        scores,
        lesson_completion_percent,
        overall_threshold=int(evaluation["overall_threshold"]),
        skill_minimums=skill_minimums,
        skill_weights=skill_weights,
        critical_skills=evaluation.get("critical_skills", []),
        lesson_completion_required_percent=int(evaluation["lesson_completion_required_percent"]),
    )


def sanitize_scores(scores: dict[str, int], evaluation: dict[str, Any]) -> dict[str, int]:
    section_keys = [section["key"] for section in evaluation.get("sections", [])]
    return {
        key: max(0, min(100, int(scores.get(key, 0))))
        for key in section_keys
    }


def level_test_attempt_payload(attempt: LevelTestAttemptModel) -> dict[str, Any]:
    return {
        "id": attempt.id,
        "user_id": attempt.user_id,
        "level_code": attempt.level_code,
        "status": attempt.status,
        "lesson_completion_percent": attempt.lesson_completion_percent,
        "scores": attempt.scores_json,
        "responses": attempt.responses_json,
        "evaluation_snapshot": attempt.evaluation_snapshot_json,
        "overall_score": attempt.overall_score,
        "passed": attempt.passed,
        "missing_requirements": attempt.missing_requirements_json,
        "weak_skills": attempt.weak_skills_json,
        "started_at": attempt.started_at.isoformat(),
        "submitted_at": attempt.submitted_at.isoformat() if attempt.submitted_at else None,
        "reviewed_at": attempt.reviewed_at.isoformat() if attempt.reviewed_at else None,
        "reviewed_by": attempt.reviewed_by,
        "admin_notes": attempt.admin_notes,
        "updated_at": attempt.updated_at.isoformat(),
    }
