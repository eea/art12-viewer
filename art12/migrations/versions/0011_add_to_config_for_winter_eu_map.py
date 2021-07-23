"""add to Config for winter eu map

Revision ID: 0011
Revises: 0010
Create Date: 2014-10-24 15:15:17.055466

"""

revision = '0011'
down_revision = '0010'

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
