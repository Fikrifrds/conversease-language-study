"""add manual transfer tracking

Revision ID: 202606030005
Revises: 202606030004
Create Date: 2026-06-03 15:10:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "202606030005"
down_revision: Union[str, None] = "202606030004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("payment_orders", sa.Column("base_amount_idr", sa.Integer(), nullable=True))
    op.add_column("payment_orders", sa.Column("unique_code", sa.Integer(), nullable=True))
    op.add_column("payment_orders", sa.Column("transfer_date", sa.DateTime(), nullable=True))
    op.add_column("payment_orders", sa.Column("confirmed_at", sa.DateTime(), nullable=True))
    op.add_column("payment_orders", sa.Column("approved_at", sa.DateTime(), nullable=True))
    op.add_column("payment_orders", sa.Column("approved_by", sa.String(length=160), nullable=True))
    op.add_column("payment_orders", sa.Column("admin_notes", sa.Text(), nullable=True))
    op.create_index("ix_payment_orders_confirmed_at", "payment_orders", ["confirmed_at"])
    op.create_index("ix_payment_orders_unique_code", "payment_orders", ["unique_code"])


def downgrade() -> None:
    op.drop_index("ix_payment_orders_unique_code", table_name="payment_orders")
    op.drop_index("ix_payment_orders_confirmed_at", table_name="payment_orders")
    op.drop_column("payment_orders", "admin_notes")
    op.drop_column("payment_orders", "approved_by")
    op.drop_column("payment_orders", "approved_at")
    op.drop_column("payment_orders", "confirmed_at")
    op.drop_column("payment_orders", "transfer_date")
    op.drop_column("payment_orders", "unique_code")
    op.drop_column("payment_orders", "base_amount_idr")
