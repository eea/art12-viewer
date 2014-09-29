"""dataset

Revision ID: 2d01aa511d91
Revises: 45e69fac91b3
Create Date: 2014-09-29 16:48:02.080721

"""
revision = '2d01aa511d91'
down_revision = '45e69fac91b3'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.create_table('datasets',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('name', mysql.VARCHAR(255), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
    )
    op.alter_column('etc_data_birds', 'ext_dataset_id',
                    existing_type=mysql.INTEGER(display_width=11),
                    nullable=True)


def downgrade():
    op.drop_table('datasets')
