"""add level test attempts

Revision ID: 202606030008
Revises: 202606030007
Create Date: 2026-06-03 21:20:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "202606030008"
down_revision: Union[str, None] = "202606030007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "level_test_attempts",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("level_code", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("lesson_completion_percent", sa.Integer(), nullable=True),
        sa.Column("scores_json", sa.JSON(), nullable=False),
        sa.Column("responses_json", sa.JSON(), nullable=False),
        sa.Column("evaluation_snapshot_json", sa.JSON(), nullable=False),
        sa.Column("overall_score", sa.Integer(), nullable=True),
        sa.Column("passed", sa.Boolean(), nullable=True),
        sa.Column("missing_requirements_json", sa.JSON(), nullable=False),
        sa.Column("weak_skills_json", sa.JSON(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_level_test_attempts_level_code", "level_test_attempts", ["level_code"])
    op.create_index("ix_level_test_attempts_passed", "level_test_attempts", ["passed"])
    op.create_index("ix_level_test_attempts_status", "level_test_attempts", ["status"])
    op.create_index("ix_level_test_attempts_submitted_at", "level_test_attempts", ["submitted_at"])
    op.create_index("ix_level_test_attempts_updated_at", "level_test_attempts", ["updated_at"])
    op.create_index("ix_level_test_attempts_user_id", "level_test_attempts", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_level_test_attempts_user_id", table_name="level_test_attempts")
    op.drop_index("ix_level_test_attempts_updated_at", table_name="level_test_attempts")
    op.drop_index("ix_level_test_attempts_submitted_at", table_name="level_test_attempts")
    op.drop_index("ix_level_test_attempts_status", table_name="level_test_attempts")
    op.drop_index("ix_level_test_attempts_passed", table_name="level_test_attempts")
    op.drop_index("ix_level_test_attempts_level_code", table_name="level_test_attempts")
    op.drop_table("level_test_attempts")
