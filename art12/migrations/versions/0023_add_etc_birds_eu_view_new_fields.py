"""Add new fields to etc_birds_eu_view and update other tables to use Integer instead of BigInteger

Revision ID: 0023
Revises: 0022
Create Date: 2026-03-13 15:10:27.922215

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0023"
down_revision = "0022"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("etc_birds_eu_view", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "conclusion_status_label_wi_previous",
                sa.String(length=50),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column("red_list_cat_wi_prev", sa.String(length=255), nullable=True)
        )


def downgrade():
    with op.batch_alter_table("etc_birds_eu_view", schema=None) as batch_op:
        batch_op.drop_column("red_list_cat_wi_prev")
        batch_op.drop_column("conclusion_status_label_wi_previous")
