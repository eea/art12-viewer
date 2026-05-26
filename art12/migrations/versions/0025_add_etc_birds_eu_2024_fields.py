"""Add etc_birds_eu_2024 fields

Revision ID: 0025
Revises: 0024
Create Date: 2026-05-26 11:45:02.589847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0025'
down_revision = '0024'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('etc_birds_eu_view', schema=None) as batch_op:
        batch_op.add_column(sa.Column('conclusion_status_label_br_prev', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('red_list_cat_br_prev', sa.String(length=255), nullable=True))


def downgrade():
    with op.batch_alter_table('etc_birds_eu_view', schema=None) as batch_op:
        batch_op.drop_column('red_list_cat_br_prev')
        batch_op.drop_column('conclusion_status_label_br_prev')
