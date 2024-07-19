"""Initial migration.

Revision ID: 78d2da39c14b
Revises: 78fa34ebd4fc
Create Date: 2024-07-19 09:40:46.496608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78d2da39c14b'
down_revision = '78fa34ebd4fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.alter_column('salary',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Integer(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.alter_column('salary',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###
