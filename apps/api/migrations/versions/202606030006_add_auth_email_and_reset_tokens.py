"""add auth email and reset tokens

Revision ID: 202606030006
Revises: 202606030005
Create Date: 2026-06-03 17:20:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "202606030006"
down_revision: Union[str, None] = "202606030005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("email_verified_at", sa.DateTime(), nullable=True))
    op.create_index("ix_users_email_verified_at", "users", ["email_verified_at"])

    op.create_table(
        "auth_tokens",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("token_type", sa.String(length=48), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("used_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash", name="uq_auth_tokens_token_hash"),
    )
    op.create_index("ix_auth_tokens_expires_at", "auth_tokens", ["expires_at"])
    op.create_index("ix_auth_tokens_token_hash", "auth_tokens", ["token_hash"])
    op.create_index("ix_auth_tokens_token_type", "auth_tokens", ["token_type"])
    op.create_index("ix_auth_tokens_used_at", "auth_tokens", ["used_at"])
    op.create_index("ix_auth_tokens_user_id", "auth_tokens", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_auth_tokens_user_id", table_name="auth_tokens")
    op.drop_index("ix_auth_tokens_used_at", table_name="auth_tokens")
    op.drop_index("ix_auth_tokens_token_type", table_name="auth_tokens")
    op.drop_index("ix_auth_tokens_token_hash", table_name="auth_tokens")
    op.drop_index("ix_auth_tokens_expires_at", table_name="auth_tokens")
    op.drop_table("auth_tokens")

    op.drop_index("ix_users_email_verified_at", table_name="users")
    op.drop_column("users", "email_verified_at")
