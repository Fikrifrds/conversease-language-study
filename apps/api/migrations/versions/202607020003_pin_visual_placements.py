"""pin visual placements by default

Revision ID: 202607020003
Revises: 202607020002
Create Date: 2026-07-02 00:00:02.000000
"""

from alembic import op
import sqlalchemy as sa


revision: str = "202607020003"
down_revision: str = "202607020002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("UPDATE visual_placements SET mode = 'pinned'")
    op.alter_column(
        "visual_placements",
        "mode",
        existing_type=sa.String(length=32),
        nullable=False,
        server_default="pinned",
    )


def downgrade() -> None:
    op.alter_column(
        "visual_placements",
        "mode",
        existing_type=sa.String(length=32),
        nullable=False,
        server_default="follow_lesson",
    )
