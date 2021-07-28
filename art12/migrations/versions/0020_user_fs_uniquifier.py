"""add fs_uniquifier to registered_users

Revision ID: 0020
Revises: 0019
Create Date: 2021-07-23 15:12:41.250524

"""
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = '0020'
down_revision = '0019'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('registered_users', sa.Column('fs_uniquifier', sa.String(length=64), nullable=True))

    # update existing rows with unique fs_uniquifier
    user_table = sa.Table('registered_users', sa.MetaData(), sa.Column('user', sa.Integer, primary_key=True),
                          sa.Column('fs_uniquifier', sa.String))
    conn = op.get_bind()
    for row in conn.execute(sa.select([user_table.c.user])):
        conn.execute(user_table.update().values(fs_uniquifier=uuid.uuid4().hex).where(user_table.c.user == row['user']))
    
    op.alter_column('registered_users', 'fs_uniquifier', existing_type=sa.String(length=64), nullable=False)

def downgrade():
    op.drop_column('registered_users', 'fs_uniquifier')
