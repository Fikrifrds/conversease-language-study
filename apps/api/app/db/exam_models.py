"""Exam System Models

SQLAlchemy models for the Real Exam System.
Based on the Technical Architecture and A1 Content Schema specifications.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Float,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ExamTemplateModel(Base):
    """Exam template definition - reusable blueprint for exams."""
    __tablename__ = "exam_templates"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    level_code: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer(), nullable=False)
    passing_score_percent: Mapped[int] = mapped_column(Integer(), nullable=False, server_default="60")
    status: Mapped[str] = mapped_column(String(32), index=True, nullable=False, server_default="draft")
    version: Mapped[int] = mapped_column(Integer(), nullable=False, server_default="1")
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), index=True, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON(), nullable=False, server_default="{}")
    created_by: Mapped[str] = mapped_column(String(160), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(), index=True, nullable=False)

    # Relationships
    sections: Mapped[list["ExamSectionModel"]] = relationship(
        back_populates="exam_template",
        cascade="all, delete-orphan",
        order_by="ExamSectionModel.sequence_order",
    )
    items: Mapped[list["ExamItemModel"]] = relationship(
        back_populates="exam_template",
        cascade="all, delete-orphan",
    )


class ExamSectionModel(Base):
    """Exam section - major part of an exam (e.g., Listening, Reading)."""
    __tablename__ = "exam_sections"
    __table_args__ = (
        UniqueConstraint("exam_template_id", "code", name="uq_exam_sections_template_code"),
    )

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    exam_template_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("exam_templates.id", ondelete="CASCADE"), index=True, nullable=False
    )
    code: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    sequence_order: Mapped[int] = mapped_column(Integer(), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer(), nullable=False)
    score_weight_percent: Mapped[int] = mapped_column(Integer(), nullable=False)
    passing_threshold_percent: Mapped[Optional[int]] = mapped_column(Integer(), nullable=True)
    item_types_allowed: Mapped[dict] = mapped_column(JSON(), nullable=False)
    config_json: Mapped[dict] = mapped_column(JSON(), nullable=False, server_default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    # Relationships
    exam_template: Mapped[ExamTemplateModel] = relationship(back_populates="sections")
    items: Mapped[list["ExamItemModel"]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan",
        order_by="ExamItemModel.sequence_order",
    )


class ExamItemModel(Base):
    """Individual exam item/question."""
    __tablename__ = "exam_items"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    exam_template_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("exam_templates.id", ondelete="CASCADE"), index=True, nullable=False
    )
    section_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("exam_sections.id", ondelete="CASCADE"), index=True, nullable=False
    )
    item_type: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    sequence_order: Mapped[int] = mapped_column(Integer(), nullable=False)
    score_points: Mapped[int] = mapped_column(Integer(), nullable=False, server_default="1")
    stimulus_text: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    stimulus_audio_url: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    stimulus_image_url: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    prompt_text: Mapped[str] = mapped_column(Text(), nullable=False)
    options_json: Mapped[Optional[dict]] = mapped_column(JSON(), nullable=True)
    correct_answer: Mapped[Optional[dict]] = mapped_column(JSON(), nullable=True)
    rubric_criteria: Mapped[Optional[dict]] = mapped_column(JSON(), nullable=True)
    config_json: Mapped[dict] = mapped_column(JSON(), nullable=False, server_default="{}")
    status: Mapped[str] = mapped_column(String(32), nullable=False, server_default="active")
    version: Mapped[int] = mapped_column(Integer(), nullable=False, server_default="1")
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    # Relationships
    exam_template: Mapped[ExamTemplateModel] = relationship(back_populates="items")
    section: Mapped[ExamSectionModel] = relationship(back_populates="items")


class ExamSessionModel(Base):
    """User's exam session/attempt."""
    __tablename__ = "exam_sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    exam_template_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("exam_templates.id", ondelete="CASCADE"), index=True, nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    access_code: Mapped[Optional[str]] = mapped_column(String(64), index=True, nullable=True)
    status: Mapped[str] = mapped_column(String(32), index=True, nullable=False, server_default="created")
    current_section_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    current_item_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(), index=True, nullable=True)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    time_extension_minutes: Mapped[int] = mapped_column(Integer(), nullable=False, server_default="0")
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON(), nullable=False, server_default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(), index=True, nullable=False)


class ItemResponseModel(Base):
    """User's response to an exam item."""
    __tablename__ = "item_responses"
    __table_args__ = (
        UniqueConstraint("session_id", "item_id", name="uq_item_responses_session_item"),
    )

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("exam_sessions.id", ondelete="CASCADE"), index=True, nullable=False
    )
    item_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("exam_items.id", ondelete="CASCADE"), index=True, nullable=False
    )
    section_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("exam_sections.id", ondelete="CASCADE"), index=True, nullable=False
    )
    response_type: Mapped[str] = mapped_column(String(32), nullable=False)
    text_response: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    selected_option_ids: Mapped[Optional[list]] = mapped_column(JSON(), nullable=True)
    matched_pairs: Mapped[Optional[dict]] = mapped_column(JSON(), nullable=True)
    file_url: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    audio_duration_seconds: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    recording_attempts: Mapped[int] = mapped_column(Integer(), nullable=False, server_default="0")
    score_points_earned: Mapped[Optional[int]] = mapped_column(Integer(), nullable=True)
    is_correct: Mapped[Optional[bool]] = mapped_column(Boolean(), nullable=True)
    confidence_score: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    ai_evaluation_json: Mapped[Optional[dict]] = mapped_column(JSON(), nullable=True)
    human_reviewed: Mapped[bool] = mapped_column(Boolean(), nullable=False, server_default="false")
    reviewed_by: Mapped[Optional[str]] = mapped_column(String(160), nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    review_notes: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    time_spent_seconds: Mapped[Optional[int]] = mapped_column(Integer(), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON(), nullable=False, server_default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)


class MediaArtifactModel(Base):
    """Media artifacts like audio files, images, etc."""
    __tablename__ = "media_artifacts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    owner_type: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    owner_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    artifact_type: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    file_url: Mapped[str] = mapped_column(Text(), nullable=False)
    object_key: Mapped[str] = mapped_column(Text(), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(64), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer(), nullable=False)
    duration_seconds: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    transcript: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    stt_provider: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    stt_model: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    stt_confidence: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON(), nullable=False, server_default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)


class ExamResultModel(Base):
    """Calculated results for a completed exam session."""
    __tablename__ = "exam_results"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("exam_sessions.id", ondelete="CASCADE"), index=True, nullable=False, unique=True
    )
    user_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    exam_template_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("exam_templates.id", ondelete="CASCADE"), index=True, nullable=False
    )
    status: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    total_score: Mapped[int] = mapped_column(Integer(), nullable=False)
    max_possible_score: Mapped[int] = mapped_column(Integer(), nullable=False)
    score_percent: Mapped[float] = mapped_column(Float(), nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    section_scores_json: Mapped[dict] = mapped_column(JSON(), nullable=False)
    skill_breakdown_json: Mapped[dict] = mapped_column(JSON(), nullable=False)
    completion_time_minutes: Mapped[int] = mapped_column(Integer(), nullable=False)
    time_breakdown_json: Mapped[dict] = mapped_column(JSON(), nullable=False)
    strengths_json: Mapped[dict] = mapped_column(JSON(), nullable=False)
    weaknesses_json: Mapped[dict] = mapped_column(JSON(), nullable=False)
    recommendations_json: Mapped[dict] = mapped_column(JSON(), nullable=False)
    ai_summary: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    certificate_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    score_calculated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON(), nullable=False, server_default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)


class ReviewQueueModel(Base):
    """Queue for human review of AI-scored items."""
    __tablename__ = "review_queue"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    response_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("item_responses.id", ondelete="CASCADE"), index=True, nullable=False, unique=True
    )
    session_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("exam_sessions.id", ondelete="CASCADE"), index=True, nullable=False
    )
    exam_template_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("exam_templates.id", ondelete="CASCADE"), index=True, nullable=False
    )
    item_type: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    priority: Mapped[int] = mapped_column(Integer(), index=True, nullable=False, server_default="5")
    status: Mapped[str] = mapped_column(String(32), index=True, nullable=False, server_default="pending")
    ai_score_points: Mapped[Optional[int]] = mapped_column(Integer(), nullable=True)
    ai_evaluation_json: Mapped[Optional[dict]] = mapped_column(JSON(), nullable=True)
    ai_confidence_score: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    human_score_points: Mapped[Optional[int]] = mapped_column(Integer(), nullable=True)
    human_reviewed_by: Mapped[Optional[str]] = mapped_column(String(160), nullable=True)
    human_reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    human_notes: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    discrepancy_flags: Mapped[Optional[dict]] = mapped_column(JSON(), nullable=True)
    assigned_to: Mapped[Optional[str]] = mapped_column(String(160), nullable=True)
    assigned_at: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    escalated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    escalated_to: Mapped[Optional[str]] = mapped_column(String(160), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
