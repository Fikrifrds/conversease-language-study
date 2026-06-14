"""Exam service for the real exam system."""
from datetime import datetime, timedelta
from typing import Optional
import hashlib
import secrets

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.db.exam_models import (
    ExamItemModel,
    ExamResultModel,
    ExamSectionModel,
    ExamSessionModel,
    ExamTemplateModel,
    ItemResponseModel,
    ReviewQueueModel,
)

OBJECTIVE_ITEM_TYPES = {"mcq", "fill_blank", "matching"}
REVIEWED_ITEM_TYPES = {"audio_response", "text_response"}


class ExamServiceError(Exception):
    """Base exception for exam service errors."""
    pass


class ExamNotFoundError(ExamServiceError):
    """Exam template not found."""
    pass


class ExamSessionNotFoundError(ExamServiceError):
    """Exam session not found."""
    pass


class ExamAlreadyStartedError(ExamServiceError):
    """Exam already started."""
    pass


class ExamNotStartedError(ExamServiceError):
    """Exam not started yet."""
    pass


class ExamAlreadySubmittedError(ExamServiceError):
    """Exam already submitted."""
    pass


class ExamItemNotFoundError(ExamServiceError):
    """Exam item not found."""
    pass


class ExamAttemptLimitError(ExamServiceError):
    """User has used all allowed attempts for this exam."""
    pass


class ExamCooldownError(ExamServiceError):
    """User must wait out the cooldown before retaking this exam."""

    def __init__(self, message: str, next_available_at: "datetime") -> None:
        super().__init__(message)
        self.next_available_at = next_available_at


DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_COOLDOWN_DAYS = 30
# Sessions that have consumed an attempt (reached a terminal state).
USED_ATTEMPT_STATUSES = ("submitted", "expired")
# Sessions that can still be resumed instead of starting a new attempt.
OPEN_SESSION_STATUSES = ("created", "in_progress")


class ExamExpiredError(ExamServiceError):
    """Exam session expired."""
    pass


class ExamService:
    """Core service for exam lifecycle management."""

    def __init__(self, db: Session):
        self.db = db

    # =========================================================================
    # Exam Template Management
    # =========================================================================

    def create_exam_template(
        self,
        code: str,
        level_code: str,
        title: str,
        description: Optional[str],
        duration_minutes: int,
        passing_score_percent: int,
        created_by: str,
    ) -> ExamTemplateModel:
        """Create a new exam template."""
        now = datetime.utcnow()
        template = ExamTemplateModel(
            id=self._generate_id(),
            code=code,
            level_code=level_code,
            title=title,
            description=description,
            duration_minutes=duration_minutes,
            passing_score_percent=passing_score_percent,
            status="draft",
            created_by=created_by,
            created_at=now,
            updated_at=now,
        )
        self.db.add(template)
        self.db.commit()
        return template

    def get_exam_template(self, template_id: str) -> ExamTemplateModel:
        """Get an exam template by ID."""
        result = self.db.execute(
            select(ExamTemplateModel).where(ExamTemplateModel.id == template_id)
        )
        template = result.scalar_one_or_none()
        if not template:
            raise ExamNotFoundError(f"Exam template {template_id} not found")
        return template

    def get_exam_template_by_code(self, code: str) -> Optional[ExamTemplateModel]:
        """Get an exam template by code."""
        result = self.db.execute(
            select(ExamTemplateModel).where(ExamTemplateModel.code == code)
        )
        return result.scalar_one_or_none()

    def list_exam_templates(
        self,
        level_code: Optional[str] = None,
        status: Optional[str] = None,
    ) -> list[ExamTemplateModel]:
        """List exam templates with optional filters."""
        query = select(ExamTemplateModel)
        if level_code:
            query = query.where(ExamTemplateModel.level_code == level_code)
        if status:
            query = query.where(ExamTemplateModel.status == status)
        query = query.order_by(ExamTemplateModel.created_at.desc())
        result = self.db.execute(query)
        return list(result.scalars().all())

    # =========================================================================
    # Exam Section Management
    # =========================================================================

    def create_exam_section(
        self,
        exam_template_id: str,
        code: str,
        title: str,
        description: Optional[str],
        sequence_order: int,
        duration_minutes: int,
        score_weight_percent: int,
        item_types_allowed: list[str],
    ) -> ExamSectionModel:
        """Create a new exam section."""
        # Verify template exists
        self.get_exam_template(exam_template_id)

        now = datetime.utcnow()
        section = ExamSectionModel(
            id=self._generate_id(),
            exam_template_id=exam_template_id,
            code=code,
            title=title,
            description=description,
            sequence_order=sequence_order,
            duration_minutes=duration_minutes,
            score_weight_percent=score_weight_percent,
            item_types_allowed=item_types_allowed,
            created_at=now,
            updated_at=now,
        )
        self.db.add(section)
        self.db.commit()
        return section

    def get_exam_sections(self, exam_template_id: str) -> list[ExamSectionModel]:
        """Get all sections for an exam template."""
        result = self.db.execute(
            select(ExamSectionModel)
            .where(ExamSectionModel.exam_template_id == exam_template_id)
            .order_by(ExamSectionModel.sequence_order)
        )
        return list(result.scalars().all())

    # =========================================================================
    # Exam Item Management
    # =========================================================================

    def create_exam_item(
        self,
        exam_template_id: str,
        section_id: str,
        item_type: str,
        sequence_order: int,
        prompt_text: str,
        score_points: int = 1,
        stimulus_text: Optional[str] = None,
        stimulus_audio_url: Optional[str] = None,
        stimulus_image_url: Optional[str] = None,
        options_json: Optional[dict] = None,
        correct_answer: Optional[dict] = None,
        rubric_criteria: Optional[dict] = None,
    ) -> ExamItemModel:
        """Create a new exam item (question)."""
        now = datetime.utcnow()
        item = ExamItemModel(
            id=self._generate_id(),
            exam_template_id=exam_template_id,
            section_id=section_id,
            item_type=item_type,
            sequence_order=sequence_order,
            score_points=score_points,
            stimulus_text=stimulus_text,
            stimulus_audio_url=stimulus_audio_url,
            stimulus_image_url=stimulus_image_url,
            prompt_text=prompt_text,
            options_json=options_json,
            correct_answer=correct_answer,
            rubric_criteria=rubric_criteria,
            created_at=now,
            updated_at=now,
        )
        self.db.add(item)
        self.db.commit()
        return item

    def get_exam_items(self, section_id: str) -> list[ExamItemModel]:
        """Get all items for a section."""
        result = self.db.execute(
            select(ExamItemModel)
            .where(ExamItemModel.section_id == section_id)
            .order_by(ExamItemModel.sequence_order)
        )
        return list(result.scalars().all())

    def get_exam_item(self, item_id: str) -> ExamItemModel:
        """Get a single exam item by ID."""
        result = self.db.execute(select(ExamItemModel).where(ExamItemModel.id == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise ExamItemNotFoundError(f"Exam item {item_id} not found")
        return item

    def update_exam_item_audio(
        self,
        *,
        item_id: str,
        stimulus_audio_url: str,
        audio_metadata: dict,
    ) -> ExamItemModel:
        """Persist generated audio data on an exam item."""
        item = self.get_exam_item(item_id)
        item.stimulus_audio_url = stimulus_audio_url
        item.config_json = {
            **(item.config_json or {}),
            "audio_generation": audio_metadata,
        }
        item.updated_at = datetime.utcnow()
        self.db.commit()
        return item

    # =========================================================================
    # Exam Session Lifecycle
    # =========================================================================

    @staticmethod
    def _attempt_policy(template: ExamTemplateModel) -> tuple[int, int]:
        """(max_attempts, cooldown_days) from template metadata, PRD defaults.
        A value <= 0 disables that limit."""
        meta = template.metadata_json if isinstance(template.metadata_json, dict) else {}
        max_attempts = meta.get("max_attempts", DEFAULT_MAX_ATTEMPTS)
        cooldown_days = meta.get("cooldown_days", DEFAULT_COOLDOWN_DAYS)
        return int(max_attempts), int(cooldown_days)

    def _used_attempt_sessions(self, exam_template_id: str, user_id: str) -> list[ExamSessionModel]:
        result = self.db.execute(
            select(ExamSessionModel)
            .where(
                and_(
                    ExamSessionModel.exam_template_id == exam_template_id,
                    ExamSessionModel.user_id == user_id,
                    ExamSessionModel.status.in_(USED_ATTEMPT_STATUSES),
                )
            )
            .order_by(ExamSessionModel.created_at.desc())
        )
        return list(result.scalars().all())

    def _open_session(self, exam_template_id: str, user_id: str) -> Optional[ExamSessionModel]:
        result = self.db.execute(
            select(ExamSessionModel)
            .where(
                and_(
                    ExamSessionModel.exam_template_id == exam_template_id,
                    ExamSessionModel.user_id == user_id,
                    ExamSessionModel.status.in_(OPEN_SESSION_STATUSES),
                )
            )
            .order_by(ExamSessionModel.created_at.desc())
        )
        return result.scalars().first()

    def attempt_status(self, exam_template_id: str, user_id: str) -> dict:
        """Attempt/cooldown standing for a user on an exam, for gating + UI."""
        template = self.get_exam_template(exam_template_id)
        max_attempts, cooldown_days = self._attempt_policy(template)
        used = self._used_attempt_sessions(exam_template_id, user_id)
        attempts_used = len(used)

        next_available_at = None
        if cooldown_days > 0 and used:
            last = used[0]
            last_at = last.submitted_at or last.updated_at
            if last_at is not None:
                candidate = last_at + timedelta(days=cooldown_days)
                if candidate > datetime.utcnow():
                    next_available_at = candidate

        attempts_remaining = (
            max(0, max_attempts - attempts_used) if max_attempts > 0 else None
        )
        return {
            "max_attempts": max_attempts if max_attempts > 0 else None,
            "attempts_used": attempts_used,
            "attempts_remaining": attempts_remaining,
            "in_cooldown": next_available_at is not None,
            "next_available_at": next_available_at,
            "has_open_session": self._open_session(exam_template_id, user_id) is not None,
        }

    def create_exam_session(
        self,
        exam_template_id: str,
        user_id: str,
        access_code: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> ExamSessionModel:
        """Create a new exam session, or resume an open one.

        Enforces per-template attempt limit and cooldown (from template metadata,
        PRD defaults: 3 attempts, 30-day cooldown). An unfinished session is
        resumed instead of consuming a new attempt.
        """
        # Verify template exists and is active
        template = self.get_exam_template(exam_template_id)
        if template.status != "active":
            raise ExamServiceError(f"Exam template {exam_template_id} is not active")

        # Resume an unfinished attempt rather than starting (and charging) a new one.
        open_session = self._open_session(exam_template_id, user_id)
        if open_session is not None:
            return open_session

        max_attempts, cooldown_days = self._attempt_policy(template)
        used = self._used_attempt_sessions(exam_template_id, user_id)

        if max_attempts > 0 and len(used) >= max_attempts:
            raise ExamAttemptLimitError(
                f"You have used all {max_attempts} attempts for this exam."
            )

        if cooldown_days > 0 and used:
            last = used[0]
            last_at = last.submitted_at or last.updated_at
            if last_at is not None:
                next_available = last_at + timedelta(days=cooldown_days)
                if next_available > datetime.utcnow():
                    raise ExamCooldownError(
                        f"You can retake this exam after {next_available.isoformat()}.",
                        next_available_at=next_available,
                    )

        now = datetime.utcnow()
        session = ExamSessionModel(
            id=self._generate_id(),
            exam_template_id=exam_template_id,
            user_id=user_id,
            access_code=access_code or self._generate_access_code(),
            status="created",
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=now,
            updated_at=now,
        )
        self.db.add(session)
        self.db.commit()
        return session

    def get_exam_session(self, session_id: str) -> ExamSessionModel:
        """Get an exam session by ID."""
        result = self.db.execute(
            select(ExamSessionModel).where(ExamSessionModel.id == session_id)
        )
        session = result.scalar_one_or_none()
        if not session:
            raise ExamSessionNotFoundError(f"Exam session {session_id} not found")
        return session

    def start_exam(
        self,
        session_id: str,
        current_section_id: Optional[str] = None,
        current_item_id: Optional[str] = None,
    ) -> ExamSessionModel:
        """Start an exam session."""
        session = self.get_exam_session(session_id)

        if session.status == "in_progress":
            raise ExamAlreadyStartedError(f"Exam session {session_id} already started")
        if session.status == "submitted":
            raise ExamAlreadySubmittedError(f"Exam session {session_id} already submitted")
        if session.status == "expired":
            raise ExamExpiredError(f"Exam session {session_id} has expired")
        
        # Get template for duration
        template = self.get_exam_template(session.exam_template_id)

        now = datetime.utcnow()
        session.status = "in_progress"
        session.started_at = now
        session.expires_at = now + timedelta(minutes=template.duration_minutes + session.time_extension_minutes)
        session.current_section_id = current_section_id
        session.current_item_id = current_item_id
        session.updated_at = now

        self.db.commit()
        return session

    def submit_exam(self, session_id: str) -> ExamSessionModel:
        """Submit an exam session."""
        session = self.get_exam_session(session_id)

        if session.status == "submitted":
            raise ExamAlreadySubmittedError(f"Exam session {session_id} already submitted")
        if session.status != "in_progress":
            raise ExamNotStartedError(f"Exam session {session_id} not in progress")
        
        # Check if expired
        if session.expires_at and datetime.utcnow() > session.expires_at:
            session.status = "expired"
            session.updated_at = datetime.utcnow()
            self.db.commit()
            raise ExamExpiredError(f"Exam session {session_id} has expired")

        session.status = "submitted"
        session.submitted_at = datetime.utcnow()
        session.updated_at = datetime.utcnow()

        self.db.commit()
        return session

    def save_item_response(
        self,
        session_id: str,
        item_id: str,
        section_id: str,
        response_type: str,
        text_response: Optional[str] = None,
        selected_option_ids: Optional[list] = None,
        matched_pairs: Optional[dict] = None,
        file_url: Optional[str] = None,
        audio_duration_seconds: Optional[float] = None,
        recording_attempts: int = 0,
        time_spent_seconds: Optional[int] = None,
    ) -> ItemResponseModel:
        """Save or update a user's response to an exam item."""
        # Check if response already exists
        result = self.db.execute(
            select(ItemResponseModel).where(
                and_(
                    ItemResponseModel.session_id == session_id,
                    ItemResponseModel.item_id == item_id,
                )
            )
        )
        existing = result.scalar_one_or_none()

        now = datetime.utcnow()

        if existing:
            # Update existing response
            existing.response_type = response_type
            existing.text_response = text_response
            existing.selected_option_ids = selected_option_ids
            existing.matched_pairs = matched_pairs
            existing.file_url = file_url
            existing.audio_duration_seconds = audio_duration_seconds
            existing.recording_attempts = recording_attempts
            existing.time_spent_seconds = time_spent_seconds
            existing.submitted_at = now
            existing.updated_at = now
            self.db.commit()
            return existing

        response = ItemResponseModel(
            id=self._generate_id(),
            session_id=session_id,
            item_id=item_id,
            section_id=section_id,
            response_type=response_type,
            text_response=text_response,
            selected_option_ids=selected_option_ids,
            matched_pairs=matched_pairs,
            file_url=file_url,
            audio_duration_seconds=audio_duration_seconds,
            recording_attempts=recording_attempts,
            human_reviewed=False,
            started_at=now,
            submitted_at=now,
            time_spent_seconds=time_spent_seconds,
            created_at=now,
            updated_at=now,
        )
        self.db.add(response)
        self.db.commit()
        return response

    def get_session_responses(self, session_id: str) -> list[ItemResponseModel]:
        """Get all responses for a session."""
        result = self.db.execute(
            select(ItemResponseModel)
            .where(ItemResponseModel.session_id == session_id)
            .order_by(ItemResponseModel.created_at)
        )
        return list(result.scalars().all())

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _generate_id(self) -> str:
        """Generate a unique ID for database records."""
        return hashlib.sha256(secrets.token_bytes(32)).hexdigest()[:64]

    def _generate_access_code(self) -> str:
        """Generate a random access code for exam sessions."""
        return secrets.token_urlsafe(32)[:64]

    # =========================================================================
    # Grading
    # =========================================================================

    @staticmethod
    def _normalize_answer(value: str) -> str:
        return " ".join(value.strip().casefold().split())

    def grade_objective_response(
        self,
        item: ExamItemModel,
        response: ItemResponseModel,
    ) -> tuple[int, bool]:
        """Grade an objective response. Returns (points_earned, is_correct)."""
        answer = item.correct_answer or {}

        if item.item_type == "mcq":
            expected = answer.get("option_id")
            selected = response.selected_option_ids or []
            is_correct = expected is not None and selected == [expected]
            return (item.score_points if is_correct else 0, is_correct)

        if item.item_type == "fill_blank":
            blanks = answer.get("blanks") or []
            variants = answer.get("acceptable_variants") or {}
            submitted = (response.text_response or "").split("\n")
            correct_count = 0
            for index, expected_blank in enumerate(blanks):
                given = self._normalize_answer(submitted[index]) if index < len(submitted) else ""
                accepted = {self._normalize_answer(expected_blank)}
                accepted.update(
                    self._normalize_answer(variant)
                    for variant in variants.get(str(index), [])
                )
                if given and given in accepted:
                    correct_count += 1
            total = len(blanks)
            if total == 0:
                return (0, False)
            points = round(item.score_points * correct_count / total)
            return (points, correct_count == total)

        if item.item_type == "matching":
            expected_pairs = answer.get("pairs") or {}
            submitted_pairs = response.matched_pairs or {}
            total = len(expected_pairs)
            if total == 0:
                return (0, False)
            correct_count = sum(
                1
                for left_id, right_id in expected_pairs.items()
                if submitted_pairs.get(left_id) == right_id
            )
            points = round(item.score_points * correct_count / total)
            return (points, correct_count == total)

        raise ExamServiceError(f"Item type {item.item_type} cannot be auto-graded")

    def finalize_submission(self, session_id: str) -> ExamResultModel:
        """Grade objective responses, queue subjective ones for human review,
        and calculate the exam result for a submitted session."""
        session = self.get_exam_session(session_id)
        if session.status != "submitted":
            raise ExamNotStartedError(f"Exam session {session_id} is not submitted")

        responses = {r.item_id: r for r in self.get_session_responses(session_id)}
        result = self.db.execute(
            select(ExamItemModel)
            .where(ExamItemModel.exam_template_id == session.exam_template_id)
        )
        items = list(result.scalars().all())

        now = datetime.utcnow()
        for item in items:
            response = responses.get(item.id)
            if response is None:
                continue
            if item.item_type in OBJECTIVE_ITEM_TYPES and item.correct_answer:
                points, is_correct = self.grade_objective_response(item, response)
                response.score_points_earned = points
                response.is_correct = is_correct
                response.updated_at = now
            elif item.item_type in REVIEWED_ITEM_TYPES and not response.human_reviewed:
                self._ensure_review_queue_entry(session, item, response, now)

        self.db.commit()
        return self.calculate_score(session_id)

    def _ensure_review_queue_entry(
        self,
        session: ExamSessionModel,
        item: ExamItemModel,
        response: ItemResponseModel,
        now: datetime,
    ) -> None:
        existing = self.db.execute(
            select(ReviewQueueModel).where(ReviewQueueModel.response_id == response.id)
        ).scalar_one_or_none()
        if existing:
            return
        self.db.add(
            ReviewQueueModel(
                id=self._generate_id(),
                response_id=response.id,
                session_id=session.id,
                exam_template_id=session.exam_template_id,
                item_type=item.item_type,
                status="pending",
                created_at=now,
                updated_at=now,
            )
        )

    def list_review_queue(
        self,
        status: str = "pending",
        exam_template_id: Optional[str] = None,
    ) -> list[ReviewQueueModel]:
        """List review queue entries by status."""
        query = select(ReviewQueueModel).where(ReviewQueueModel.status == status)
        if exam_template_id:
            query = query.where(ReviewQueueModel.exam_template_id == exam_template_id)
        query = query.order_by(ReviewQueueModel.priority, ReviewQueueModel.created_at)
        result = self.db.execute(query)
        return list(result.scalars().all())

    def get_review_queue_entry(self, queue_id: str) -> ReviewQueueModel:
        """Get a review queue entry by ID."""
        result = self.db.execute(
            select(ReviewQueueModel).where(ReviewQueueModel.id == queue_id)
        )
        entry = result.scalar_one_or_none()
        if not entry:
            raise ExamServiceError(f"Review queue entry {queue_id} not found")
        return entry

    def apply_review_score(
        self,
        queue_id: str,
        score_points: int,
        reviewed_by: str,
        notes: Optional[str] = None,
    ) -> ExamResultModel:
        """Apply a human review score to a queued response and recalculate the result."""
        entry = self.get_review_queue_entry(queue_id)
        response = self.db.execute(
            select(ItemResponseModel).where(ItemResponseModel.id == entry.response_id)
        ).scalar_one_or_none()
        if not response:
            raise ExamServiceError(f"Response {entry.response_id} not found")
        item = self.get_exam_item(response.item_id)

        if score_points < 0 or score_points > item.score_points:
            raise ExamServiceError(
                f"Score must be between 0 and {item.score_points} for this item"
            )

        now = datetime.utcnow()
        response.score_points_earned = score_points
        response.is_correct = score_points == item.score_points
        response.human_reviewed = True
        response.reviewed_by = reviewed_by
        response.reviewed_at = now
        response.review_notes = notes
        response.updated_at = now

        entry.status = "completed"
        entry.human_score_points = score_points
        entry.human_reviewed_by = reviewed_by
        entry.human_reviewed_at = now
        entry.human_notes = notes
        entry.updated_at = now

        self.db.commit()
        return self.calculate_score(entry.session_id)

    def calculate_score(
        self,
        session_id: str,
    ) -> ExamResultModel:
        """Calculate exam results for a submitted session.

        Section percentages are weighted by ``score_weight_percent``. The result
        stays ``pending_review`` until every queued subjective response has been
        human-reviewed, then it is published.
        """
        session = self.get_exam_session(session_id)
        template = self.get_exam_template(session.exam_template_id)
        responses = self.get_session_responses(session_id)

        # Get all items for this exam
        result = self.db.execute(
            select(ExamItemModel)
            .where(ExamItemModel.exam_template_id == template.id)
        )
        items = {item.id: item for item in result.scalars().all()}

        # Get sections
        sections = self.get_exam_sections(template.id)

        # Calculate scores per section
        section_scores = {}
        total_score = 0
        max_possible = 0
        weighted_percent_sum = 0.0
        weight_sum = 0

        for section in sections:
            section_score = 0
            section_max = 0

            # Get items for this section
            section_items = [item for item in items.values() if item.section_id == section.id]

            for item in section_items:
                section_max += item.score_points

                # Find response for this item
                response = next((r for r in responses if r.item_id == item.id), None)
                if response and response.score_points_earned is not None:
                    section_score += response.score_points_earned

            section_percent = (section_score / section_max * 100) if section_max > 0 else 0
            section_scores[section.code] = {
                "score": section_score,
                "max": section_max,
                "percentage": section_percent,
                "weight_percent": section.score_weight_percent,
            }
            total_score += section_score
            max_possible += section_max
            if section_max > 0:
                weighted_percent_sum += section_percent * section.score_weight_percent
                weight_sum += section.score_weight_percent

        # Weighted final percentage across sections
        score_percent = (weighted_percent_sum / weight_sum) if weight_sum > 0 else 0
        passed = score_percent >= template.passing_score_percent

        # Pending human reviews keep the result unpublished
        pending_reviews = self.db.execute(
            select(ReviewQueueModel).where(
                and_(
                    ReviewQueueModel.session_id == session_id,
                    ReviewQueueModel.status == "pending",
                )
            )
        ).scalars().all()
        result_status = "pending_review" if pending_reviews else "published"

        # Calculate completion time
        completion_time = 0
        if session.started_at and session.submitted_at:
            completion_time = int((session.submitted_at - session.started_at).total_seconds() / 60)

        now = datetime.utcnow()
        existing = self.db.execute(
            select(ExamResultModel).where(ExamResultModel.session_id == session_id)
        ).scalar_one_or_none()

        if existing:
            result = existing
        else:
            result = ExamResultModel(
                id=self._generate_id(),
                session_id=session_id,
                user_id=session.user_id,
                exam_template_id=template.id,
                skill_breakdown_json={},
                time_breakdown_json={},
                strengths_json=[],
                weaknesses_json=[],
                recommendations_json=[],
                created_at=now,
            )
            self.db.add(result)

        result.status = result_status
        result.total_score = total_score
        result.max_possible_score = max_possible
        result.score_percent = score_percent
        result.passed = passed
        result.section_scores_json = section_scores
        result.completion_time_minutes = completion_time
        result.metadata_json = {
            **(result.metadata_json or {}),
            "pending_review_count": len(pending_reviews),
        }
        result.published_at = now if result_status == "published" else None
        result.score_calculated_at = now
        result.updated_at = now

        self.db.commit()
        return result
