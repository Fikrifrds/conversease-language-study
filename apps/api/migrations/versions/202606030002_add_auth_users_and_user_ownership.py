"""add auth users and user ownership

Revision ID: 202606030002
Revises: 202606030001
Create Date: 2026-06-03 09:45:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "202606030002"
down_revision: Union[str, None] = "202606030001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    with op.batch_alter_table("conversation_sessions") as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.String(length=64), nullable=True))
        batch_op.create_foreign_key(
            "fk_conversation_sessions_user_id_users",
            "users",
            ["user_id"],
            ["id"],
            ondelete="CASCADE",
        )
    op.create_index("ix_conversation_sessions_user_id", "conversation_sessions", ["user_id"])

    with op.batch_alter_table("practice_progress") as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.String(length=64), nullable=True))
        batch_op.create_foreign_key(
            "fk_practice_progress_user_id_users",
            "users",
            ["user_id"],
            ["id"],
            ondelete="CASCADE",
        )
    op.create_index("ix_practice_progress_user_id", "practice_progress", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_practice_progress_user_id", table_name="practice_progress")
    with op.batch_alter_table("practice_progress") as batch_op:
        batch_op.drop_constraint("fk_practice_progress_user_id_users", type_="foreignkey")
        batch_op.drop_column("user_id")

    op.drop_index("ix_conversation_sessions_user_id", table_name="conversation_sessions")
    with op.batch_alter_table("conversation_sessions") as batch_op:
        batch_op.drop_constraint("fk_conversation_sessions_user_id_users", type_="foreignkey")
        batch_op.drop_column("user_id")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
