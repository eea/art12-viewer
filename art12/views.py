import json

from flask import request, url_for
from flask.views import View
from art12.common import TemplateView, generate_map_url
from art12.definitions import EU_COUNTRY
from art12.forms import (
    SummaryFilterForm, ProgressFilterForm, ReportsFilterForm,
)
from art12.mixins import SpeciesMixin
from art12.models import Dataset


class Homepage(TemplateView):
    template_name = 'homepage.html'


class Summary(SpeciesMixin, TemplateView):
    template_name = 'summary/species.html'

    def get_context_data(self, **kwargs):
        map_url = ''
        filter_form = SummaryFilterForm(request.args)
        filter_args = {}
        subject = filter_form.subject.data

        if subject:
            filter_args['speciescode'] = subject
        if filter_args:
            filter_args['dataset'] = filter_form.dataset
            period = filter_args['dataset'].id
            qs = self.model_cls.query.filter_by(**filter_args)
            content_objects = qs.filter(
                self.model_cls.country_isocode != EU_COUNTRY)
            eu_objects = qs.filter(
                self.model_cls.country_isocode == EU_COUNTRY)

            sensitive = False

            map_url = generate_map_url(
                subject=subject,
                sensitive=sensitive,
            )
        else:
            content_objects = []
            eu_objects = []
            period = 0

        url_kwargs = dict(period=period, subject=subject)

        return {
            'filter_form': filter_form,
            'objects': content_objects, 'eu_objects': eu_objects,
            'current_selection': filter_form.get_selection(),
            'dataset': filter_form.dataset,
            'subject': subject,
            'datasheet_url': url_for('wiki.datasheet', **url_kwargs),
            'audittrail_url': url_for('wiki.audittrail', **url_kwargs),
            'map_url': map_url,
        }


class Progress(SpeciesMixin, TemplateView):
    template_name = 'progress/species.html'

    def get_conclusion_qs(self, conclusion_type):
        if conclusion_type == 'bs':
            field = self.model_cls.conclusion_population_bs
        elif conclusion_type == 'ws':
            field = self.model_cls.conclusion_population_ws
        elif conclusion_type == 'rg':
            field = self.model_cls.conclusion_range_bs
        else:
            raise ValueError('Unknown conclusion type')
        return (
            self.model_cls.query
            .filter(self.model_cls.country_isocode == EU_COUNTRY)
            .with_entities(self.model_cls.speciescode,
                           self.model_cls.speciesname, field)
            .order_by(self.model_cls.speciesname)
        )

    def get_context_data(self, **kwargs):
        filter_form = ProgressFilterForm(request.args)

        conclusion_type = filter_form.conclusion.data
        if conclusion_type:
            conclusions = self.get_conclusion_qs(conclusion_type)
        else:
            conclusions = []
        dataset = filter_form.dataset
        return {
            'filter_form': filter_form,
            'conclusions': conclusions,
            'species': self.get_subjects(dataset),
            'current_selection': filter_form.get_selection(),
            'dataset': dataset,
            }


class Reports(SpeciesMixin, TemplateView):
    template_name = 'reports/species.html'

    def get_context_data(self, **kwargs):
        filter_form = ReportsFilterForm(request.args)

        country = filter_form.country.data
        if country:
            objects = (
                self.model_cls.query
                .filter_by(country_isocode=country)
                .order_by(self.model_cls.speciesname)
            )
        else:
            objects = []

        return {
            'filter_form': filter_form,
            'current_selection': filter_form.get_selection(),
            'objects': objects,
            'dataset': filter_form.dataset,
        }


class ConnectedSelectBoxes(View, SpeciesMixin):
    methods = ['GET']

    def dispatch_request(self):
        dataset_id = request.args.get('dataset_id', 1)
        dataset = Dataset.query.get_or_404(dataset_id)
        options = [('', '-')] + self.get_subjects(dataset)
        return json.dumps(options)
