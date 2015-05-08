import json

from flask import request, current_app
from flask.views import View
from art12.common import (
    TemplateView, generate_map_url, generate_eu_map_breeding_url,
    generate_eu_map_winter_url, check_map_exists
)
from art12.definitions import EU_COUNTRY
from art12.forms import (
    SummaryFilterForm, ProgressFilterForm, ReportsFilterForm,
)
from art12.mixins import SpeciesMixin
from art12.models import Dataset, LuRestrictedDataBird
from eea_integration.auth.security import current_user


class Homepage(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        context.update({
            'current_user': current_user,
        })
        return context


class Summary(SpeciesMixin, TemplateView):
    template_name = 'summary/species.html'

    def get_context_data(self, **kwargs):
        map_url = ''
        map_warning = ''
        eu_map_breeding_url, eu_map_winter_url = '', ''
        filter_form = SummaryFilterForm(request.args)
        filter_args = {}
        subject = filter_form.subject.data
        dataset = filter_form.dataset

        if subject:
            filter_args['speciescode'] = subject
        if filter_args:
            filter_args['dataset'] = dataset
            qs = self.model_cls.query.filter_by(**filter_args)
            content_objects = qs.filter(
                self.model_cls.country_isocode != EU_COUNTRY)
            eu_objects = self.model_eu_cls.query.filter_by(**filter_args)

            sensitive = False
            sensitive_records = (
                LuRestrictedDataBird.query
                .filter_by(speciescode=subject, dataset=dataset, show_data=0)
                .all()
            )
            if sensitive_records:
                if current_user.is_anonymous():
                    map_warning = ', '.join(
                        [s.country for s in sensitive_records]
                    )
                else:
                    sensitive = True

            map_url = generate_map_url(
                subject=subject,
                sensitive=sensitive,
            )
            eu_map_breeding_url = generate_eu_map_breeding_url(
                subject=subject,
                sensitive=sensitive,
            )
            eu_map_winter_url = generate_eu_map_winter_url(
                subject=subject,
                sensitive=sensitive,
            )
        else:
            content_objects = []
            eu_objects = []

        return {
            'filter_form': filter_form,
            'objects': content_objects, 'eu_objects': eu_objects,
            'current_selection': filter_form.get_selection(),
            'dataset': dataset,
            'subject': subject,
            'map_url': map_url,
            'map_warning': map_warning,
            'eu_map_breeding_url': eu_map_breeding_url,
            'eu_map_winter_url': eu_map_winter_url,
        }


class Progress(SpeciesMixin, TemplateView):
    template_name = 'progress/species.html'
    TREND_LABEL = 'trend'
    STATUS_LABEL = 'status'

    def get_conclusion_qs(self, dataset, conclusion_value, status_level):
        return (
            self.model_eu_cls.query
                .filter_by(dataset=dataset)
                .filter(conclusion_value != None)
                .with_entities(self.model_eu_cls.speciescode,
                               conclusion_value,
                               status_level)
                .order_by(self.model_eu_cls.speciesname)
                .all()
        )

    def get_context_data(self, **kwargs):
        filter_form = ProgressFilterForm(request.args)

        conclusion_type = filter_form.conclusion.data
        dataset = filter_form.dataset
        status_level = self.model_eu_cls.conclusion_status_level2
        label_type = self.TREND_LABEL
        if conclusion_type:
            if conclusion_type == 'bs':
                status_level = self.model_eu_cls.conclusion_status_level1
                conclusion_value = self.model_eu_cls.conclusion_status_label
                label_type = self.STATUS_LABEL
            elif conclusion_type == 'stbp':
                conclusion_value = self.model_eu_cls.br_population_trend
            elif conclusion_type == 'ltbp':
                conclusion_value = self.model_eu_cls.br_population_trend_long
            elif conclusion_type == 'stwp':
                conclusion_value = self.model_eu_cls.wi_population_trend
            elif conclusion_type == 'ltwp':
                conclusion_value = self.model_eu_cls.wi_population_trend_long
            else:
                raise ValueError('Unknown conclusion type')
            conclusions = self.get_conclusion_qs(dataset,
                                                 conclusion_value,
                                                 status_level)
        else:
            conclusions = []

        return {
            'filter_form': filter_form,
            'conclusions': dict((c[0], c[1]) for c in conclusions),
            'titles': dict((c[0], c[2]) for c in conclusions if c[2] != None),
            'species': self.get_subjects(dataset),
            'current_selection': filter_form.get_selection(),
            'dataset': dataset,
            'label_type': label_type,
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


class EuMap(TemplateView):
    template_name = 'summary/eu_map.html'

    def get_context_data(self, **kwargs):
        speciescode = request.args['speciescode']
        suffix = request.args['suffix']
        map_exists = check_map_exists(speciescode, suffix)

        return {
            'speciescode': speciescode,
            'suffix': suffix,
            'MAPS_URI': current_app.config['MAPS_URI'],
            'map_exists': map_exists,
        }
