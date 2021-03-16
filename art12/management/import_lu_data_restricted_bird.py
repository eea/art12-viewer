import csv

from flask_script import Manager, Option
from flask_security.script import Command

from art12 import models


class GenerateLuDataRestrictedBirdCommand(Command):

    option_list = Command.option_list + (
        Option('-f', '--file', dest='file', required=True),
    )


    def run(self, **kwargs):
        with open(kwargs['file']) as file:
            data = [{k: v for k, v in row.items()} for row in 
                    csv.DictReader(file, skipinitialspace=True)]
            for data_object in data:
                new_object = models.LuRestrictedDataBird(**data_object)
                models.db.session.add(new_object)
                models.db.session.commit()

generate_lu_data_restricted_bird = Manager()
generate_lu_data_restricted_bird.add_command('run', GenerateLuDataRestrictedBirdCommand())