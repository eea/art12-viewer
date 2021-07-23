from factory.alchemy import SQLAlchemyModelFactory

from art12 import models

DATE_FORMAT = '%Y-%m-%d'


class DatasetFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Dataset
        sqlalchemy_session = models.db.session

    id = 1
    name = 'import-from-2006'


