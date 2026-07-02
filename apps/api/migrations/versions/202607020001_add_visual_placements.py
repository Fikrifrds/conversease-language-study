"""add visual placements

Revision ID: 202607020001
Revises: 202607010002
Create Date: 2026-07-02 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision: str = "202607020001"
down_revision: str = "202607010002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "visual_placements",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("owner_type", sa.String(length=32), nullable=False),
        sa.Column("owner_key", sa.String(length=240), nullable=False),
        sa.Column("slot", sa.String(length=64), nullable=False),
        sa.Column("asset_id", sa.String(length=64), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["asset_id"], ["lesson_visual_assets.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "owner_type",
            "owner_key",
            "slot",
            name="uq_visual_placements_owner_slot",
        ),
    )
    op.create_index(
        "ix_visual_placements_asset_id", "visual_placements", ["asset_id"]
    )
    op.create_index(
        "ix_visual_placements_owner_key", "visual_placements", ["owner_key"]
    )
    op.create_index(
        "ix_visual_placements_owner_type", "visual_placements", ["owner_type"]
    )
    op.create_index("ix_visual_placements_slot", "visual_placements", ["slot"])
    op.create_index(
        "ix_visual_placements_updated_at", "visual_placements", ["updated_at"]
    )


def downgrade() -> None:
    op.drop_index("ix_visual_placements_updated_at", table_name="visual_placements")
    op.drop_index("ix_visual_placements_slot", table_name="visual_placements")
    op.drop_index("ix_visual_placements_owner_type", table_name="visual_placements")
    op.drop_index("ix_visual_placements_owner_key", table_name="visual_placements")
    op.drop_index("ix_visual_placements_asset_id", table_name="visual_placements")
    op.drop_table("visual_placements")
