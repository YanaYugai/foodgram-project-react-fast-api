"""change id to id_pk

Revision ID: ed6fb0aff535
Revises: a1eaa196c260
Create Date: 2024-04-14 19:26:02.289944

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ed6fb0aff535'
down_revision: Union[str, None] = 'a1eaa196c260'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'ingredientsinrecipe',
        sa.Column('pk_id', sa.Integer(), autoincrement=True, nullable=False),
    )
    op.drop_column('ingredientsinrecipe', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'ingredientsinrecipe',
        sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_column('ingredientsinrecipe', 'pk_id')
    # ### end Alembic commands ###
