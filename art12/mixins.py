from art12.definitions import EU_COUNTRY
from art12.models import EtcDataBird, LuDataBird, EtcBirdsEu


class SpeciesMixin(object):
    model_cls = EtcDataBird
    model_eu_cls = EtcBirdsEu

    def get_subjects(self, dataset):
        model = LuDataBird
        if dataset.id == 3:
            return [
                (entry.speciesname, entry.speciesname)
                for entry in (
                    model.query.filter_by(dataset=dataset)
                    .distinct()
                    .with_entities(model.speciesname, model.speciesname)
                    .order_by(model.speciesname)
                    .all()
                )
            ]
        else:
            return [
                (entry.speciescode, entry.speciesname)
                for entry in (
                    model.query.filter_by(dataset=dataset)
                    .distinct()
                    .with_entities(model.speciescode, model.speciesname)
                    .order_by(model.speciesname)
                    .all()
                )
            ]

    def get_reported_name(self, dataset, speciesname):
        model = EtcDataBird
        lu_data_bird = LuDataBird.query.filter_by(speciesname=speciesname).first()
        if not lu_data_bird:
            speciesname = ""
        else:
            speciesname = lu_data_bird.speciesname
        return [
            (entry.speciescode, entry.reported_name)
            for entry in (
                model.query.filter_by(
                    dataset=dataset, assessment_speciesname=speciesname
                )
                .with_entities(model.speciescode, model.reported_name)
                .order_by(model.reported_name)
                .distinct()
                .all()
            )
        ]

    def get_countries(self, dataset):
        if dataset.id == 2:
            return [("GR", "GR")]
        return [
            (entry.country_isocode, entry.country)
            for entry in (
                self.model_cls.query.filter_by(dataset=dataset)
                .filter(self.model_cls.country_isocode != EU_COUNTRY)
                .with_entities(self.model_cls.country_isocode, self.model_cls.country)
                .distinct()
                .order_by(self.model_cls.country)
                .all()
            )
        ]
