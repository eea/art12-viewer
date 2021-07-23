from art12 import models
from flask.cli import AppGroup

import click


generate_new_period = AppGroup("generate_new_period")

@generate_new_period.command("run")
@click.option('-i', '--id', 'id')
@click.option('-n', '--name', 'name')
def run(**kwargs):
    dataset = models.Dataset.query.filter_by(id=kwargs['id']).first()
    if not dataset:
        dataset = models.Dataset(id=kwargs['id'], name=kwargs['name'])
        models.db.session.add(dataset)
        models.db.session.commit()
        print(f"Created new dataset {dataset.id}, {dataset.name}")