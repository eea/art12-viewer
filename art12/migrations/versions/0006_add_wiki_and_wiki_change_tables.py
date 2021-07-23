"""add_wiki_and_wiki_change_tables

Revision ID: 0006
Revises: 0005
Create Date: 2014-10-07 15:52:07.956349

"""
# revision identifiers, used by Alembic.
revision = '0006'
down_revision = '0005'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('wiki',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('speciescode', sa.String(length=10), nullable=False),
        sa.Column('ext_dataset_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['ext_dataset_id'], ['datasets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wiki_changes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('wiki_id', sa.Integer(), nullable=False),
        sa.Column('body', sa.String(length=6000), nullable=False),
        sa.Column('editor', sa.String(length=60), nullable=False),
        sa.Column('changed', sa.TIMESTAMP, server_default=sa.func.now(),
                  nullable=False),
        sa.Column('active', sa.Integer(), nullable=True),
        sa.Column('ext_dataset_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['ext_dataset_id'], ['datasets.id'], ),
        sa.ForeignKeyConstraint(['wiki_id'], ['wiki.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('wiki_changes')
    op.drop_table('wiki')

