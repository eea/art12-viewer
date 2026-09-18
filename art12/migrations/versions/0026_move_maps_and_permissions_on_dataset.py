"""Move maps and permissions on dataset

Revision ID: 0026
Revises: 0025
Create Date: 2026-07-10 15:54:27.163838

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0026"
down_revision = "0025"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("config", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("default_public_dataset_id", sa.BigInteger(), nullable=True)
        )
        batch_op.drop_column("eu_species_map_winter_url")
        batch_op.drop_column("sensitive_species_map_url")
        batch_op.drop_column("eu_sensitive_species_map_breeding_url")
        batch_op.drop_column("eu_sensitive_species_map_winter_url")
        batch_op.drop_column("eu_species_map_breeding_url")
        batch_op.drop_column("species_map_url")

    with op.batch_alter_table("datasets", schema=None) as batch_op:
        batch_op.add_column(sa.Column("latest", sa.Boolean(), nullable=True))
        batch_op.add_column(
            sa.Column("public_can_view_assessments", sa.Boolean(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("species_map_url", sa.String(length=255), nullable=True)
        )
        batch_op.add_column(
            sa.Column("sensitive_species_map_url", sa.String(length=255), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "eu_species_map_breeding_url", sa.String(length=255), nullable=True
            )
        )
        batch_op.add_column(
            sa.Column(
                "eu_sensitive_species_map_breeding_url",
                sa.String(length=255),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column("eu_species_map_winter_url", sa.String(length=255), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "eu_sensitive_species_map_winter_url",
                sa.String(length=255),
                nullable=True,
            )
        )


def downgrade():

    with op.batch_alter_table("datasets", schema=None) as batch_op:
        batch_op.drop_column("eu_sensitive_species_map_winter_url")
        batch_op.drop_column("eu_species_map_winter_url")
        batch_op.drop_column("eu_sensitive_species_map_breeding_url")
        batch_op.drop_column("eu_species_map_breeding_url")
        batch_op.drop_column("sensitive_species_map_url")
        batch_op.drop_column("species_map_url")
        batch_op.drop_column("public_can_view_assessments")
        batch_op.drop_column("latest")

    with op.batch_alter_table("config", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "species_map_url",
                sa.VARCHAR(length=255),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "eu_species_map_breeding_url",
                sa.VARCHAR(length=255),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "eu_sensitive_species_map_winter_url",
                sa.VARCHAR(length=255),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "eu_sensitive_species_map_breeding_url",
                sa.VARCHAR(length=255),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "sensitive_species_map_url",
                sa.VARCHAR(length=255),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "eu_species_map_winter_url",
                sa.VARCHAR(length=255),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.drop_column("default_public_dataset_id")
