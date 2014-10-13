"""add_columns_for_eu_map_urls

Revision ID: 43b182bdca5d
Revises: 227c20797e6c
Create Date: 2014-10-13 12:45:09.922799

"""

# revision identifiers, used by Alembic.
revision = '43b182bdca5d'
down_revision = '227c20797e6c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('config', sa.Column('eu_sensitive_species_map_url',
                                      sa.String(length=255), nullable=True))
    op.add_column('config', sa.Column('eu_species_map_url',
                                      sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('config', 'eu_species_map_url')
    op.drop_column('config', 'eu_sensitive_species_map_url')
