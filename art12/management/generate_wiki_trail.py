import csv
import click

from art12 import models

from flask_sqlalchemy import SQLAlchemy
from flask.cli import AppGroup


def get_model(self, name):
    return self.Model._sa_registry._class_registry.get(name, None)


SQLAlchemy.get_model = get_model

generate_wiki_trail = AppGroup("generate_wiki_trail")


@generate_wiki_trail.command("run")
@click.option("-f", "--file", "file")
@click.option("-i", "--id", "id")
def run(**kwargs):
    with open(kwargs["file"]) as file:
        data = [
            {k: v for k, v in row.items()}
            for row in csv.DictReader(file, skipinitialspace=True)
        ]
        for data_object in data:
            new_wiki_trail = models.WikiTrail(
                dataset_id=kwargs["id"],
                reported_name=data_object["reported_name"],
                reported_name_code=data_object["speciescode"],
                speciescode=data_object["assessment_speciesname"],
            )
            models.db.session.add(new_wiki_trail)
            models.db.session.commit()
            new_wiki_trail_change = models.WikiTrailChange(
                body=data_object["merge"],
                editor="Admin",
                active=1,
                dataset_id=kwargs["id"],
                wiki=new_wiki_trail,
            )
            models.db.session.add(new_wiki_trail_change)
            models.db.session.commit()
