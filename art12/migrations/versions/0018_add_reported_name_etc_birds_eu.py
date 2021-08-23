"""add reported_name to etc_birds_eu_view

Revision ID: 0018
Revises: 0017
Create Date: 2020-06-19 16:43:53.628563

"""

# revision identifiers, used by Alembic.
revision = "0018"
down_revision = "0017"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        "etc_birds_eu_view", sa.Column("reported_name", sa.Text(), nullable=True)
    )


def downgrade():
    op.drop_column("etc_birds_eu_view", "reported_name")
