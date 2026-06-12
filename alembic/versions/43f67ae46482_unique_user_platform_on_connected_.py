"""unique user platform on connected_integrations

Revision ID: 43f67ae46482
Revises: 8403163a3c78
Create Date: 2026-06-12 20:54:13.557354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43f67ae46482'
down_revision: Union[str, Sequence[str], None] = '8403163a3c78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Dedupe first: keep the newest row per (user_id, platform)
    op.execute("""
        DELETE FROM connected_integrations a
        USING connected_integrations b
        WHERE a.user_id = b.user_id
          AND a.platform = b.platform
          AND a.created_at < b.created_at
    """)
    op.create_unique_constraint(
        "uq_connected_integrations_user_platform",
        "connected_integrations",
        ["user_id", "platform"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_connected_integrations_user_platform",
        "connected_integrations",
        type_="unique",
    )
