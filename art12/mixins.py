from art12.definitions import EU_COUNTRY
from art12.models import EtcDataBird, LuDataBird, EtcBirdsEu


class SpeciesMixin(object):
    model_cls = EtcDataBird
    model_eu_cls = EtcBirdsEu

    def get_subjects(self, dataset):
        model = LuDataBird
        cols = (
            (model.speciesname, model.speciesname)
            if dataset.id in [3, 4]
            else (model.speciescode, model.speciesname)
        )
        order_field = model.speciesname
        entries = (
            model.query.filter_by(dataset=dataset)
            .distinct()
            .with_entities(*cols)
            .order_by(order_field)
            .all()
        )
        return [(a, b) for a, b in entries]

    def get_reported_name(self, dataset, speciesname):
        model = EtcDataBird
        lu_data_bird = LuDataBird.query.filter_by(speciesname=speciesname).first()
        speciesname = getattr(lu_data_bird, "speciesname", "")

        if dataset.id == 4:
            sub_species_field = model.speciesname
            sub_species_column_name = "speciesname"
        else:
            sub_species_field = model.reported_name
            sub_species_column_name = "reported_name"

        return [
            (entry.speciescode, getattr(entry, sub_species_column_name))
            for entry in (
                model.query.filter_by(
                    dataset=dataset, assessment_speciesname=speciesname
                )
                .with_entities(model.speciescode, sub_species_field)
                .order_by(sub_species_field)
                .distinct()
                .all()
            )
        ]

    def get_countries(self, dataset):
        if dataset.id == 2:
            return [("GR", "GR")]

        if dataset.id == 4:
            field = self.model_cls.country
            field_name = "country"
        else:
            field = self.model_cls.country_isocode
            field_name = "country_isocode"

        return [
            (getattr(entry, field_name), entry.country)
            for entry in (
                self.model_cls.query.filter_by(dataset=dataset)
                .filter(field != EU_COUNTRY)
                .with_entities(self.model_cls.country, field)
                .distinct()
                .order_by(self.model_cls.country)
                .all()
            )
        ]
