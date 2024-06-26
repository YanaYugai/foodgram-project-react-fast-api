"""Deleted rows for checking tables_3

Revision ID: 8b01fc9f5403
Revises: e28b934887aa
Create Date: 2024-04-13 23:02:41.763423

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8b01fc9f5403'
down_revision: Union[str, None] = 'e28b934887aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tagsinrecipe')
    op.drop_table('ingredientsinrecipe')
    op.drop_table('tag')
    op.drop_table('ingredient')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'ingredient',
        sa.Column(
            'id',
            sa.INTEGER(),
            server_default=sa.text("nextval('ingredient_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            'name', sa.VARCHAR(length=200), autoincrement=False, nullable=False
        ),
        sa.Column(
            'measurement_unit',
            sa.VARCHAR(length=200),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id', name='ingredient_pkey'),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        'tag',
        sa.Column(
            'id',
            sa.INTEGER(),
            server_default=sa.text("nextval('tag_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            'name', sa.VARCHAR(length=200), autoincrement=False, nullable=False
        ),
        sa.Column(
            'color', sa.VARCHAR(length=7), autoincrement=False, nullable=False
        ),
        sa.Column(
            'slug', sa.VARCHAR(length=200), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint('id', name='tag_pkey'),
        sa.UniqueConstraint('slug', name='tag_slug_key'),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        'ingredientsinrecipe',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            'recipe_id', sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            'ingredient_id', sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column('amount', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ['ingredient_id'],
            ['ingredient.id'],
            name='ingredientsinrecipe_ingredient_id_fkey',
        ),
        sa.ForeignKeyConstraint(
            ['recipe_id'],
            ['recipe.id'],
            name='ingredientsinrecipe_recipe_id_fkey',
        ),
        sa.PrimaryKeyConstraint('id', name='ingredientsinrecipe_pkey'),
        sa.UniqueConstraint(
            'recipe_id',
            'ingredient_id',
            name='ingredientsinrecipe_recipe_id_ingredient_id_key',
        ),
    )
    op.create_table(
        'tagsinrecipe',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            'recipe_id', sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column('tag_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ['recipe_id'], ['recipe.id'], name='tagsinrecipe_recipe_id_fkey'
        ),
        sa.ForeignKeyConstraint(
            ['tag_id'], ['tag.id'], name='tagsinrecipe_tag_id_fkey'
        ),
        sa.PrimaryKeyConstraint('id', name='tagsinrecipe_pkey'),
        sa.UniqueConstraint(
            'recipe_id', 'tag_id', name='tagsinrecipe_recipe_id_tag_id_key'
        ),
    )
    # ### end Alembic commands ###
