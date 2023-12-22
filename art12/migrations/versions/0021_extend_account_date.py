"""empty message

Revision ID: 8a10b516e6a4
Revises: 0020
Create Date: 2023-12-22 13:12:19.067055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0021"
down_revision = "0020"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "registered_users",
        "account_date",
        existing_type=sa.String(length=16),
        type_=sa.String(length=100),
    )


def downgrade():
    op.alter_column(
        "registered_users",
        "account_date",
        existing_type=sa.String(length=100),
        type_=sa.String(length=16),
    )
