from art12.definitions import EU_COUNTRY
from art12.models import EtcDataBird, LuDataBird, EtcBirdsEu


class SpeciesMixin(object):
    model_cls = EtcDataBird
    model_eu_cls = EtcBirdsEu

    def get_subjects(self, dataset):
        model = LuDataBird
        if dataset.id == 3:
            result = (
                model.query.filter_by(dataset=dataset).distinct()
                .with_entities(model.speciesname, model.speciesname)
                .order_by(model.speciesname)
                .all()
            )
            return result
        return (
            model.query
            .filter_by(dataset=dataset)
            .with_entities(model.speciescode, model.speciesname)
            .order_by(model.speciesname)
            .all()
        )

        return result

    def get_reported_name(self, dataset, speciesname):
        model = EtcDataBird
        lu_data_bird = LuDataBird.query.filter_by(speciesname=speciesname).first()
        if not lu_data_bird:
            speciesname = ''
        else:
            speciesname = lu_data_bird.speciesname
        etc_data_bird_results = (
            model.query
            .filter_by(dataset=dataset, assessment_speciesname=speciesname)
            .filter(model.reported_name!='')
            .with_entities(model.speciescode, model.reported_name)
            .order_by(model.reported_name).distinct()
            .all()
        )
        etc_birds_eu_results = (
            EtcBirdsEu.query
            .filter_by(dataset=dataset, assessment_speciesname=speciesname)
            .filter(EtcBirdsEu.reported_name!='')
            .with_entities(EtcBirdsEu.speciescode, EtcBirdsEu.reported_name)
            .order_by(EtcBirdsEu.reported_name).distinct()
            .all()
        )
        return list(set(etc_data_bird_results + etc_birds_eu_results))

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
