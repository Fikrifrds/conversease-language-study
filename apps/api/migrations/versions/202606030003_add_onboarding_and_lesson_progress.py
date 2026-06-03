"""add onboarding and lesson progress

Revision ID: 202606030003
Revises: 202606030002
Create Date: 2026-06-03 12:15:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "202606030003"
down_revision: Union[str, None] = "202606030002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_onboarding_profiles",
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("primary_goal", sa.String(length=120), nullable=False),
        sa.Column("confidence_level", sa.String(length=160), nullable=False),
        sa.Column("daily_target_minutes", sa.Integer(), nullable=False),
        sa.Column("recommended_course_slug", sa.String(length=160), nullable=False),
        sa.Column("recommended_level_code", sa.String(length=16), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_index(
        "ix_user_onboarding_profiles_updated_at",
        "user_onboarding_profiles",
        ["updated_at"],
    )

    op.create_table(
        "lesson_progress",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("course_slug", sa.String(length=160), nullable=False),
        sa.Column("lesson_slug", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("completed_sections", sa.JSON(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "lesson_slug", name="uq_lesson_progress_user_lesson"),
    )
    op.create_index("ix_lesson_progress_course_slug", "lesson_progress", ["course_slug"])
    op.create_index("ix_lesson_progress_lesson_slug", "lesson_progress", ["lesson_slug"])
    op.create_index("ix_lesson_progress_status", "lesson_progress", ["status"])
    op.create_index("ix_lesson_progress_updated_at", "lesson_progress", ["updated_at"])
    op.create_index("ix_lesson_progress_user_id", "lesson_progress", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_lesson_progress_user_id", table_name="lesson_progress")
    op.drop_index("ix_lesson_progress_updated_at", table_name="lesson_progress")
    op.drop_index("ix_lesson_progress_status", table_name="lesson_progress")
    op.drop_index("ix_lesson_progress_lesson_slug", table_name="lesson_progress")
    op.drop_index("ix_lesson_progress_course_slug", table_name="lesson_progress")
    op.drop_table("lesson_progress")

    op.drop_index(
        "ix_user_onboarding_profiles_updated_at",
        table_name="user_onboarding_profiles",
    )
    op.drop_table("user_onboarding_profiles")
