"""add billing access tables

Revision ID: 202606030004
Revises: 202606030003
Create Date: 2026-06-03 14:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "202606030004"
down_revision: Union[str, None] = "202606030003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_subscriptions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("plan_key", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("starts_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_subscriptions_expires_at", "user_subscriptions", ["expires_at"])
    op.create_index("ix_user_subscriptions_plan_key", "user_subscriptions", ["plan_key"])
    op.create_index("ix_user_subscriptions_status", "user_subscriptions", ["status"])
    op.create_index("ix_user_subscriptions_updated_at", "user_subscriptions", ["updated_at"])
    op.create_index("ix_user_subscriptions_user_id", "user_subscriptions", ["user_id"])

    op.create_table(
        "minute_ledger_entries",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("amount_minutes", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("balance_type", sa.String(length=32), nullable=False),
        sa.Column("related_session_id", sa.String(length=64), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_minute_ledger_entries_balance_type", "minute_ledger_entries", ["balance_type"])
    op.create_index("ix_minute_ledger_entries_created_at", "minute_ledger_entries", ["created_at"])
    op.create_index("ix_minute_ledger_entries_expires_at", "minute_ledger_entries", ["expires_at"])
    op.create_index("ix_minute_ledger_entries_source", "minute_ledger_entries", ["source"])
    op.create_index("ix_minute_ledger_entries_user_id", "minute_ledger_entries", ["user_id"])

    op.create_table(
        "payment_orders",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("package_key", sa.String(length=64), nullable=False),
        sa.Column("payment_kind", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("amount_idr", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("provider_reference", sa.String(length=128), nullable=False),
        sa.Column("checkout_url", sa.Text(), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_payment_orders_package_key", "payment_orders", ["package_key"])
    op.create_index("ix_payment_orders_payment_kind", "payment_orders", ["payment_kind"])
    op.create_index("ix_payment_orders_provider_reference", "payment_orders", ["provider_reference"])
    op.create_index("ix_payment_orders_status", "payment_orders", ["status"])
    op.create_index("ix_payment_orders_updated_at", "payment_orders", ["updated_at"])
    op.create_index("ix_payment_orders_user_id", "payment_orders", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_payment_orders_user_id", table_name="payment_orders")
    op.drop_index("ix_payment_orders_updated_at", table_name="payment_orders")
    op.drop_index("ix_payment_orders_status", table_name="payment_orders")
    op.drop_index("ix_payment_orders_provider_reference", table_name="payment_orders")
    op.drop_index("ix_payment_orders_payment_kind", table_name="payment_orders")
    op.drop_index("ix_payment_orders_package_key", table_name="payment_orders")
    op.drop_table("payment_orders")

    op.drop_index("ix_minute_ledger_entries_user_id", table_name="minute_ledger_entries")
    op.drop_index("ix_minute_ledger_entries_source", table_name="minute_ledger_entries")
    op.drop_index("ix_minute_ledger_entries_expires_at", table_name="minute_ledger_entries")
    op.drop_index("ix_minute_ledger_entries_created_at", table_name="minute_ledger_entries")
    op.drop_index("ix_minute_ledger_entries_balance_type", table_name="minute_ledger_entries")
    op.drop_table("minute_ledger_entries")

    op.drop_index("ix_user_subscriptions_user_id", table_name="user_subscriptions")
    op.drop_index("ix_user_subscriptions_updated_at", table_name="user_subscriptions")
    op.drop_index("ix_user_subscriptions_status", table_name="user_subscriptions")
    op.drop_index("ix_user_subscriptions_plan_key", table_name="user_subscriptions")
    op.drop_index("ix_user_subscriptions_expires_at", table_name="user_subscriptions")
    op.drop_table("user_subscriptions")
