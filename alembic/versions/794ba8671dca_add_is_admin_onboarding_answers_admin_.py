"""add is_admin, onboarding_answers, admin_knowledge table

Revision ID: 794ba8671dca
Revises: a1b2c3d4e5f6
Create Date: 2026-06-06 12:34:42.794264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '794ba8671dca'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Add is_admin to user_accounts
    op.add_column('user_accounts', sa.Column('is_admin', sa.Boolean(), server_default='false', nullable=False))
    
    # 2. Add onboarding_answers to business_identities
    op.add_column('business_identities', sa.Column('onboarding_answers', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    
    # 3. Create admin_knowledge table
    op.create_table('admin_knowledge',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('uploaded_by', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('content_type', sa.String(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('is_embedded', sa.Boolean(), nullable=True),
    sa.Column('embedding_ids', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('chunk_count', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('source_url', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['uploaded_by'], ['user_accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('admin_knowledge')
    op.drop_column('business_identities', 'onboarding_answers')
    op.drop_column('user_accounts', 'is_admin')
