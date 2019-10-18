from flask_script import Manager, Option
from flask_security.script import (
    CreateUserCommand as BaseCreateUserCommand
)

from art12 import models


class ImportGreeceCommand(BaseCreateUserCommand):

    option_list = BaseCreateUserCommand.option_list + (
        Option('-i', '--id', dest='id', default=None),
        Option('-l', '--ldap', dest='is_ldap', action='store_true'),
        Option('-n', '--name', dest='name'),
    )

    def run(self, **kwargs):
        speciescodes = [
            data.speciescode for data in
            models.EtcDataBird.query.all()
            if data.dataset_id == 2 and data.country_isocode == 'GR'
        ]

        for speciescode in speciescodes:
            ludatabird = models.LuDataBird.query.filter_by(
                speciescode=speciescode
            ).first()
            if not models.LuDataBird.query.filter_by(
                    speciescode=ludatabird.speciescode, dataset_id=2).all():
                new_ludatabird = models.LuDataBird(
                    speciescode=ludatabird.speciescode,
                    speciesname=ludatabird.speciesname,
                    dataset_id=2
                )
                models.db.session.add(new_ludatabird)
                models.db.session.commit()


import_greece = Manager()
import_greece.add_command('run', ImportGreeceCommand())
