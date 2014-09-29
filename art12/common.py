from flask import Blueprint, url_for, render_template
from flask.views import MethodView
from art12.definitions import TREND_OPTIONS, EU_COUNTRY
from art12.utils import str2num

common = Blueprint('common', __name__)

HOMEPAGE_VIEW_NAME = 'views.homepage'


@common.app_context_processor
def inject_globals():
    make_tooltip = lambda d: '\n' + '\n'.join(
        ['%s: %s' % (k, v) for k, v in d])

    return {
        'APP_BREADCRUMBS': [('Article 17', url_for(HOMEPAGE_VIEW_NAME))],
        'EU_COUNTRY': EU_COUNTRY,
        'TREND_TOOLTIP': make_tooltip(TREND_OPTIONS),
        'population_size_unit': population_size_unit,
    }


class TemplateView(MethodView):
    def get_context_data(self, **kwargs):
        return kwargs

    def get(self):
        return render_template(self.template_name,
                               **self.get_context_data())


def get_default_period():
    return 1  # FIXME


def population_size_unit(season):
    min_size = season['population_minimum_size'] or ''
    max_size = season['population_maximum_size'] or ''
    filled = season['filled_population'] or 'N/A'
    size_unit = season['population_size_unit'] or 'N/A'

    if filled == 'Min':
        min_size = '(%s)' % min_size
    if filled == 'Max':
        max_size = '(%s)' % max_size

    if min_size or max_size:
        size_unit_value = '%s - %s' % (min_size, max_size)
    else:
        size_unit_value = 'N/A'

    return '%s %s' % (str2num(size_unit_value), size_unit)
