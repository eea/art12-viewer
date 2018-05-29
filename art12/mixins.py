from art12.definitions import EU_COUNTRY
from art12.models import EtcDataBird, LuDataBird, EtcBirdsEu


class SpeciesMixin(object):
    model_cls = EtcDataBird
    model_eu_cls = EtcBirdsEu

    def get_subjects(self, dataset):
        model = LuDataBird
        return (
            model.query
            .filter_by(dataset=dataset)
            .with_entities(model.speciescode, model.speciesname)
            .order_by(model.speciesname)
            .all()
        )

    def get_countries(self, dataset):
        if dataset.id == 2:
            return [(u'GR', u'GR')]
        return (
            self.model_cls.query
            .filter_by(dataset=dataset)
            .filter(self.model_cls.country_isocode != EU_COUNTRY)
            .with_entities(self.model_cls.country_isocode,
                           self.model_cls.country)
            .distinct()
            .order_by(self.model_cls.country)
            .all()
        )
