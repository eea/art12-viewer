from flask import request
from flask.views import MethodView
from art12.common import TemplateView
from art12.definitions import EU_COUNTRY
from art12.forms import SummaryFilterForm, ProgressFilterForm
from art12.mixins import SpeciesMixin


class Homepage(TemplateView):
    template_name = 'homepage.html'


class Summary(SpeciesMixin, TemplateView):
    template_name = 'summary/species.html'

    def get_context_data(self, **kwargs):
        filter_form = SummaryFilterForm(request.args)
        filter_args = {}
        subject = filter_form.subject.data
        if subject:
            filter_args['speciescode'] = subject
        if filter_args:
            filter_args['dataset'] = filter_form.dataset
            qs = self.model_cls.query.filter_by(**filter_args)
            content_objects = qs.filter(
                self.model_cls.country_isocode != EU_COUNTRY)
            eu_objects = qs.filter(
                self.model_cls.country_isocode == EU_COUNTRY)
        else:
            content_objects = []
            eu_objects = []
        return {
            'filter_form': filter_form,
            'objects': content_objects, 'eu_objects': eu_objects,
            'current_selection': filter_form.get_selection(),
            'dataset': filter_form.data,
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
        return {
            'filter_form': filter_form,
            'conclusions': conclusions,
            'current_selection': filter_form.get_selection(),
        }


class Report(MethodView):
    pass
