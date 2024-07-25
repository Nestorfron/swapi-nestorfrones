"""empty message

Revision ID: 4b354ceeb908
Revises: ad0ecbd33b3e
Create Date: 2024-07-20 19:16:37.169036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b354ceeb908'
down_revision = 'ad0ecbd33b3e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_planet')
    op.drop_table('favorite_character')
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'favorite', ['favorite_id'], ['id'])

    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'favorite', ['favorite_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('favorite_id')

    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('favorite_id')

    op.create_table('favorite_character',
    sa.Column('favorite_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('character_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], name='favorite_character_character_id_fkey'),
    sa.ForeignKeyConstraint(['favorite_id'], ['favorite.id'], name='favorite_character_favorite_id_fkey'),
    sa.PrimaryKeyConstraint('favorite_id', 'character_id', name='favorite_character_pkey')
    )
    op.create_table('favorite_planet',
    sa.Column('favorite_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['favorite_id'], ['favorite.id'], name='favorite_planet_favorite_id_fkey'),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], name='favorite_planet_planet_id_fkey'),
    sa.PrimaryKeyConstraint('favorite_id', 'planet_id', name='favorite_planet_pkey')
    )
    # ### end Alembic commands ###