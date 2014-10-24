"""add to Config for winter eu map

Revision ID: 54c814967b52
Revises: 43b182bdca5d
Create Date: 2014-10-24 15:15:17.055466

"""

revision = '54c814967b52'
down_revision = '43b182bdca5d'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.add_column('config', sa.Column('eu_sensitive_species_map_breeding_url',
                                      sa.String(length=255), nullable=True))
    op.add_column('config', sa.Column('eu_sensitive_species_map_winter_url',
                                      sa.String(length=255), nullable=True))
    op.add_column('config', sa.Column('eu_species_map_breeding_url',
                                      sa.String(length=255), nullable=True))
    op.add_column('config', sa.Column('eu_species_map_winter_url',
                                      sa.String(length=255), nullable=True))
    op.drop_column('config', 'eu_sensitive_species_map_url')
    op.drop_column('config', 'eu_species_map_url')


def downgrade():
    op.add_column('config', sa.Column('eu_species_map_url',
                                      mysql.VARCHAR(length=255), nullable=True))
    op.add_column('config', sa.Column('eu_sensitive_species_map_url',
                                      mysql.VARCHAR(length=255), nullable=True))
    op.drop_column('config', 'eu_species_map_winter_url')
    op.drop_column('config', 'eu_species_map_breeding_url')
    op.drop_column('config', 'eu_sensitive_species_map_winter_url')
    op.drop_column('config', 'eu_sensitive_species_map_breeding_url')
