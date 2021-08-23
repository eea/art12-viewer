"""add_fields_etc_data_birds_period_2018

Revision ID: 0013
Revises: 0012
Create Date: 2020-03-18 10:30:20.486534

"""

# revision identifiers, used by Alembic.
revision = "0013"
down_revision = "0012"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        "datasets", "name", existing_type=sa.String(length=255), nullable=False
    )
    op.create_unique_constraint(None, "datasets", ["id"])

    op.alter_column(
        "etc_birds_eu_view",
        "ID",
        existing_type=sa.Integer(),
        nullable=False,
    )
    op.alter_column(
        "etc_birds_eu_view",
        "assessment_speciesname",
        existing_type=sa.String(length=255),
        nullable=True,
    )

    op.alter_column(
        "etc_data_birds",
        "envelope",
        existing_type=sa.String(length=60),
        type_=sa.Text(),
    )
    op.add_column(
        "etc_data_birds", sa.Column("reported_name", sa.Text(), nullable=True)
    )
    op.alter_column(
        "etc_data_birds",
        "speciescode",
        existing_type=sa.String(length=10),
        type_=sa.String(length=255),
    )
    op.alter_column(
        "etc_data_birds",
        "speciesname",
        existing_type=sa.String(length=128),
        type_=sa.String(length=255),
    )
    op.alter_column(
        "etc_data_birds",
        "subspecies_name",
        existing_type=sa.String(length=128),
        type_=sa.String(length=255),
    )
    op.alter_column(
        "etc_data_birds",
        "alternative_speciesname",
        existing_type=sa.String(length=128),
        type_=sa.String(length=255),
    )
    op.alter_column(
        "etc_data_birds",
        "valid_speciesname",
        existing_type=sa.String(length=128),
        type_=sa.Text(),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("assessment_speciescode", sa.String(length=10), nullable=True),
    )
    op.alter_column(
        "etc_data_birds",
        "assesment_speciesname",
        new_column_name="assessment_speciesname",
        existing_type=sa.String(length=128),
        type_=sa.String(length=255),
    )
    op.alter_column(
        "etc_data_birds",
        "assesment_speciesname_changed",
        new_column_name="assessment_speciesname_changed",
        existing_type=sa.Integer(),
    )
    op.add_column(
        "etc_data_birds", sa.Column("population_size_bs", sa.Text(), nullable=True)
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("population_size_method_bs", sa.String(length=255), nullable=True),
    )
    op.alter_column(
        "etc_data_birds",
        "population_size_unit_bs",
        existing_type=sa.String(length=10),
        type_=sa.String(length=255),
    )
    op.alter_column(
        "etc_data_birds",
        "population_change_reason_bs",
        existing_type=sa.String(length=150),
        type_=sa.String(length=200),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("population_estimateType_bs", sa.String(length=255), nullable=True),
    )
    op.alter_column(
        "etc_data_birds",
        "population_trend_period_bs",
        existing_type=sa.String(length=30),
        type_=sa.String(length=255),
    )
    op.alter_column(
        "etc_data_birds",
        "population_trend_bs",
        existing_type=sa.String(length=2),
        type_=sa.String(length=3),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column(
            "population_trend_magnitude_bs", sa.String(length=131), nullable=True
        ),
    )
    op.alter_column(
        "etc_data_birds",
        "population_trend_long_period_bs",
        existing_type=sa.String(length=30),
        type_=sa.String(length=255),
    )
    op.alter_column(
        "etc_data_birds",
        "population_trend_long_bs",
        existing_type=sa.String(length=2),
        type_=sa.String(length=3),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column(
            "population_trend_long_magnitude_bs", sa.String(length=131), nullable=True
        ),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("distribution_surface_area_bs", sa.Text(), nullable=True),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column(
            "distribution_surface_area_method_bs", sa.String(length=255), nullable=True
        ),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column(
            "distribution_additional_info_record_bs", sa.String(length=1), nullable=True
        ),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("distribution_additional_info_bs", sa.Text(), nullable=True),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("percentage_distribution_surface_area_bs", sa.Text(), nullable=True),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("distribution_trend_period_bs", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("distribution_trend_bs", sa.String(length=3), nullable=True),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("distribution_trend_magnitude_min_bs", sa.Text(), nullable=True),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("distribution_trend_magnitude_max_bs", sa.Text(), nullable=True),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column(
            "distribution_trend_magnitude_bs", sa.String(length=131), nullable=True
        ),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column(
            "distribution_trend_long_period_bs", sa.String(length=255), nullable=True
        ),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("distribution_trend_long_bs", sa.String(length=3), nullable=True),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("distribution_trend_long_magnitude_min_bs", sa.Text(), nullable=True),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("distribution_trend_long_magnitude_max_bs", sa.Text(), nullable=True),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column(
            "distribution_trend_long_magnitude_bs", sa.String(length=131), nullable=True
        ),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column(
            "distribution_trend_additional_info_record_bs",
            sa.String(length=1),
            nullable=True,
        ),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("distribution_trend_additional_info_bs", sa.Text(), nullable=True),
    )
    op.add_column(
        "etc_data_birds", sa.Column("population_size_ws", sa.Text(), nullable=True)
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("population_size_method_ws", sa.String(length=255), nullable=True),
    )
    op.alter_column(
        "etc_data_birds",
        "population_size_unit_ws",
        existing_type=sa.String(length=10),
        type_=sa.String(length=255),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("population_units_agreed_ws", sa.String(length=10), nullable=True),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("population_units_other_ws", sa.String(length=10), nullable=True),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("population_estimateType_ws", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("population_change_reason_ws", sa.String(length=200), nullable=True),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column(
            "number_of_different_population_units_ws", sa.Integer(), nullable=True
        ),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column("different_population_percentage_ws", sa.Integer(), nullable=True),
    )
    op.alter_column(
        "etc_data_birds",
        "population_trend_period_ws",
        existing_type=sa.String(length=30),
        type_=sa.String(length=255),
    )
    op.alter_column(
        "etc_data_birds",
        "population_trend_ws",
        existing_type=sa.String(length=2),
        type_=sa.String(length=3),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column(
            "population_trend_magnitude_ws", sa.String(length=131), nullable=True
        ),
    )
    op.alter_column(
        "etc_data_birds",
        "population_trend_long_period_ws",
        existing_type=sa.String(length=30),
        type_=sa.String(length=255),
    )
    op.alter_column(
        "etc_data_birds",
        "population_trend_long_ws",
        existing_type=sa.String(length=2),
        type_=sa.String(length=3),
    )
    op.add_column(
        "etc_data_birds",
        sa.Column(
            "population_trend_long_magnitude_ws", sa.String(length=131), nullable=True
        ),
    )
    op.add_column(
        "etc_data_birds", sa.Column("status_ws", sa.String(length=18), nullable=True)
    )
    op.add_column(
        "etc_data_birds", sa.Column("use_for_statistics", sa.Text(), nullable=True)
    )
    op.alter_column(
        "lu_birds_name",
        "ext_dataset_id",
        existing_type=sa.Integer(),
        nullable=False,
    )
    op.alter_column(
        "lu_birds_name",
        "speciescode",
        existing_type=sa.String(length=10),
        nullable=False,
    )
    op.alter_column(
        "lu_restricted_birds",
        "show_data",
        existing_type=sa.SmallInteger(),
        nullable=False,
    )
    op.alter_column(
        "wiki_changes", "body", existing_type=sa.String(length=6000), nullable=False
    )


def downgrade():
    op.alter_column(
        "wiki_changes", "body", existing_type=sa.String(length=6000), nullable=True
    )
    op.alter_column(
        "lu_restricted_birds",
        "show_data",
        existing_type=sa.SmallInteger(),
        nullable=True,
    )
    op.alter_column(
        "lu_birds_name",
        "speciescode",
        existing_type=sa.String(length=10),
        nullable=True,
    )
    op.alter_column(
        "lu_birds_name",
        "ext_dataset_id",
        existing_type=sa.Integer(),
        nullable=True,
    )

    op.drop_column("etc_data_birds", "use_for_statistics")
    op.drop_column("etc_data_birds", "status_ws")
    op.drop_column("etc_data_birds", "population_trend_long_magnitude_ws")
    op.alter_column(
        "etc_data_birds",
        "population_trend_long_ws",
        existing_type=sa.String(length=3),
        type_=sa.String(length=2),
    )
    op.alter_column(
        "etc_data_birds",
        "population_trend_long_period_ws",
        existing_type=sa.String(length=255),
        type_=sa.String(length=30),
    )
    op.drop_column("etc_data_birds", "population_trend_magnitude_ws")
    op.alter_column(
        "etc_data_birds",
        "population_trend_ws",
        existing_type=sa.String(length=3),
        type_=sa.String(length=2),
    )
    op.alter_column(
        "etc_data_birds",
        "population_trend_period_ws",
        existing_type=sa.String(length=255),
        type_=sa.String(length=30),
    )
    op.drop_column("etc_data_birds", "different_population_percentage_ws")
    op.drop_column("etc_data_birds", "number_of_different_population_units_ws")
    op.drop_column("etc_data_birds", "population_change_reason_ws")
    op.drop_column("etc_data_birds", "population_estimateType_ws")
    op.drop_column("etc_data_birds", "population_units_other_ws")
    op.drop_column("etc_data_birds", "population_units_agreed_ws")
    op.alter_column(
        "etc_data_birds",
        "population_size_unit_ws",
        existing_type=sa.String(length=255),
        type_=sa.String(length=10),
    )
    op.drop_column("etc_data_birds", "population_size_method_ws")
    op.drop_column("etc_data_birds", "population_size_ws")
    op.drop_column("etc_data_birds", "distribution_trend_additional_info_bs")
    op.drop_column("etc_data_birds", "distribution_trend_additional_info_record_bs")
    op.drop_column("etc_data_birds", "distribution_trend_long_magnitude_bs")
    op.drop_column("etc_data_birds", "distribution_trend_long_magnitude_max_bs")
    op.drop_column("etc_data_birds", "distribution_trend_long_magnitude_min_bs")
    op.drop_column("etc_data_birds", "distribution_trend_long_bs")
    op.drop_column("etc_data_birds", "distribution_trend_long_period_bs")
    op.drop_column("etc_data_birds", "distribution_trend_magnitude_bs")
    op.drop_column("etc_data_birds", "distribution_trend_magnitude_max_bs")
    op.drop_column("etc_data_birds", "distribution_trend_magnitude_min_bs")
    op.drop_column("etc_data_birds", "distribution_trend_bs")
    op.drop_column("etc_data_birds", "distribution_trend_period_bs")
    op.drop_column("etc_data_birds", "percentage_distribution_surface_area_bs")
    op.drop_column("etc_data_birds", "distribution_additional_info_bs")
    op.drop_column("etc_data_birds", "distribution_additional_info_record_bs")
    op.drop_column("etc_data_birds", "distribution_surface_area_method_bs")
    op.drop_column("etc_data_birds", "distribution_surface_area_bs")
    op.drop_column("etc_data_birds", "population_trend_long_magnitude_bs")
    op.alter_column(
        "etc_data_birds",
        "population_trend_long_bs",
        existing_type=sa.String(length=3),
        type_=sa.String(length=2),
    )
    op.alter_column(
        "etc_data_birds",
        "population_trend_long_period_bs",
        existing_type=sa.String(length=255),
        type_=sa.String(length=30),
    )
    op.drop_column("etc_data_birds", "population_trend_magnitude_bs")
    op.alter_column(
        "etc_data_birds",
        "population_trend_bs",
        existing_type=sa.String(length=3),
        type_=sa.String(length=2),
    )
    op.alter_column(
        "etc_data_birds",
        "population_trend_period_bs",
        existing_type=sa.String(length=255),
        type_=sa.String(length=30),
    )
    op.drop_column("etc_data_birds", "population_estimateType_bs")
    op.alter_column(
        "etc_data_birds",
        "population_change_reason_bs",
        existing_type=sa.String(length=200),
        type_=sa.String(length=150),
    )
    op.alter_column(
        "etc_data_birds",
        "population_size_unit_bs",
        existing_type=sa.String(length=255),
        type_=sa.String(length=10),
    )
    op.drop_column("etc_data_birds", "population_size_method_bs")
    op.drop_column("etc_data_birds", "population_size_bs")
    op.alter_column(
        "etc_data_birds",
        "assessment_speciesname_changed",
        new_column_name="assesment_speciesname_changed",
        existing_type=sa.Integer(),
    )
    op.alter_column(
        "etc_data_birds",
        "assessment_speciesname",
        new_column_name="assesment_speciesname",
        existing_type=sa.String(length=255),
        type_=sa.String(length=128),
    )
    op.drop_column("etc_data_birds", "assessment_speciescode")
    op.alter_column(
        "etc_data_birds",
        "valid_speciesname",
        existing_type=sa.Text(),
        type_=sa.String(length=128),
    )
    op.alter_column(
        "etc_data_birds",
        "alternative_speciesname",
        existing_type=sa.String(length=255),
        type_=sa.String(length=128),
    )
    op.alter_column(
        "etc_data_birds",
        "subspecies_name",
        existing_type=sa.String(length=255),
        type_=sa.String(length=128),
    )
    op.alter_column(
        "etc_data_birds",
        "speciesname",
        existing_type=sa.String(length=255),
        type_=sa.String(length=128),
    )
    op.alter_column(
        "etc_data_birds",
        "speciescode",
        existing_type=sa.String(length=255),
        type_=sa.String(length=10),
    )
    op.drop_column("etc_data_birds", "reported_name")
    op.alter_column(
        "etc_data_birds",
        "envelope",
        existing_type=sa.Text(),
        type_=sa.String(length=60),
    )

    op.alter_column(
        "etc_birds_eu_view",
        "assessment_speciesname",
        existing_type=sa.String(length=255),
        nullable=False,
    )
    op.alter_column(
        "etc_birds_eu_view",
        "ID",
        existing_type=sa.Integer(),
        nullable=True,
    )

    op.alter_column(
        "datasets", "name", existing_type=sa.String(length=255), nullable=True
    )
