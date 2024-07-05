"""empty message

Revision ID: 554282309b9e
Revises: 2b93f35b85b2
Create Date: 2024-07-05 09:43:02.677292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '554282309b9e'
down_revision = '2b93f35b85b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.alter_column('urgency',
               existing_type=sa.BOOLEAN(),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.alter_column('urgency',
               existing_type=sa.Integer(),
               type_=sa.BOOLEAN(),
               existing_nullable=True)

    # ### end Alembic commands ###
