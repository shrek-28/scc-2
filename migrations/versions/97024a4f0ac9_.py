"""empty message

Revision ID: 97024a4f0ac9
Revises: 41a968ae7e63
Create Date: 2024-07-05 00:22:07.714500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97024a4f0ac9'
down_revision = '41a968ae7e63'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_no', sa.String(length=10), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_column('phone_no')

    # ### end Alembic commands ###
