import click
import csv

from flask.cli import AppGroup
from art12 import models


generate_lu_data_restricted_bird = AppGroup("generate_lu_data_restricted_bird")


@generate_lu_data_restricted_bird.command("run")
@click.option("-f", "--file", "file")
def run(**kwargs):
    with open(kwargs["file"]) as file:
        data = [
            {k: v for k, v in row.items()}
            for row in csv.DictReader(file, skipinitialspace=True)
        ]
        for data_object in data:
            new_object = models.LuRestrictedDataBird(**data_object)
            models.db.session.add(new_object)
            models.db.session.commit()
