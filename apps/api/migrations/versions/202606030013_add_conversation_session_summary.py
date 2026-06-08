"""add conversation session summary

Revision ID: 202606030013
Revises: 202606030012
Create Date: 2026-06-08 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision: str = "202606030013"
down_revision: str = "202606030012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Stores the end-of-session summary + scores so Conversation Partner history
    # (past sessions, scores, done status) survives reloads.
    op.add_column(
        "conversation_sessions",
        sa.Column("summary_json", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("conversation_sessions", "summary_json")
