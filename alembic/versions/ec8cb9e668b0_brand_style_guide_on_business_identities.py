"""brand style guide on business identities

Revision ID: ec8cb9e668b0
Revises: 31f53b66fb92
Create Date: 2026-06-20 07:24:30.159765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec8cb9e668b0'
down_revision: Union[str, Sequence[str], None] = '31f53b66fb92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("business_identities", sa.Column("website_url", sa.String(), nullable=True))
    op.add_column("business_identities", sa.Column("brand_style_guide", sa.Text(), nullable=True))
    op.add_column("business_identities", sa.Column("style_extracted_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("business_identities", "style_extracted_at")
    op.drop_column("business_identities", "brand_style_guide")
    op.drop_column("business_identities", "website_url")
