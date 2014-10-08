"""auth

Revision ID: 24a37d870923
Revises: 31ed56cad45a
Create Date: 2014-10-08 14:15:12.614723

"""
revision = '24a37d870923'
down_revision = '31ed56cad45a'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.create_table('registered_users',
        sa.Column('user', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('institution', sa.String(length=45), nullable=True),
        sa.Column('abbrev', sa.String(length=10), nullable=True),
        sa.Column('MS', sa.String(length=255), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('qualification', sa.String(length=255), nullable=True),
        sa.Column('account_date', sa.String(length=16), nullable=False),
        sa.Column('show_assessment', sa.Integer(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('confirmed_at', sa.DateTime(), nullable=True),
        sa.Column('is_ldap', sa.Boolean(), nullable=False),
        sa.Column('password', sa.String(length=60), nullable=True),
        sa.PrimaryKeyConstraint('user')
    )
    op.create_table('roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('description'),
        sa.UniqueConstraint('name')
    )
    op.create_table('roles_users',
        sa.Column('registered_users_user', sa.String(length=50), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['registered_users_user'], ['registered_users.user'], ),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], )
    )


def downgrade():
    op.drop_table('roles_users')
    op.drop_table('roles')
    op.drop_table('registered_users')
