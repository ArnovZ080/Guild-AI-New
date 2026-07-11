"""onboarding knowledge ledger

Revision ID: 5a3902989ea4
Revises: 84ca8ea25419
Create Date: 2026-07-11 23:36:00.095547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a3902989ea4'
down_revision: Union[str, Sequence[str], None] = '84ca8ea25419'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("business_identities",
        sa.Column("knowledge_ledger", postgresql.JSONB(), server_default="{}"))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("business_identities", "knowledge_ledger")
