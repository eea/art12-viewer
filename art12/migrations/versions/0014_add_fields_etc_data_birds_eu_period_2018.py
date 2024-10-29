from alembic import op
import sqlalchemy as sa

"""add_fields_etc_data_birds_eu_period_2018

Revision ID: 0014
Revises: 0013
Create Date: 2020-04-03 12:45:16.506572

"""

# revision identifiers, used by Alembic.
revision = "0014"
down_revision = "0013"


def upgrade():
    op.add_column(
        "etc_birds_eu_view",
        sa.Column("assessment_speciescode", sa.String(length=10), nullable=True),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "non_native",
        existing_type=sa.String(length=8),
        type_=sa.String(length=20),
    )
    op.add_column(
        "etc_birds_eu_view",
        sa.Column("br_distribution_surface_area", sa.Integer(), nullable=True),
    )
    op.add_column(
        "etc_birds_eu_view",
        sa.Column("br_distribution_trend", sa.String(length=3), nullable=True),
    )
    op.add_column(
        "etc_birds_eu_view",
        sa.Column("br_distribution_trend_long", sa.String(length=3), nullable=True),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "br_population_size_unit",
        existing_type=sa.String(length=10),
        type_=sa.String(length=20),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "wi_population_size",
        existing_type=sa.String(length=35),
        type_=sa.String(length=255),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "wi_population_size_unit",
        existing_type=sa.String(length=10),
        type_=sa.String(length=20),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_status_label",
        existing_type=sa.String(length=25),
        type_=sa.String(length=50),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_status_improving",
        existing_type=sa.String(length=4),
        type_=sa.String(length=50),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_status_br_wi",
        existing_type=sa.String(length=3),
        type_=sa.String(length=20),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_status_level1_record",
        existing_type=sa.String(length=1),
        type_=sa.String(length=20),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_status_level2_record",
        existing_type=sa.String(length=1),
        type_=sa.String(length=20),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_population_size_unit",
        existing_type=sa.String(length=10),
        type_=sa.String(length=20),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_population_trend",
        existing_type=sa.String(length=25),
        type_=sa.String(length=30),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_population_trend_long",
        existing_type=sa.String(length=25),
        type_=sa.String(length=30),
    )
    op.add_column(
        "etc_birds_eu_view",
        sa.Column("conclusion_status_label_prev", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "etc_birds_eu_view",
        sa.Column("conclusion_status_br_wi_prev", sa.String(length=20), nullable=True),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "contribution_target1",
        existing_type=sa.String(length=3),
        type_=sa.String(length=20),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "contribution_target1_label",
        existing_type=sa.String(length=25),
        type_=sa.String(length=30),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "last_update",
        existing_type=sa.String(length=16),
        type_=sa.String(length=20),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "decision",
        existing_type=sa.String(length=3),
        type_=sa.String(length=20),
    )
    op.add_column(
        "etc_birds_eu_view", sa.Column("use_for_statistics", sa.Text(), nullable=True)
    )


def downgrade():
    op.drop_column("etc_birds_eu_view", "use_for_statistics")
    op.alter_column(
        "etc_birds_eu_view",
        "decision",
        existing_type=sa.String(length=20),
        type_=sa.String(length=3),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "last_update",
        existing_type=sa.String(length=20),
        type_=sa.String(length=16),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "contribution_target1_label",
        existing_type=sa.String(length=30),
        type_=sa.String(length=25),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "contribution_target1",
        existing_type=sa.String(length=20),
        type_=sa.String(length=3),
    )
    op.drop_column("etc_birds_eu_view", "conclusion_status_label_prev")
    op.drop_column("etc_birds_eu_view", "conclusion_status_br_wi_prev")
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_population_trend_long",
        existing_type=sa.String(length=30),
        type_=sa.String(length=25),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_population_trend",
        existing_type=sa.String(length=30),
        type_=sa.String(length=25),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_population_size_unit",
        existing_type=sa.String(length=20),
        type_=sa.String(length=10),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_status_level2_record",
        existing_type=sa.String(length=20),
        type_=sa.String(length=1),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_status_level1_record",
        existing_type=sa.String(length=20),
        type_=sa.String(length=1),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_status_br_wi",
        existing_type=sa.String(length=20),
        type_=sa.String(length=3),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_status_improving",
        existing_type=sa.String(length=50),
        type_=sa.String(length=4),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "conclusion_status_label",
        existing_type=sa.String(length=50),
        type_=sa.String(length=25),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "wi_population_size_unit",
        existing_type=sa.String(length=20),
        type_=sa.String(length=10),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "wi_population_size",
        existing_type=sa.String(length=255),
        type_=sa.String(length=35),
    )
    op.alter_column(
        "etc_birds_eu_view",
        "br_population_size_unit",
        existing_type=sa.String(length=20),
        type_=sa.String(length=10),
    )
    op.drop_column("etc_birds_eu_view", "br_distribution_trend_long")
    op.drop_column("etc_birds_eu_view", "br_distribution_trend")
    op.drop_column("etc_birds_eu_view", "br_distribution_surface_area")
    op.alter_column(
        "etc_birds_eu_view",
        "non_native",
        existing_type=sa.String(length=20),
        type_=sa.String(length=8),
    )
    op.drop_column("etc_birds_eu_view", "assessment_speciescode")
