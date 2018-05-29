from flask.ext.script import Manager, Option
from flask.ext.security.script import (
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
            if data.dataset_id == 2
        ]
        species = [
            data.speciesname for data in models.EtcDataBird.query.filter_by(
                country_isocode='GR').filter_by(dataset_id=2)
        ]

        for speciescode in speciescodes:
            ludatabird = models.LuDataBird.query.filter_by(
                speciescode=speciescode,
                dataset_id=2
            ).first()
            if ludatabird:
                if ludatabird.speciesname not in species:
                    models.db.session.delete(ludatabird)
            models.db.session.commit()


import_greece = Manager()
import_greece.add_command('run', ImportGreeceCommand())
