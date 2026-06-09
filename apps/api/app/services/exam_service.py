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
)


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

    def create_exam_session(
        self,
        exam_template_id: str,
        user_id: str,
        access_code: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> ExamSessionModel:
        """Create a new exam session for a user."""
        # Verify template exists and is active
        template = self.get_exam_template(exam_template_id)
        if template.status != "active":
            raise ExamServiceError(f"Exam template {exam_template_id} is not active")

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

    def calculate_score(
        self,
        session_id: str,
    ) -> ExamResultModel:
        """Calculate exam results for a submitted session.
        
        This is a placeholder - actual scoring logic will be implemented
        based on item types and rubrics.
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
        result = self.db.execute(
            select(ExamSectionModel)
            .where(ExamSectionModel.exam_template_id == template.id)
        )
        sections = {section.id: section for section in result.scalars().all()}

        # Calculate scores per section
        section_scores = {}
        total_score = 0
        max_possible = 0

        for section in sections.values():
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

            section_scores[section.code] = {
                "score": section_score,
                "max": section_max,
                "percentage": (section_score / section_max * 100) if section_max > 0 else 0,
            }
            total_score += section_score
            max_possible += section_max

        # Calculate final percentage
        score_percent = (total_score / max_possible * 100) if max_possible > 0 else 0
        passed = score_percent >= template.passing_score_percent

        # Calculate completion time
        completion_time = 0
        if session.started_at and session.submitted_at:
            completion_time = int((session.submitted_at - session.started_at).total_seconds() / 60)

        # Create result record
        now = datetime.utcnow()
        result = ExamResultModel(
            id=self._generate_id(),
            session_id=session_id,
            user_id=session.user_id,
            exam_template_id=template.id,
            status="published",
            total_score=total_score,
            max_possible_score=max_possible,
            score_percent=score_percent,
            passed=passed,
            section_scores_json=section_scores,
            skill_breakdown_json={},
            completion_time_minutes=completion_time,
            time_breakdown_json={},
            strengths_json=[],
            weaknesses_json=[],
            recommendations_json=[],
            published_at=now,
            score_calculated_at=now,
            created_at=now,
            updated_at=now,
        )
        self.db.add(result)
        self.db.commit()
        return result
