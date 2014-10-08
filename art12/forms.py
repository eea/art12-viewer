from flask import request
from flask.ext.wtf import Form
from wtforms import SelectField, DateField, StringField
from wtforms.validators import Optional
from art12.common import get_default_period
from art12.mixins import SpeciesMixin
from art12.models import Dataset, EtcDataBird


class CommonFilterForm(Form):
    period = SelectField('Period...')
    model_cls = EtcDataBird

    def __init__(self, *args, **kwargs):
        super(CommonFilterForm, self).__init__(*args, **kwargs)
        self.period.choices = [(d.id, d.name) for d in Dataset.query.all()]
        dataset_id = request.args.get('period', get_default_period())
        self.dataset = Dataset.query.get_or_404(dataset_id)

    def get_selection(self):
        return [self.dataset.name]


class SummaryFilterForm(SpeciesMixin, CommonFilterForm):
    subject = SelectField('Name...', default='')

    def __init__(self, *args, **kwargs):
        super(SummaryFilterForm, self).__init__(*args, **kwargs)
        self.subject.choices = [('', '-')] + self.get_subjects(self.dataset)

    def get_selection(self):
        subject = self.subject.data
        if not subject:
            return []
        subject_name = self.model_cls.query.filter_by(
            speciescode=subject).first().speciesname

        return super(SummaryFilterForm, self).get_selection() + [subject_name]


class ProgressFilterForm(CommonFilterForm):
    CONCLUSION_TYPE = (
        ('', '-'),
        ('bs', 'Breeding Population'),
        ('rg', 'Breeding Range'),
        ('ws', 'Winter Population'),
    )
    conclusion = SelectField('Conclusion type...', choices=CONCLUSION_TYPE,
                             default='')

    def get_selection(self):
        conclusion = self.conclusion.data
        if not conclusion:
            return []

        conc_name = dict(self.CONCLUSION_TYPE).get(conclusion)
        return super(ProgressFilterForm, self).get_selection() + [conc_name]


class ReportsFilterForm(SpeciesMixin, CommonFilterForm):
    country = SelectField('Country...', default='')

    def __init__(self, *args, **kwargs):
        super(ReportsFilterForm, self).__init__(*args, **kwargs)
        self.country.choices = [('', '-')] + self.get_countries(self.dataset)

    def get_selection(self):
        country_name = self.country.data
        if not country_name:
            return []

        return super(ReportsFilterForm, self).get_selection() + [country_name]


class ConfigForm(Form):
    default_dataset_id = SelectField(label="Default period")

    species_map_url = StringField(label="URL for species map",
                                  validators=[Optional()])
    sensitive_species_map_url = StringField(
        label="URL for sensitive species map", validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        dataset_qs = Dataset.query.with_entities(Dataset.id, Dataset.name).all()
        self.default_dataset_id.choices = [
            (str(ds_id), name) for ds_id, name in dataset_qs
        ]

