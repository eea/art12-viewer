"""fix float fields for n/a value

Revision ID: 0017
Revises: 0016
Create Date: 2020-05-14 14:10:55.065613

"""

# revision identifiers, used by Alembic.
revision = "0017"
down_revision = "0016"

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.alter_column(
        "etc_data_birds",
        "population_minimum_size_bs",
        existing_type=sa.Float(asdecimal=True),
        type_=sa.String(length=30),
    )
    op.alter_column(
        "etc_data_birds",
        "population_maximum_size_bs",
        existing_type=sa.Float(asdecimal=True),
        type_=sa.String(length=30),
    )
    op.alter_column(
        "etc_data_birds",
        "percentage_population_mean_size_bs",
        existing_type=sa.Float(asdecimal=True),
        type_=sa.String(length=30),
    )
    op.alter_column(
        "etc_data_birds",
        "population_minimum_size_ws",
        existing_type=sa.Float(asdecimal=True),
        type_=sa.String(length=30),
    )
    op.alter_column(
        "etc_data_birds",
        "population_maximum_size_ws",
        existing_type=sa.Float(asdecimal=True),
        type_=sa.String(length=30),
    )
    op.alter_column(
        "etc_data_birds",
        "percentage_population_mean_size_ws",
        existing_type=sa.Float(asdecimal=True),
        type_=sa.String(length=30),
    )
    op.alter_column(
        "etc_data_birds",
        "percentage_distribution_grid_area",
        existing_type=sa.Float(asdecimal=True),
        type_=sa.String(length=30),
    )


def downgrade():
    op.alter_column(
        "etc_data_birds",
        "population_maximum_size_bs",
        existing_type=sa.String(length=30),
        type_=sa.Float(asdecimal=True),
    )
    op.alter_column(
        "etc_data_birds",
        "population_minimum_size_bs",
        existing_type=sa.String(length=30),
        type_=sa.Float(asdecimal=True),
    )
    op.alter_column(
        "etc_data_birds",
        "percentage_population_mean_size_bs",
        existing_type=sa.String(length=30),
        type_=sa.Float(asdecimal=True),
    )
    op.alter_column(
        "etc_data_birds",
        "population_minimum_size_ws",
        existing_type=sa.String(length=30),
        type_=sa.Float(asdecimal=True),
    )
    op.alter_column(
        "etc_data_birds",
        "population_maximum_size_ws",
        existing_type=sa.String(length=30),
        type_=sa.Float(asdecimal=True),
    )
    op.alter_column(
        "etc_data_birds",
        "percentage_population_mean_size_ws",
        existing_type=sa.String(length=30),
        type_=sa.Float(asdecimal=True),
    )
    op.alter_column(
        "etc_data_birds",
        "percentage_distribution_grid_area",
        existing_type=sa.String(length=30),
        type_=sa.Float(asdecimal=True),
    )
