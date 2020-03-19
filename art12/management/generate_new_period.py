from flask_script import Manager, Option
from flask_security.script import Command

from art12 import models


class GenerateNewPeriodCommand(Command):

    option_list = Command.option_list + (
        Option('-i', '--id', dest='id', required=True),
        Option('-n', '--name', dest='name', required=True),
    )

    def run(self, **kwargs):

        dataset = models.Dataset.query.filter_by(id=kwargs['id']).first()
        if not dataset:
            dataset = models.Dataset(id=kwargs['id'], name=kwargs['name'])
            models.db.session.add(dataset)
            models.db.session.commit()
            print("Created new dataset {} {}".format(dataset.id, dataset.name))
 

generate_new_period = Manager()
generate_new_period.add_command('run', GenerateNewPeriodCommand())
