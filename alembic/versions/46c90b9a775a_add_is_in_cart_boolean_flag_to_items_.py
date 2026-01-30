"""Add is_in_cart boolean flag to items table

Revision ID: 46c90b9a775a
Revises: abaa41c6b81f
Create Date: 2026-01-30 20:36:43.323476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46c90b9a775a'
down_revision: Union[str, Sequence[str], None] = 'abaa41c6b81f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
