import csv
import sys

from flask_script import Manager, Option
from flask_security.script import Command

from art12 import models

from flask_sqlalchemy import SQLAlchemy

def get_model(self, name):
    return self.Model._decl_class_registry.get(name, None)
SQLAlchemy.get_model = get_model

class GenerateWikiTrail(Command):

    option_list = Command.option_list + (
        Option('-f', '--file', dest='file', required=True),
        Option('-i', '--id', dest='id', required=True)
    )

    def run(self, **kwargs):
        with open(kwargs['file']) as file:
            data = [{k: v for k, v in row.items()} for row in 
                    csv.DictReader(file, skipinitialspace=True)]
            for data_object in data:
                new_wiki_trail = models.WikiTrail(dataset_id=kwargs['id'],
                                                  reported_name=data_object['reported_name'],
                                                  reported_name_code=data_object['speciescode'],
                                                  speciescode=data_object['assessment_speciesname'])
                models.db.session.add(new_wiki_trail)
                models.db.session.commit()
                new_wiki_trail_change = models.WikiTrailChange(
                    body=data_object['merge'],
                    editor='Admin',
                    active=1,
                    dataset_id=kwargs['id'],
                    wiki=new_wiki_trail,
                )
                models.db.session.add(new_wiki_trail_change)
                models.db.session.commit()

generate_wiki_trail = Manager()
generate_wiki_trail.add_command('run', GenerateWikiTrail())