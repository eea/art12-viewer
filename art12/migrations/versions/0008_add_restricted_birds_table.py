"""add restricted birds table

Revision ID: 0008
Revises: 0007
Create Date: 2014-10-10 14:53:51.163684

"""

# revision identifiers, used by Alembic.
revision = '0008'
down_revision = '0007'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('lu_restricted_birds',
        sa.Column('speciescode', sa.String(length=10), nullable=False),
        sa.Column('country', sa.String(length=8), nullable=False),
        sa.Column('show_data', sa.SmallInteger(), nullable=False),
        sa.Column('ext_dataset_id', sa.Integer(), server_default='0',
                  nullable=False),
        sa.ForeignKeyConstraint(['ext_dataset_id'], ['datasets.id'], ),
    )


def downgrade():
    op.drop_table('lu_restricted_birds')
