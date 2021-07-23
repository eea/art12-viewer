from art12 import models
from flask.cli import AppGroup

import click


generate_lu_data_bird = AppGroup("generate_lu_data_bird")

@generate_lu_data_bird.command("run")
@click.option('-i', '--id', 'id')
def run(**kwargs):
    dataset = models.Dataset.query.filter_by(id=kwargs['id']).first()
    etc_data_birds = models.EtcDataBird.query.filter_by(dataset=dataset)
    for etc_data_bird in etc_data_birds:
        lu_data_bird = models.LuDataBird.query.filter_by(
            speciescode=etc_data_bird.speciescode,
            speciesname=etc_data_bird.assessment_speciesname,
            dataset=dataset
        ).first()
        if not lu_data_bird:
            lu_data_bird = models.LuDataBird(
                speciescode=etc_data_bird.speciescode,
                speciesname=etc_data_bird.assessment_speciesname,
                dataset=dataset
            )
        
            models.db.session.add(lu_data_bird)
            models.db.session.commit()