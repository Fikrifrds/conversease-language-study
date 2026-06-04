"""add user roles

Revision ID: 202606030010
Revises: 202606030009
Create Date: 2026-06-04 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision: str = "202606030010"
down_revision: str = "202606030009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("role", sa.String(length=32), server_default="student", nullable=False),
    )
    op.create_index("ix_users_role", "users", ["role"])
    op.alter_column("users", "role", server_default=None)


def downgrade() -> None:
    op.drop_index("ix_users_role", table_name="users")
    op.drop_column("users", "role")
