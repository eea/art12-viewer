"""add_fields_etc_data_birds_eu_period_2018

Revision ID: 0015
Revises: 0014
Create Date: 2020-04-03 12:45:16.506572

"""

# revision identifiers, used by Alembic.
revision = '0015'
down_revision = '0014'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():

    op.alter_column('etc_data_birds', 'envelope',
               existing_type=mysql.TEXT(),
               nullable=False)

    op.alter_column('wiki_changes', 'ext_dataset_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('wiki_trail_changes', 'body',
               existing_type=mysql.VARCHAR(length=6000),
               nullable=False)


def downgrade():
    op.alter_column('wiki_trail_changes', 'body',
               existing_type=mysql.VARCHAR(length=6000),
               nullable=True)
    op.alter_column('wiki_changes', 'ext_dataset_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)

    op.alter_column('etc_data_birds', 'envelope',
               existing_type=mysql.TEXT(),
               nullable=True)
