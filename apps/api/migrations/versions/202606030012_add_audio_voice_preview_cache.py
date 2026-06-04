"""add audio voice preview cache

Revision ID: 202606030012
Revises: 202606030011
Create Date: 2026-06-04 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision: str = "202606030012"
down_revision: str = "202606030011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "audio_voice_previews",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("model", sa.String(length=80), nullable=False),
        sa.Column("voice_id", sa.String(length=160), nullable=False),
        sa.Column("speed", sa.Float(), nullable=False),
        sa.Column("sample_text_hash", sa.String(length=64), nullable=False),
        sa.Column("sample_text", sa.Text(), nullable=False),
        sa.Column("audio_url", sa.Text(), nullable=False),
        sa.Column("object_key", sa.Text(), nullable=False),
        sa.Column("duration_seconds", sa.Float(), nullable=False),
        sa.Column("audio_format", sa.String(length=16), nullable=False),
        sa.Column("audio_size", sa.Integer(), nullable=False),
        sa.Column("trace_id", sa.String(length=160), nullable=True),
        sa.Column("usage_characters", sa.Integer(), nullable=False),
        sa.Column("generated_by", sa.String(length=160), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "provider",
            "model",
            "voice_id",
            "speed",
            "sample_text_hash",
            name="uq_audio_voice_previews_voice_sample",
        ),
    )
    op.create_index("ix_audio_voice_previews_created_at", "audio_voice_previews", ["created_at"])
    op.create_index("ix_audio_voice_previews_generated_by", "audio_voice_previews", ["generated_by"])
    op.create_index("ix_audio_voice_previews_model", "audio_voice_previews", ["model"])
    op.create_index("ix_audio_voice_previews_provider", "audio_voice_previews", ["provider"])
    op.create_index("ix_audio_voice_previews_sample_text_hash", "audio_voice_previews", ["sample_text_hash"])
    op.create_index("ix_audio_voice_previews_updated_at", "audio_voice_previews", ["updated_at"])
    op.create_index("ix_audio_voice_previews_voice_id", "audio_voice_previews", ["voice_id"])


def downgrade() -> None:
    op.drop_index("ix_audio_voice_previews_voice_id", table_name="audio_voice_previews")
    op.drop_index("ix_audio_voice_previews_updated_at", table_name="audio_voice_previews")
    op.drop_index("ix_audio_voice_previews_sample_text_hash", table_name="audio_voice_previews")
    op.drop_index("ix_audio_voice_previews_provider", table_name="audio_voice_previews")
    op.drop_index("ix_audio_voice_previews_model", table_name="audio_voice_previews")
    op.drop_index("ix_audio_voice_previews_generated_by", table_name="audio_voice_previews")
    op.drop_index("ix_audio_voice_previews_created_at", table_name="audio_voice_previews")
    op.drop_table("audio_voice_previews")
