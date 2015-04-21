"""eu_population

Revision ID: 2b7f93383070
Revises: 54c814967b52
Create Date: 2015-04-21 16:49:48.444859

"""
revision = '2b7f93383070'
down_revision = '54c814967b52'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('etc_birds_eu_view',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('speciescode', sa.String(length=10), server_default='', nullable=False),
    sa.Column('speciesname', sa.String(length=255), nullable=True),
    sa.Column('speciesname_subpopulation', sa.String(length=255), nullable=True),
    sa.Column('assessment_speciesname', sa.String(length=255), nullable=True),
    sa.Column('assessment_subpopulation', sa.String(length=255), nullable=True),
    sa.Column('euringcode', sa.String(length=30), nullable=True),
    sa.Column('non_native', sa.String(length=8), nullable=True),
    sa.Column('br_range_surface_area', sa.String(length=35), nullable=True),
    sa.Column('br_range_surface_area_downrounded', sa.String(length=35), nullable=True),
    sa.Column('br_range_trend', sa.String(length=25), nullable=True),
    sa.Column('br_range_trend_long', sa.String(length=25), nullable=True),
    sa.Column('br_population_size', sa.String(length=35), nullable=True),
    sa.Column('br_population_minimum_size', sa.Numeric(precision=18, scale=5), nullable=True),
    sa.Column('br_population_minimum_size_downrounded', sa.Numeric(precision=18, scale=5), nullable=True),
    sa.Column('br_population_maximum_size', sa.Numeric(precision=18, scale=5), nullable=True),
    sa.Column('br_population_maximum_size_uprounded', sa.Numeric(precision=18, scale=5), nullable=True),
    sa.Column('br_population_size_unit', sa.String(length=10), nullable=True),
    sa.Column('br_population_trend', sa.String(length=25), nullable=True),
    sa.Column('br_population_trend_long', sa.String(length=25), nullable=True),
    sa.Column('wi_population_size', sa.String(length=35), nullable=True),
    sa.Column('wi_population_minimum_size', sa.Numeric(precision=18, scale=5), nullable=True),
    sa.Column('wi_population_minimum_size_downrounded', sa.Numeric(precision=18, scale=5), nullable=True),
    sa.Column('wi_population_maximum_size', sa.Numeric(precision=18, scale=5), nullable=True),
    sa.Column('wi_population_maximum_size_uprounded', sa.Numeric(precision=18, scale=5), nullable=True),
    sa.Column('wi_population_size_unit', sa.String(length=10), nullable=True),
    sa.Column('wi_population_trend', sa.String(length=25), nullable=True),
    sa.Column('wi_population_trend_long', sa.String(length=25), nullable=True),
    sa.Column('conclusion_status_label', sa.String(length=25), nullable=True),
    sa.Column('conclusion_status_improving', sa.String(length=4), nullable=True),
    sa.Column('conclusion_status_br_wi', sa.String(length=3), nullable=True),
    sa.Column('conclusion_status_level1_record', sa.String(length=1), nullable=True),
    sa.Column('conclusion_status_level1', sa.String(length=512), nullable=True),
    sa.Column('conclusion_status_level2_record', sa.String(length=1), nullable=True),
    sa.Column('conclusion_status_level2', sa.String(length=512), nullable=True),
    sa.Column('conclusion_population_size_unit', sa.String(length=10), nullable=True),
    sa.Column('conclusion_population_minimum_size', sa.Numeric(precision=18, scale=5), nullable=True),
    sa.Column('conclusion_population_minimum_size_downrounded', sa.Numeric(precision=18, scale=5), nullable=True),
    sa.Column('conclusion_population_maximum_size', sa.Numeric(precision=18, scale=5), nullable=True),
    sa.Column('conclusion_population_maximum_size_uprounded', sa.Numeric(precision=18, scale=5), nullable=True),
    sa.Column('conclusion_population_trend', sa.String(length=25), nullable=True),
    sa.Column('conclusion_population_trend_long', sa.String(length=25), nullable=True),
    sa.Column('contribution_target1', sa.String(length=3), nullable=True),
    sa.Column('contribution_target1_label', sa.String(length=25), nullable=True),
    sa.Column('user', sa.String(length=50), nullable=True),
    sa.Column('last_update', sa.String(length=16), nullable=True),
    sa.Column('deleted_record', sa.Integer(), nullable=True),
    sa.Column('decision', sa.String(length=3), nullable=True),
    sa.Column('user_decision', sa.String(length=50), nullable=True),
    sa.Column('last_update_decision', sa.String(length=50), nullable=True),
    sa.Column('ext_dataset_id', sa.Integer(), server_default='0', nullable=False),
    sa.ForeignKeyConstraint(['ext_dataset_id'], ['datasets.id'], ),
    sa.PrimaryKeyConstraint('ID', 'ext_dataset_id')
    )


def downgrade():
    op.drop_table('etc_birds_eu_view')
