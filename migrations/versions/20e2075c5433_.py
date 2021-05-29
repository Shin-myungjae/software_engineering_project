"""empty message

Revision ID: 20e2075c5433
Revises: b7bdeac0d9b0
Create Date: 2021-05-23 15:53:33.604884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20e2075c5433'
down_revision = 'b7bdeac0d9b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), server_default='1', nullable=True))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
