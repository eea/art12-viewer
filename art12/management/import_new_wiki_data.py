import csv
import click

from art12 import models

from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy


def get_model(self, name):
    return self.Model._decl_class_registry.get(name, None)


SQLAlchemy.get_model = get_model


import_new_wiki_data = AppGroup("import_new_wiki_data")


@import_new_wiki_data.command("run")
@click.option("-f", "--file", "file")
@click.option("-m", "--model", "model")
def run(**kwargs):
    with open(kwargs["file"]) as file:
        data = [
            {k: v for k, v in row.items()}
            for row in csv.DictReader(file, skipinitialspace=True)
        ]
        if kwargs["model"] == "Wiki":
            for data_object in data:
                new_object = models.Wiki(**data_object)
                models.db.session.add(new_object)
                models.db.session.commit()
        if kwargs["model"] == "WikiChanges":
            for data_object in data:
                new_object = models.WikiChange(**data_object)
                models.db.session.add(new_object)
                models.db.session.commit()
