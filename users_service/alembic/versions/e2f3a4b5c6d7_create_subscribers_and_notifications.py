"""create_subscribers_and_notifications_sent

Revision ID: e2f3a4b5c6d7
Revises: d1a2b3c4d5e6
Create Date: 2026-03-08 12:01:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2f3a4b5c6d7'
down_revision: Union[str, None] = 'd1a2b3c4d5e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "subscribers",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("subscriber_id", sa.BigInteger, nullable=False),
        sa.Column("author_id", sa.BigInteger, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("subscriber_id", "author_id", name="uq_subscriber_author"),
    )

    op.create_table(
        "notifications_sent",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("subscriber_id", sa.BigInteger, nullable=False),
        sa.Column("post_id", sa.BigInteger, nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("subscriber_id", "post_id", name="uq_subscriber_post"),
    )


def downgrade() -> None:
    op.drop_table("notifications_sent")
    op.drop_table("subscribers")
