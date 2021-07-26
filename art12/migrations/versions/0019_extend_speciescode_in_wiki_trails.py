"""add reported_name to etc_birds_eu_view

Revision ID: 0019
Revises: 0018
Create Date: 2020-10-19 16:43:53.628563

"""

# revision identifiers, used by Alembic.
revision = "0019"
down_revision = "0018"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        "wiki_trail",
        "speciescode",
        existing_type=sa.String(length=10),
        type_=sa.String(length=50),
    )
    op.add_column(
        "wiki_trail", sa.Column("reported_name", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "wiki_trail",
        sa.Column("reported_name_code", sa.String(length=100), nullable=True),
    )


def downgrade():
    op.drop_column("wiki_trail", "reported_name_code")
    op.drop_column("wiki_trail", "reported_name")
    op.alter_column(
        "wiki_trail",
        "speciescode",
        existing_type=sa.String(length=50),
        type_=sa.String(length=10),
    )
