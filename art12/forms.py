from flask import request
from flask_wtf import Form
from wtforms import SelectField, StringField, TextField, PasswordField
from wtforms.validators import Optional, InputRequired
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
    subject = SelectField('Species name...', default='')
    reported_name = SelectField('Sub-specific unit...', default='')

    def __init__(self, *args, **kwargs):
        super(SummaryFilterForm, self).__init__(*args, **kwargs)
        self.subject.choices = [('', '-')] + self.get_subjects(self.dataset)
        reported_name = [('', '-')]
        reported_names = self.get_reported_name(self.dataset, self.subject.data)
        if reported_names:
            reported_name.extend(reported_names)
        self.reported_name.choices = reported_name

    def get_selection(self):
        subject = self.subject.data
        if not subject:
            return []

        choices_dict = dict(self.subject.choices)
        subject_name = choices_dict.get(subject, subject)
        reported_name = self.reported_name.data
        if reported_name:
            reported_name =dict(self.reported_name.choices).get(reported_name)
            return super(SummaryFilterForm, self).get_selection() + [subject_name] + [reported_name]
        else:
            return super(SummaryFilterForm, self).get_selection() + [subject_name]

class ProgressFilterForm(CommonFilterForm):
    CONCLUSION_TYPE = (
        ('', '-'),
        ('bs', 'Bird Status'),
        ('stbp', 'Short-term breeding population trend'),
        ('ltbp', 'Long-term breeding population trend'),
        ('stwp', 'Short-term winter population trend'),
        ('ltwp', 'Long-term winter population trend')
    )
    conclusion = SelectField('Assessment type...', choices=CONCLUSION_TYPE,
                             default='')

    def __init__(self, *args, **kwargs):
        super(ProgressFilterForm, self).__init__(*args, **kwargs)

        self.period.choices = [(d.id, d.name) for d in
                               Dataset.query.filter(Dataset.id != 2)]
        dataset_id = request.args.get('period', get_default_period())
        self.dataset = Dataset.query.get_or_404(dataset_id)

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

        choices_dict = dict(self.country.choices)
        country_name = choices_dict.get(country_name, country_name)
        return super(ReportsFilterForm, self).get_selection() + [country_name]


class ConfigForm(Form):
    default_dataset_id = SelectField(label="Default period")

    species_map_url = StringField(label="URL for species map",
                                  validators=[Optional()])
    sensitive_species_map_url = StringField(
        label="URL for sensitive species map", validators=[Optional()])
    eu_species_map_breeding_url = StringField(
        label="URL for EU species map of Breeding population trend",
        validators=[Optional()])
    eu_sensitive_species_map_breeding_url = StringField(
        label="URL for EU sensitive species map of Breeding population trend",
        validators=[Optional()])
    eu_species_map_winter_url = StringField(
        label="URL for EU species map of Winter population trend",
        validators=[Optional()])
    eu_sensitive_species_map_winter_url = StringField(
        label="URL for EU sensitive species map of Winter population trend",
        validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        dataset_qs = Dataset.query.with_entities(Dataset.id, Dataset.name).all()
        self.default_dataset_id.choices = [
            (str(ds_id), name) for ds_id, name in dataset_qs
        ]


class ChangeDetailsForm(Form):
    institution = StringField(label="Institution", validators=[Optional()])
    abbrev = StringField(label="Abbreviation", validators=[Optional()])
    MS = StringField(label="MS", validators=[Optional()])
    qualification = StringField(label="Qualification", validators=[Optional()])

class LoginForm(Form):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
