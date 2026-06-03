from datetime import datetime
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ConversationSessionModel(Base):
    __tablename__ = "conversation_sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[Optional[str]] = mapped_column(
        String(64),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    demo_user_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    language_code: Mapped[str] = mapped_column(String(16), nullable=False)
    level_code: Mapped[str] = mapped_column(String(16), nullable=False)
    mode: Mapped[str] = mapped_column(String(64), nullable=False)
    scenario_key: Mapped[str] = mapped_column(String(128), nullable=False)
    lesson_slug: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)

    turns: Mapped[list["ConversationTurnModel"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ConversationTurnModel.turn_index",
    )


class ConversationTurnModel(Base):
    __tablename__ = "conversation_turns"
    __table_args__ = (
        UniqueConstraint("session_id", "turn_index", name="uq_conversation_turns_session_turn"),
    )

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("conversation_sessions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    turn_index: Mapped[int] = mapped_column(Integer, nullable=False)
    user_transcript: Mapped[str] = mapped_column(Text, nullable=False)
    coach_reply: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    minutes_consumed: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    session: Mapped[ConversationSessionModel] = relationship(back_populates="turns")
    feedback: Mapped["ConversationFeedbackModel"] = relationship(
        back_populates="turn",
        cascade="all, delete-orphan",
        uselist=False,
    )


class ConversationFeedbackModel(Base):
    __tablename__ = "conversation_feedback"

    turn_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("conversation_turns.id", ondelete="CASCADE"),
        primary_key=True,
    )
    better_version: Mapped[str] = mapped_column(Text, nullable=False)
    indonesian_explanation: Mapped[str] = mapped_column(Text, nullable=False)
    scores: Mapped[dict] = mapped_column(JSON, nullable=False)
    next_practice: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    turn: Mapped[ConversationTurnModel] = relationship(back_populates="feedback")


class PracticeProgressModel(Base):
    __tablename__ = "practice_progress"
    __table_args__ = (
        UniqueConstraint("demo_user_id", "lesson_slug", name="uq_practice_progress_user_lesson"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[str]] = mapped_column(
        String(64),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    demo_user_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    lesson_slug: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    latest_session_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("conversation_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    completed_turns: Mapped[int] = mapped_column(Integer, nullable=False)
    total_turns: Mapped[int] = mapped_column(Integer, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    last_score: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)


class UserOnboardingProfileModel(Base):
    __tablename__ = "user_onboarding_profiles"

    user_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    primary_goal: Mapped[str] = mapped_column(String(120), nullable=False)
    confidence_level: Mapped[str] = mapped_column(String(160), nullable=False)
    daily_target_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    recommended_course_slug: Mapped[str] = mapped_column(String(160), nullable=False)
    recommended_level_code: Mapped[str] = mapped_column(String(16), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)


class LessonProgressModel(Base):
    __tablename__ = "lesson_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "lesson_slug", name="uq_lesson_progress_user_lesson"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    course_slug: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    lesson_slug: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    completed_sections: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)


class LevelTestAttemptModel(Base):
    __tablename__ = "level_test_attempts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    level_code: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    lesson_completion_percent: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    scores_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    responses_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    evaluation_snapshot_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    overall_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    passed: Mapped[Optional[bool]] = mapped_column(Boolean, index=True, nullable=True)
    missing_requirements_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    weak_skills_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True, nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True, nullable=True)
    reviewed_by: Mapped[Optional[str]] = mapped_column(String(160), nullable=True)
    admin_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)


class UserSubscriptionModel(Base):
    __tablename__ = "user_subscriptions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    plan_key: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)


class MinuteLedgerEntryModel(Base):
    __tablename__ = "minute_ledger_entries"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    amount_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    source: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    balance_type: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    related_session_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)


class PaymentOrderModel(Base):
    __tablename__ = "payment_orders"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    package_key: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    payment_kind: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    amount_idr: Mapped[int] = mapped_column(Integer, nullable=False)
    base_amount_idr: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    unique_code: Mapped[Optional[int]] = mapped_column(Integer, index=True, nullable=True)
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    provider_reference: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    checkout_url: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    transfer_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True, nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    approved_by: Mapped[Optional[str]] = mapped_column(String(160), nullable=True)
    admin_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    email_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class AuthTokenModel(Base):
    __tablename__ = "auth_tokens"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    token_type: Mapped[str] = mapped_column(String(48), index=True, nullable=False)
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class ContentRevisionModel(Base):
    __tablename__ = "content_revisions"
    __table_args__ = (
        UniqueConstraint(
            "resource_type",
            "resource_key",
            "version",
            name="uq_content_revisions_resource_version",
        ),
    )

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    resource_type: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    resource_key: Mapped[str] = mapped_column(String(240), index=True, nullable=False)
    version: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    action: Mapped[str] = mapped_column(String(32), nullable=False)
    changed_by: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    before_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    after_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)
