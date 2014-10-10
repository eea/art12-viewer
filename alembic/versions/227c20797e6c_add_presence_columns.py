"""add_presence_columns

Revision ID: 227c20797e6c
Revises: 3d53b5906a3d
Create Date: 2014-10-10 15:50:31.567980

"""

# revision identifiers, used by Alembic.
revision = '227c20797e6c'
down_revision = '3d53b5906a3d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('etc_data_birds',
                  sa.Column('presence_bs', sa.String(length=30), nullable=True))
    op.add_column('etc_data_birds',
                  sa.Column('presence_ws', sa.String(length=30), nullable=True))


def downgrade():
    op.drop_column('etc_data_birds', 'presence_ws')
    op.drop_column('etc_data_birds', 'presence_bs')
