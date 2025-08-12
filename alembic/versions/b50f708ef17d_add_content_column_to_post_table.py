"""add content column to post table

Revision ID: b50f708ef17d
Revises: f8254b26a183
Create Date: 2025-08-12 09:28:35.744297

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b50f708ef17d'
down_revision: Union[str, Sequence[str], None] = 'f8254b26a183'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts', 
        sa.Column(
            'content', 
            sa.String(),
            nullable=False,
            )
        )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
