"""

Revision ID: 45e69fac91b3
Revises: None
Create Date: 2014-09-29 16:37:24.292676

"""
# revision identifiers, used by Alembic.
revision = '45e69fac91b3'
down_revision = None

import os
from alembic import op

SQL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sql')
SCRIPT_NAME = 'etc_data_birds.sql'


def upgrade():
    with open(os.path.join(SQL_DIR, SCRIPT_NAME)) as f:
        sql = f.read()
    op.execute(sql)


def downgrade():
    raise NotImplementedError("Just drop & create the database manually.")
