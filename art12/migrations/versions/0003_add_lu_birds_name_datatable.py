"""Add lu_birds_name datatable

Revision ID: 0003
Revises: 0002
Create Date: 2014-10-03 13:56:57.588352

"""

# revision identifiers, used by Alembic.
revision = "0003"
down_revision = "0002"

import os
from alembic import op

SQL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sql")
SCRIPT_NAME = "lu_birds_name.sql"


def upgrade():
    with open(os.path.join(SQL_DIR, SCRIPT_NAME)) as f:
        sql = f.read()
    op.execute(sql)


def downgrade():
    op.execute("DROP TABLE IF EXISTS `lu_birds_name`;")
