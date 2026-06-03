"""add level test admin review

Revision ID: 202606030009
Revises: 202606030008
Create Date: 2026-06-03 22:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "202606030009"
down_revision: Union[str, None] = "202606030008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("level_test_attempts", sa.Column("reviewed_at", sa.DateTime(), nullable=True))
    op.add_column("level_test_attempts", sa.Column("reviewed_by", sa.String(length=160), nullable=True))
    op.add_column("level_test_attempts", sa.Column("admin_notes", sa.Text(), nullable=True))
    op.create_index("ix_level_test_attempts_reviewed_at", "level_test_attempts", ["reviewed_at"])


def downgrade() -> None:
    op.drop_index("ix_level_test_attempts_reviewed_at", table_name="level_test_attempts")
    op.drop_column("level_test_attempts", "admin_notes")
    op.drop_column("level_test_attempts", "reviewed_by")
    op.drop_column("level_test_attempts", "reviewed_at")
