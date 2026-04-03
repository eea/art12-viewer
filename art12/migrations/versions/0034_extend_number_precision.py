"""Extend number precision for population trend magnitude fields

Revision ID: 0034
Revises: 0023
Create Date: 2026-04-03 11:48:04.280959

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0034'
down_revision = '0023'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('etc_data_birds', schema=None) as batch_op:
        batch_op.alter_column('population_trend_long_magnitude_min_bs',
               existing_type=sa.NUMERIC(precision=18, scale=5),
               type_=sa.Numeric(precision=35, scale=20),
               existing_nullable=True)
        batch_op.alter_column('population_trend_long_magnitude_max_bs',
               existing_type=sa.NUMERIC(precision=18, scale=5),
               type_=sa.Numeric(precision=35, scale=20),
               existing_nullable=True)


def downgrade():
    with op.batch_alter_table('etc_data_birds', schema=None) as batch_op:
        batch_op.alter_column('population_trend_long_magnitude_max_bs',
               existing_type=sa.Numeric(precision=35, scale=18),
               type_=sa.NUMERIC(precision=18, scale=5),
               existing_nullable=True)
        batch_op.alter_column('population_trend_long_magnitude_min_bs',
               existing_type=sa.Numeric(precision=18, scale=18),
               type_=sa.NUMERIC(precision=18, scale=5),
               existing_nullable=True)
