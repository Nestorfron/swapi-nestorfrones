"""empty message

Revision ID: a6d5dc6fbd56
Revises: d6ec5ce8fa6d
Create Date: 2024-07-18 00:35:10.901183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6d5dc6fbd56'
down_revision = 'd6ec5ce8fa6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'favorite', ['favorite_id'], ['id'])

    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.drop_constraint('favorite_planet_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorite_character_id_fkey', type_='foreignkey')
        batch_op.drop_column('character_id')
        batch_op.drop_column('planet_id')

    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'favorite', ['favorite_id'], ['id'])

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('user_favorite_id_fkey', type_='foreignkey')
        batch_op.drop_column('favorite_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('user_favorite_id_fkey', 'favorite', ['favorite_id'], ['id'])

    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('favorite_id')

    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('character_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('favorite_character_id_fkey', 'character', ['character_id'], ['id'])
        batch_op.create_foreign_key('favorite_planet_id_fkey', 'planet', ['planet_id'], ['id'])

    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('favorite_id')

    # ### end Alembic commands ###
