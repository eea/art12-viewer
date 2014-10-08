"""add Config table

Revision ID: 31ed56cad45a
Revises: 3c8e31fa45ca
Create Date: 2014-10-06 12:22:07.478672

"""

# revision identifiers, used by Alembic.
revision = '31ed56cad45a'
down_revision = '3c8e31fa45ca'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('config',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('default_dataset_id', sa.Integer(), nullable=True),
        sa.Column('species_map_url', sa.String(length=255), nullable=True),
        sa.Column('sensitive_species_map_url', sa.String(length=255),
                  nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.execute("INSERT INTO `config` (`id`, `default_dataset_id`) "
               "VALUES ('1', '1');")


def downgrade():
    op.drop_table('config')
