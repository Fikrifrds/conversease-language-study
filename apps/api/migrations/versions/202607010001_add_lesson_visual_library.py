"""add lesson visual library

Revision ID: 202607010001
Revises: 202606090001
Create Date: 2026-07-01 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision: str = "202607010001"
down_revision: str = "202606090001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "lesson_visual_assets",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("storage_key", sa.Text(), nullable=False),
        sa.Column("preview_storage_key", sa.Text(), nullable=False),
        sa.Column("mime_type", sa.String(length=64), nullable=False),
        sa.Column("source_lesson_slug", sa.String(length=160), nullable=True),
        sa.Column("source_slot", sa.String(length=32), nullable=False),
        sa.Column("model", sa.String(length=120), nullable=False),
        sa.Column("archive_reason", sa.String(length=64), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column("byte_count", sa.Integer(), nullable=False),
        sa.Column("description_json", sa.JSON(), nullable=False),
        sa.Column("prompt_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("content_hash"),
        sa.UniqueConstraint("storage_key"),
    )
    op.create_index(
        "ix_lesson_visual_assets_content_hash",
        "lesson_visual_assets",
        ["content_hash"],
    )
    op.create_index(
        "ix_lesson_visual_assets_created_at", "lesson_visual_assets", ["created_at"]
    )
    op.create_index(
        "ix_lesson_visual_assets_model", "lesson_visual_assets", ["model"]
    )
    op.create_index(
        "ix_lesson_visual_assets_source_lesson_slug",
        "lesson_visual_assets",
        ["source_lesson_slug"],
    )
    op.create_index(
        "ix_lesson_visual_assets_source_slot",
        "lesson_visual_assets",
        ["source_slot"],
    )

    op.create_table(
        "lesson_visual_active",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("lesson_slug", sa.String(length=160), nullable=False),
        sa.Column("slot", sa.String(length=32), nullable=False),
        sa.Column("asset_id", sa.String(length=64), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["asset_id"], ["lesson_visual_assets.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "lesson_slug", "slot", name="uq_lesson_visual_active_lesson_slot"
        ),
    )
    op.create_index(
        "ix_lesson_visual_active_asset_id", "lesson_visual_active", ["asset_id"]
    )
    op.create_index(
        "ix_lesson_visual_active_lesson_slug",
        "lesson_visual_active",
        ["lesson_slug"],
    )
    op.create_index(
        "ix_lesson_visual_active_slot", "lesson_visual_active", ["slot"]
    )
    op.create_index(
        "ix_lesson_visual_active_updated_at",
        "lesson_visual_active",
        ["updated_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_lesson_visual_active_updated_at", table_name="lesson_visual_active")
    op.drop_index("ix_lesson_visual_active_slot", table_name="lesson_visual_active")
    op.drop_index("ix_lesson_visual_active_lesson_slug", table_name="lesson_visual_active")
    op.drop_index("ix_lesson_visual_active_asset_id", table_name="lesson_visual_active")
    op.drop_table("lesson_visual_active")
    op.drop_index("ix_lesson_visual_assets_source_slot", table_name="lesson_visual_assets")
    op.drop_index(
        "ix_lesson_visual_assets_source_lesson_slug", table_name="lesson_visual_assets"
    )
    op.drop_index("ix_lesson_visual_assets_model", table_name="lesson_visual_assets")
    op.drop_index("ix_lesson_visual_assets_created_at", table_name="lesson_visual_assets")
    op.drop_index("ix_lesson_visual_assets_content_hash", table_name="lesson_visual_assets")
    op.drop_table("lesson_visual_assets")
