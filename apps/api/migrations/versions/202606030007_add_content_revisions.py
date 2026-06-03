"""add content revisions

Revision ID: 202606030007
Revises: 202606030006
Create Date: 2026-06-03 19:40:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "202606030007"
down_revision: Union[str, None] = "202606030006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "content_revisions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("resource_type", sa.String(length=64), nullable=False),
        sa.Column("resource_key", sa.String(length=240), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(length=32), nullable=False),
        sa.Column("changed_by", sa.String(length=160), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("before_json", sa.JSON(), nullable=True),
        sa.Column("after_json", sa.JSON(), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "resource_type",
            "resource_key",
            "version",
            name="uq_content_revisions_resource_version",
        ),
    )
    op.create_index("ix_content_revisions_changed_by", "content_revisions", ["changed_by"])
    op.create_index("ix_content_revisions_content_hash", "content_revisions", ["content_hash"])
    op.create_index("ix_content_revisions_created_at", "content_revisions", ["created_at"])
    op.create_index("ix_content_revisions_resource_key", "content_revisions", ["resource_key"])
    op.create_index("ix_content_revisions_resource_type", "content_revisions", ["resource_type"])
    op.create_index("ix_content_revisions_version", "content_revisions", ["version"])


def downgrade() -> None:
    op.drop_index("ix_content_revisions_version", table_name="content_revisions")
    op.drop_index("ix_content_revisions_resource_type", table_name="content_revisions")
    op.drop_index("ix_content_revisions_resource_key", table_name="content_revisions")
    op.drop_index("ix_content_revisions_created_at", table_name="content_revisions")
    op.drop_index("ix_content_revisions_content_hash", table_name="content_revisions")
    op.drop_index("ix_content_revisions_changed_by", table_name="content_revisions")
    op.drop_table("content_revisions")
