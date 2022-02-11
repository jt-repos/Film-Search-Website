"""empty message

Revision ID: 393be2c59487
Revises: 5bd86458b2cf
Create Date: 2021-12-13 03:54:00.705650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '393be2c59487'
down_revision = '5bd86458b2cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cinema', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.String(length=256), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cinema', schema=None) as batch_op:
        batch_op.drop_column('address')

    # ### end Alembic commands ###