"""adding votes table

Revision ID: 2dee2fe2dc6f
Revises: c7095cc7044c
Create Date: 2025-08-12 13:28:23.655366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dee2fe2dc6f'
down_revision: Union[str, Sequence[str], None] = 'c7095cc7044c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'votes', 
        sa.Column('user_id',sa.Integer(), nullable=False, primary_key=True),
        sa.Column('post_id', sa.Integer(), nullable=False, primary_key=True)
        )
    op.create_foreign_key(
        'user_id_fk',
        source_table='votes',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id'],
        ondelete='Cascade'
        )
    op.create_foreign_key(
        "post_id_fk",
        source_table="votes",
        referent_table="posts",
        local_cols=["post_id"],
        remote_cols=["id"],
        ondelete="Cascade",
    )
    pass


def downgrade() -> None:
    op.drop_constraint('user_id_fk', table_name='votes')
    op.drop_constraint('post_id_fk', table_name='votes')
    op.drop_table('votes')
    pass
