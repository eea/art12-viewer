from alembic import op
import sqlalchemy as sa

"""empty message

Revision ID: 0015
Revises: 0014
Create Date: 2020-05-11 13:02:41.122492

"""

# revision identifiers, used by Alembic.
revision = "0015"
down_revision = "0014"


def upgrade():
    op.alter_column(
        "etc_data_birds",
        "distribution_grid_area",
        existing_type=sa.Float(asdecimal=True),
        type_=sa.String(length=20),
    )


def downgrade():
    op.alter_column(
        "etc_data_birds",
        "distribution_grid_area",
        existing_type=sa.String(length=20),
        type_=sa.Float(asdecimal=True),
    )
