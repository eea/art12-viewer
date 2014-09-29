from flask.ext.wtf import Form
from wtforms import SelectField
from art12.models import Dataset


class CommonFilterForm(Form):
    period = SelectField('Period...')

    def __init__(self, *args, **kwargs):
        super(CommonFilterForm, self).__init__(*args, **kwargs)
        self.period.choices = [(d.id, d.name) for d in Dataset.query.all()]


class SummaryFilterForm(CommonFilterForm):
    subject = SelectField('Name...')
