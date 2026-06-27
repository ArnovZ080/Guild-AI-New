"""add contact_id and reply_to to nurture_sequences

Revision ID: 31f53b66fb92
Revises: 43f67ae46482
Create Date: 2026-06-16 08:06:11.097961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31f53b66fb92'
down_revision: Union[str, Sequence[str], None] = '43f67ae46482'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("nurture_sequences",
        sa.Column("contact_id", sa.String(), sa.ForeignKey("contacts.id"), nullable=True))


def downgrade() -> None:
    op.drop_column("nurture_sequences", "contact_id")
