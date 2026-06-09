"""add conversation turn stt metadata

Revision ID: 202606030011
Revises: 202606030010
Create Date: 2026-06-04 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision: str = "202606030011"
down_revision: str = "202606030010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "conversation_turns",
        sa.Column("input_source", sa.String(length=32), server_default="typed", nullable=False),
    )
    op.add_column("conversation_turns", sa.Column("stt_provider", sa.String(length=32), nullable=True))
    op.add_column("conversation_turns", sa.Column("stt_model", sa.String(length=80), nullable=True))
    op.add_column(
        "conversation_turns",
        sa.Column("stt_transcript_id", sa.String(length=128), nullable=True),
    )
    op.add_column("conversation_turns", sa.Column("stt_confidence", sa.Float(), nullable=True))
    op.add_column(
        "conversation_turns",
        sa.Column("stt_audio_duration_seconds", sa.Float(), nullable=True),
    )
    op.add_column("conversation_turns", sa.Column("stt_metadata_json", sa.JSON(), nullable=True))
    op.create_index(
        "ix_conversation_turns_stt_transcript_id",
        "conversation_turns",
        ["stt_transcript_id"],
    )
    bind = op.get_bind()
    if bind.dialect.name != "sqlite":
        op.alter_column("conversation_turns", "input_source", server_default=None)


def downgrade() -> None:
    op.drop_index("ix_conversation_turns_stt_transcript_id", table_name="conversation_turns")
    op.drop_column("conversation_turns", "stt_metadata_json")
    op.drop_column("conversation_turns", "stt_audio_duration_seconds")
    op.drop_column("conversation_turns", "stt_confidence")
    op.drop_column("conversation_turns", "stt_transcript_id")
    op.drop_column("conversation_turns", "stt_model")
    op.drop_column("conversation_turns", "stt_provider")
    op.drop_column("conversation_turns", "input_source")
