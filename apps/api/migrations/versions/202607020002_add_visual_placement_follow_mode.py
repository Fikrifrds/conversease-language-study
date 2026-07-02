"""add visual placement follow mode

Revision ID: 202607020002
Revises: 202607020001
Create Date: 2026-07-02 00:00:01.000000
"""

from alembic import op
import sqlalchemy as sa


revision: str = "202607020002"
down_revision: str = "202607020001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "visual_placements",
        sa.Column(
            "mode",
            sa.String(length=32),
            nullable=False,
            server_default="follow_lesson",
        ),
    )
    op.add_column(
        "visual_placements",
        sa.Column("source_lesson_slug", sa.String(length=160), nullable=True),
    )
    op.add_column(
        "visual_placements",
        sa.Column("source_slot", sa.String(length=32), nullable=True),
    )
    op.create_index(
        "ix_visual_placements_source_lesson_slug",
        "visual_placements",
        ["source_lesson_slug"],
    )
    op.create_index(
        "ix_visual_placements_source_slot",
        "visual_placements",
        ["source_slot"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_visual_placements_source_slot", table_name="visual_placements"
    )
    op.drop_index(
        "ix_visual_placements_source_lesson_slug", table_name="visual_placements"
    )
    op.drop_column("visual_placements", "source_slot")
    op.drop_column("visual_placements", "source_lesson_slug")
    op.drop_column("visual_placements", "mode")
