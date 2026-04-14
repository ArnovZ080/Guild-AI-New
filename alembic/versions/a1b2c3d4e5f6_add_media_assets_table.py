"""Add media_assets table

Revision ID: a1b2c3d4e5f6
Revises: dd9d9f191e3c
Create Date: 2026-04-13 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'dd9d9f191e3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'media_assets',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),

        # File info
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('original_filename', sa.String(), nullable=False),
        sa.Column('mime_type', sa.String(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('storage_url', sa.String(), nullable=False),
        sa.Column('thumbnail_url', sa.String(), nullable=True),

        # AI-generated metadata
        sa.Column('ai_description', sa.Text(), nullable=True),
        sa.Column('ai_tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('ai_colors', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('ai_embedding_id', sa.String(), nullable=True),

        # User metadata
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('user_tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('alt_text', sa.String(), nullable=True),

        # Dimensions
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),

        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),

        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_media_assets_user_id', 'media_assets', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_media_assets_user_id', table_name='media_assets')
    op.drop_table('media_assets')
