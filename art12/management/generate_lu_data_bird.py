from flask_script import Manager, Option
from flask_security.script import Command

from art12 import models


class GenerateLuDataBirdCommand(Command):

    option_list = Command.option_list + (
        Option('-i', '--id', dest='id', required=True),
    )

    def run(self, **kwargs):

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

generate_lu_data_bird = Manager()
generate_lu_data_bird.add_command('run', GenerateLuDataBirdCommand())