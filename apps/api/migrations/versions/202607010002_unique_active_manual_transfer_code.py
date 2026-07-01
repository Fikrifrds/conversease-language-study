"""unique active manual transfer code

Revision ID: 202607010002
Revises: 202607010001
Create Date: 2026-07-01 00:00:00.000001
"""

from alembic import op


revision: str = "202607010002"
down_revision: str = "202607010001"
branch_labels = None
depends_on = None


INDEX_NAME = "ix_payment_orders_active_unique_code"


def upgrade() -> None:
    op.execute(
        f"""
        CREATE UNIQUE INDEX {INDEX_NAME}
        ON payment_orders (provider, unique_code)
        WHERE status IN ('pending', 'confirmed') AND unique_code IS NOT NULL
        """
    )


def downgrade() -> None:
    op.execute(f"DROP INDEX {INDEX_NAME}")
