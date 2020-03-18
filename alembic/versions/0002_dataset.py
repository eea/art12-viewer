"""dataset

Revision ID: 0002
Revises: 0001
Create Date: 2014-09-29 16:48:02.080721

"""
revision = '0002'
down_revision = '0001'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.create_table(
        'datasets',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('name', mysql.VARCHAR(255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('datasets')
