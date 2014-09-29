from flask import request
from flask.views import MethodView
from art12.common import TemplateView
from art12.definitions import EU_COUNTRY
from art12.forms import SummaryFilterForm
from art12.common import get_default_period
from art12.models import EtcDataBird, Dataset


class Homepage(TemplateView):
    template_name = 'homepage.html'


class Summary(TemplateView):
    template_name = 'summary/species.html'
    model_cls = EtcDataBird

    def get_context_data(self, **kwargs):
        dataset_id = request.args.get('period') or get_default_period()
        dataset = Dataset.query.get_or_404(dataset_id)
        filter_form = SummaryFilterForm(request.args)
        filter_form.subject.choices = self.get_subjects(dataset)
        subject = request.args.get('subject')
        filter_args = {}
        current_selection = []
        if subject:
            filter_args['speciescode'] = subject
            subject_name = self.model_cls.query.filter_by(
                speciescode=subject).first().speciesname
            current_selection = [dataset.name, subject_name]
        if filter_args:
            filter_args['dataset'] = dataset
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
            'current_selection': current_selection, 'dataset': dataset,
        }

    def get_subjects(self, dataset):
        return (
            EtcDataBird.query
            .filter_by(dataset=dataset)
            .with_entities(self.model_cls.speciescode,
                           self.model_cls.speciesname)
            .distinct()
        )


class Report(MethodView):
    pass


class Progress(MethodView):
    pass

