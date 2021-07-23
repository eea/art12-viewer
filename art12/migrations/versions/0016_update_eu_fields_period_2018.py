"""empty message

Revision ID: 0016
Revises: 0015
Create Date: 2020-05-13 10:55:19.226939

"""

# revision identifiers, used by Alembic.
revision = '0016'
down_revision = '0015'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.alter_column('etc_birds_eu_view', 'br_population_size_unit',
                    existing_type=sa.String(length=35),
                    type_=sa.String(length=225))
    op.add_column('etc_birds_eu_view', sa.Column('br_conclusion_status_label',
                                       sa.String(length=255), nullable=True))
    op.add_column('etc_birds_eu_view', sa.Column('br_contribution_target1',
                                       sa.String(length=50), nullable=True))
    op.add_column('etc_birds_eu_view', sa.Column('br_red_list_cat',
                                       sa.String(length=255), nullable=True))
    op.add_column('etc_birds_eu_view', sa.Column('wi_conclusion_status_label',
                                       sa.String(length=255), nullable=True))
    op.add_column('etc_birds_eu_view', sa.Column('wi_contribution_target1',
                                       sa.String(length=50), nullable=True))
    op.add_column('etc_birds_eu_view', sa.Column('wi_red_list_cat',
                                       sa.String(length=255), nullable=True))
    op.add_column('etc_birds_eu_view', sa.Column('red_list_cat_prev',
                                       sa.String(length=255), nullable=True))

def downgrade():
    op.drop_column('etc_birds_eu_view', 'red_list_cat_prev')
    op.drop_column('etc_birds_eu_view', 'wi_red_list_cat')
    op.drop_column('etc_birds_eu_view', 'wi_contribution_target1')
    op.drop_column('etc_birds_eu_view', 'wi_conclusion_status_label')
    op.drop_column('etc_birds_eu_view', 'br_red_list_cat')
    op.drop_column('etc_birds_eu_view', 'br_contribution_target1')
    op.drop_column('etc_birds_eu_view', 'br_conclusion_status_label')
    op.alter_column('etc_birds_eu_view', 'br_population_size_unit',
                    existing_type=sa.String(length=225),
                    type_=sa.String(length=35))
