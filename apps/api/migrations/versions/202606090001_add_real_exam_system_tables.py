"""add_real_exam_system_tables

Revision ID: 202606090001
Revises: 202606030013
Create Date: 2026-06-09 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '202606090001'
down_revision = '202606030013'
branch_labels = None
depends_on = None


def upgrade():
    # Exam Templates (Reusable exam definitions)
    op.create_table(
        'exam_templates',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('code', sa.String(32), unique=True, index=True, nullable=False),
        sa.Column('level_code', sa.String(16), index=True, nullable=False),
        sa.Column('title', sa.String(160), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('passing_score_percent', sa.Integer(), nullable=False, server_default='60'),
        sa.Column('status', sa.String(32), index=True, nullable=False, server_default='draft'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('content_hash', sa.String(64), index=True, nullable=True),
        sa.Column('metadata_json', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('created_by', sa.String(160), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), index=True, nullable=False),
    )

    # Exam Sections
    op.create_table(
        'exam_sections',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('exam_template_id', sa.String(64), sa.ForeignKey('exam_templates.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('code', sa.String(32), nullable=False),
        sa.Column('title', sa.String(160), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('sequence_order', sa.Integer(), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('score_weight_percent', sa.Integer(), nullable=False),
        sa.Column('passing_threshold_percent', sa.Integer(), nullable=True),
        sa.Column('item_types_allowed', sa.JSON(), nullable=False),
        sa.Column('config_json', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('exam_template_id', 'code', name='uq_exam_sections_template_code'),
    )

    # Exam Items (Questions)
    op.create_table(
        'exam_items',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('exam_template_id', sa.String(64), sa.ForeignKey('exam_templates.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('section_id', sa.String(64), sa.ForeignKey('exam_sections.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('item_type', sa.String(32), index=True, nullable=False),
        sa.Column('sequence_order', sa.Integer(), nullable=False),
        sa.Column('score_points', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('stimulus_text', sa.Text(), nullable=True),
        sa.Column('stimulus_audio_url', sa.Text(), nullable=True),
        sa.Column('stimulus_image_url', sa.Text(), nullable=True),
        sa.Column('prompt_text', sa.Text(), nullable=False),
        sa.Column('options_json', sa.JSON(), nullable=True),
        sa.Column('correct_answer', sa.JSON(), nullable=True),
        sa.Column('rubric_criteria', sa.JSON(), nullable=True),
        sa.Column('config_json', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('status', sa.String(32), nullable=False, server_default='active'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Exam Sessions (User's exam attempts)
    op.create_table(
        'exam_sessions',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('exam_template_id', sa.String(64), sa.ForeignKey('exam_templates.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('user_id', sa.String(64), sa.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('access_code', sa.String(64), index=True, nullable=True),
        sa.Column('status', sa.String(32), index=True, nullable=False, server_default='created'),
        sa.Column('current_section_id', sa.String(64), nullable=True),
        sa.Column('current_item_id', sa.String(64), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), index=True, nullable=True),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('time_extension_minutes', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('metadata_json', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), index=True, nullable=False),
    )

    # Item Responses (User's answers)
    op.create_table(
        'item_responses',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('session_id', sa.String(64), sa.ForeignKey('exam_sessions.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('item_id', sa.String(64), sa.ForeignKey('exam_items.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('section_id', sa.String(64), sa.ForeignKey('exam_sections.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('response_type', sa.String(32), nullable=False),
        sa.Column('text_response', sa.Text(), nullable=True),
        sa.Column('selected_option_ids', sa.JSON(), nullable=True),
        sa.Column('matched_pairs', sa.JSON(), nullable=True),
        sa.Column('file_url', sa.Text(), nullable=True),
        sa.Column('audio_duration_seconds', sa.Float(), nullable=True),
        sa.Column('recording_attempts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('score_points_earned', sa.Integer(), nullable=True),
        sa.Column('is_correct', sa.Boolean(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('ai_evaluation_json', sa.JSON(), nullable=True),
        sa.Column('human_reviewed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('reviewed_by', sa.String(160), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(), nullable=True),
        sa.Column('review_notes', sa.Text(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('time_spent_seconds', sa.Integer(), nullable=True),
        sa.Column('metadata_json', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('session_id', 'item_id', name='uq_item_responses_session_item'),
    )

    # Media Artifacts (Audio files, images, etc.)
    op.create_table(
        'media_artifacts',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('owner_type', sa.String(32), index=True, nullable=False),
        sa.Column('owner_id', sa.String(64), index=True, nullable=False),
        sa.Column('artifact_type', sa.String(32), index=True, nullable=False),
        sa.Column('file_url', sa.Text(), nullable=False),
        sa.Column('object_key', sa.Text(), nullable=False),
        sa.Column('mime_type', sa.String(64), nullable=False),
        sa.Column('file_size_bytes', sa.Integer(), nullable=False),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('transcript', sa.Text(), nullable=True),
        sa.Column('stt_provider', sa.String(32), nullable=True),
        sa.Column('stt_model', sa.String(80), nullable=True),
        sa.Column('stt_confidence', sa.Float(), nullable=True),
        sa.Column('metadata_json', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Exam Results
    op.create_table(
        'exam_results',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('session_id', sa.String(64), sa.ForeignKey('exam_sessions.id', ondelete='CASCADE'), index=True, nullable=False, unique=True),
        sa.Column('user_id', sa.String(64), sa.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('exam_template_id', sa.String(64), sa.ForeignKey('exam_templates.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('status', sa.String(32), index=True, nullable=False),
        sa.Column('total_score', sa.Integer(), nullable=False),
        sa.Column('max_possible_score', sa.Integer(), nullable=False),
        sa.Column('score_percent', sa.Float(), nullable=False),
        sa.Column('passed', sa.Boolean(), nullable=False),
        sa.Column('section_scores_json', sa.JSON(), nullable=False),
        sa.Column('skill_breakdown_json', sa.JSON(), nullable=False),
        sa.Column('completion_time_minutes', sa.Integer(), nullable=False),
        sa.Column('time_breakdown_json', sa.JSON(), nullable=False),
        sa.Column('strengths_json', sa.JSON(), nullable=False),
        sa.Column('weaknesses_json', sa.JSON(), nullable=False),
        sa.Column('recommendations_json', sa.JSON(), nullable=False),
        sa.Column('ai_summary', sa.Text(), nullable=True),
        sa.Column('certificate_id', sa.String(64), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('score_calculated_at', sa.DateTime(), nullable=False),
        sa.Column('metadata_json', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Review Queue (For human review of AI-scored items)
    op.create_table(
        'review_queue',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('response_id', sa.String(64), sa.ForeignKey('item_responses.id', ondelete='CASCADE'), index=True, nullable=False, unique=True),
        sa.Column('session_id', sa.String(64), sa.ForeignKey('exam_sessions.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('exam_template_id', sa.String(64), sa.ForeignKey('exam_templates.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('item_type', sa.String(32), index=True, nullable=False),
        sa.Column('priority', sa.Integer(), index=True, nullable=False, server_default='5'),
        sa.Column('status', sa.String(32), index=True, nullable=False, server_default='pending'),
        sa.Column('ai_score_points', sa.Integer(), nullable=True),
        sa.Column('ai_evaluation_json', sa.JSON(), nullable=True),
        sa.Column('ai_confidence_score', sa.Float(), nullable=True),
        sa.Column('human_score_points', sa.Integer(), nullable=True),
        sa.Column('human_reviewed_by', sa.String(160), nullable=True),
        sa.Column('human_reviewed_at', sa.DateTime(), nullable=True),
        sa.Column('human_notes', sa.Text(), nullable=True),
        sa.Column('discrepancy_flags', sa.JSON(), nullable=True),
        sa.Column('assigned_to', sa.String(160), nullable=True),
        sa.Column('assigned_at', sa.DateTime(), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('escalated_at', sa.DateTime(), nullable=True),
        sa.Column('escalated_to', sa.String(160), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # Indexes for common query patterns
    op.create_index('idx_exam_templates_level_status', 'exam_templates', ['level_code', 'status'])
    op.create_index('idx_exam_sections_template_order', 'exam_sections', ['exam_template_id', 'sequence_order'])
    op.create_index('idx_exam_items_section_order', 'exam_items', ['section_id', 'sequence_order'])
    op.create_index('idx_exam_sessions_user_status', 'exam_sessions', ['user_id', 'status'])
    op.create_index('idx_exam_sessions_template', 'exam_sessions', ['exam_template_id'])
    op.create_index('idx_item_responses_session', 'item_responses', ['session_id'])
    op.create_index('idx_media_artifacts_owner', 'media_artifacts', ['owner_type', 'owner_id'])
    op.create_index('idx_exam_results_user', 'exam_results', ['user_id'])
    op.create_index('idx_exam_results_published', 'exam_results', ['published_at'])
    op.create_index('idx_review_queue_status_priority', 'review_queue', ['status', 'priority'])
    op.create_index('idx_review_queue_assigned', 'review_queue', ['assigned_to', 'status'])


def downgrade():
    # Drop indexes first
    op.drop_index('idx_review_queue_assigned', table_name='review_queue')
    op.drop_index('idx_review_queue_status_priority', table_name='review_queue')
    op.drop_index('idx_exam_results_published', table_name='exam_results')
    op.drop_index('idx_exam_results_user', table_name='exam_results')
    op.drop_index('idx_media_artifacts_owner', table_name='media_artifacts')
    op.drop_index('idx_item_responses_session', table_name='item_responses')
    op.drop_index('idx_exam_sessions_template', table_name='exam_sessions')
    op.drop_index('idx_exam_sessions_user_status', table_name='exam_sessions')
    op.drop_index('idx_exam_items_section_order', table_name='exam_items')
    op.drop_index('idx_exam_sections_template_order', table_name='exam_sections')
    op.drop_index('idx_exam_templates_level_status', table_name='exam_templates')

    # Drop tables in reverse order
    op.drop_table('review_queue')
    op.drop_table('exam_results')
    op.drop_table('media_artifacts')
    op.drop_table('item_responses')
    op.drop_table('exam_sessions')
    op.drop_table('exam_items')
    op.drop_table('exam_sections')
    op.drop_table('exam_templates')
