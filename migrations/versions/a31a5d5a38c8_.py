"""empty message

Revision ID: a31a5d5a38c8
Revises: 2d226c622f8d
Create Date: 2024-07-18 00:09:34.819924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a31a5d5a38c8'
down_revision = '2d226c622f8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('character_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'character', ['character_id'], ['id'])
        batch_op.create_foreign_key(None, 'planet', ['planet_id'], ['id'])

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'favorite', ['favorite_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('favorite_id')

    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('character_id')
        batch_op.drop_column('planet_id')

    # ### end Alembic commands ###
