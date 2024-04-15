"""change id to nullable

Revision ID: a1eaa196c260
Revises: 357d70dbb450
Create Date: 2024-04-14 19:09:46.239106

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a1eaa196c260'
down_revision: Union[str, None] = '357d70dbb450'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'ingredientsinrecipe',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ingredientsinrecipe', 'id')
    # ### end Alembic commands ###
