"""add_subscription_key_to_users

Revision ID: d1a2b3c4d5e6
Revises: b99e9f95e733
Create Date: 2026-03-08 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1a2b3c4d5e6'
down_revision: Union[str, None] = 'b99e9f95e733'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("subscription_key", sa.Text, nullable=True))


def downgrade() -> None:
    op.drop_column("users", "subscription_key")
