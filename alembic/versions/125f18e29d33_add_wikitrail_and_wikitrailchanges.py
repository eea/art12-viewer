"""add WikiTrail and WikiTrailChanges

Revision ID: 125f18e29d33
Revises: 41385c05675a
Create Date: 2014-10-07 18:12:32.559577

"""

# revision identifiers, used by Alembic.
revision = '125f18e29d33'
down_revision = '41385c05675a'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.create_table('wiki_trail',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('speciescode', sa.String(length=10), nullable=True),
        sa.Column('ext_dataset_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['ext_dataset_id'], ['datasets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wiki_trail_changes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('wiki_id', sa.Integer(), nullable=False),
        sa.Column('body', sa.String(length=6000), nullable=False),
        sa.Column('editor', sa.String(length=60), nullable=False),
        sa.Column('changed', sa.TIMESTAMP, server_default=sa.func.now(),
                  nullable=False),
        sa.Column('active', sa.Integer(), nullable=True),
        sa.Column('ext_dataset_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['ext_dataset_id'], ['datasets.id'], ),
        sa.ForeignKeyConstraint(['wiki_id'], ['wiki_trail.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.alter_column(u'wiki', 'speciescode',
                    existing_type=mysql.VARCHAR(length=10),
                    nullable=True)


def downgrade():
    op.alter_column(u'wiki', 'speciescode',
                    existing_type=mysql.VARCHAR(length=10),
                    nullable=False)
    op.drop_table('wiki_trail_changes')
    op.drop_table('wiki_trail')
