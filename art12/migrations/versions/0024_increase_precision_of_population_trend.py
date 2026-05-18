"""Increase precision of population_trend_long_magnitude_max_bs

Revision ID: 0024
Revises: 0023
Create Date: 2026-05-18 14:27:43.254264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0024'
down_revision = '0023'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('etc_data_birds', schema=None) as batch_op:
        batch_op.alter_column('population_trend_long_magnitude_max_bs',
               existing_type=sa.NUMERIC(precision=18, scale=5),
               type_=sa.Numeric(precision=25, scale=5),
               existing_nullable=True)



def downgrade():
    with op.batch_alter_table('etc_data_birds', schema=None) as batch_op:
        batch_op.alter_column('population_trend_long_magnitude_max_bs',
               existing_type=sa.Numeric(precision=25, scale=5),
               type_=sa.NUMERIC(precision=18, scale=5),
               existing_nullable=True)
