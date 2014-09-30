from art12.models import EtcDataBird


class SpeciesMixin(object):
    model_cls = EtcDataBird

    def get_subjects(self, dataset):
        return (
            self.model_cls.query
            .filter_by(dataset=dataset)
            .with_entities(self.model_cls.speciescode,
                           self.model_cls.speciesname)
            .distinct()
        )
