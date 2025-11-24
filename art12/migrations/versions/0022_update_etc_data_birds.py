"""Update etc_data_birds filename to nullable

Revision ID: 0022
Revises: 0021
Create Date: 2025-11-24 09:42:11.749430

"""

from alembic import op
import sqlalchemy as sa

revision = "0022"
down_revision = "0021"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("etc_data_birds", schema=None) as batch_op:
        batch_op.alter_column(
            "filename", existing_type=sa.VARCHAR(length=60), nullable=True
        )


def downgrade():

    with op.batch_alter_table("etc_data_birds", schema=None) as batch_op:
        batch_op.alter_column(
            "filename", existing_type=sa.VARCHAR(length=60), nullable=False
        )
