import csv
import click

from art12 import models

from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy


def get_model(self, name):
    return self.Model._decl_class_registry.get(name, None)


SQLAlchemy.get_model = get_model


import_new_data = AppGroup("import_new_data")


@import_new_data.command("run")
@click.option("-f", "--file", "file")
@click.option("-m", "--model", "model")
def run(**kwargs):
    with open(kwargs["file"]) as file:
        data = [
            {k: v for k, v in row.items()}
            for row in csv.DictReader(file, skipinitialspace=True)
        ]
        model_class = models.db.get_model(kwargs["model"])
        for data_object in data:
            new_object = model_class(**data_object)
            models.db.session.add(new_object)
            models.db.session.commit()
