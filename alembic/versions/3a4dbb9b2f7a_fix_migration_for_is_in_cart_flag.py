"""Fix migration for is_in_cart flag

Revision ID: 3a4dbb9b2f7a
Revises: 46c90b9a775a
Create Date: 2026-01-30 20:46:02.900320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a4dbb9b2f7a'
down_revision: Union[str, Sequence[str], None] = '46c90b9a775a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
