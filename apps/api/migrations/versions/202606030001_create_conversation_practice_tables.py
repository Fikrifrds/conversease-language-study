"""create conversation practice tables

Revision ID: 202606030001
Revises:
Create Date: 2026-06-03 09:30:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "202606030001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "conversation_sessions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("demo_user_id", sa.String(length=128), nullable=False),
        sa.Column("language_code", sa.String(length=16), nullable=False),
        sa.Column("level_code", sa.String(length=16), nullable=False),
        sa.Column("mode", sa.String(length=64), nullable=False),
        sa.Column("scenario_key", sa.String(length=128), nullable=False),
        sa.Column("lesson_slug", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_conversation_sessions_demo_user_id",
        "conversation_sessions",
        ["demo_user_id"],
    )
    op.create_index("ix_conversation_sessions_lesson_slug", "conversation_sessions", ["lesson_slug"])
    op.create_index("ix_conversation_sessions_status", "conversation_sessions", ["status"])
    op.create_index("ix_conversation_sessions_updated_at", "conversation_sessions", ["updated_at"])

    op.create_table(
        "conversation_turns",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("session_id", sa.String(length=64), nullable=False),
        sa.Column("turn_index", sa.Integer(), nullable=False),
        sa.Column("user_transcript", sa.Text(), nullable=False),
        sa.Column("coach_reply", sa.Text(), nullable=True),
        sa.Column("minutes_consumed", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["conversation_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "session_id",
            "turn_index",
            name="uq_conversation_turns_session_turn",
        ),
    )
    op.create_index("ix_conversation_turns_session_id", "conversation_turns", ["session_id"])

    op.create_table(
        "conversation_feedback",
        sa.Column("turn_id", sa.String(length=64), nullable=False),
        sa.Column("better_version", sa.Text(), nullable=False),
        sa.Column("indonesian_explanation", sa.Text(), nullable=False),
        sa.Column("scores", sa.JSON(), nullable=False),
        sa.Column("next_practice", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["turn_id"], ["conversation_turns.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("turn_id"),
    )

    op.create_table(
        "practice_progress",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("demo_user_id", sa.String(length=128), nullable=False),
        sa.Column("lesson_slug", sa.String(length=160), nullable=False),
        sa.Column("latest_session_id", sa.String(length=64), nullable=False),
        sa.Column("completed_turns", sa.Integer(), nullable=False),
        sa.Column("total_turns", sa.Integer(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("last_score", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["latest_session_id"],
            ["conversation_sessions.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "demo_user_id",
            "lesson_slug",
            name="uq_practice_progress_user_lesson",
        ),
    )
    op.create_index("ix_practice_progress_demo_user_id", "practice_progress", ["demo_user_id"])
    op.create_index("ix_practice_progress_lesson_slug", "practice_progress", ["lesson_slug"])
    op.create_index("ix_practice_progress_updated_at", "practice_progress", ["updated_at"])


def downgrade() -> None:
    op.drop_index("ix_practice_progress_updated_at", table_name="practice_progress")
    op.drop_index("ix_practice_progress_lesson_slug", table_name="practice_progress")
    op.drop_index("ix_practice_progress_demo_user_id", table_name="practice_progress")
    op.drop_table("practice_progress")

    op.drop_table("conversation_feedback")

    op.drop_index("ix_conversation_turns_session_id", table_name="conversation_turns")
    op.drop_table("conversation_turns")

    op.drop_index("ix_conversation_sessions_updated_at", table_name="conversation_sessions")
    op.drop_index("ix_conversation_sessions_status", table_name="conversation_sessions")
    op.drop_index("ix_conversation_sessions_lesson_slug", table_name="conversation_sessions")
    op.drop_index("ix_conversation_sessions_demo_user_id", table_name="conversation_sessions")
    op.drop_table("conversation_sessions")
