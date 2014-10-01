from flask import Blueprint, url_for, render_template
from flask.views import MethodView
from art12.definitions import TREND_OPTIONS, EU_COUNTRY, TREND_CLASSES
from art12.utils import str2num

common = Blueprint('common', __name__)

HOMEPAGE_VIEW_NAME = 'views.homepage'


@common.app_context_processor
def inject_globals():
    make_tooltip = lambda d: '\n' + '\n'.join(
        ['%s: %s' % (k, v) for k, v in d])

    return {
        'APP_BREADCRUMBS': [('Article 12', url_for(HOMEPAGE_VIEW_NAME))],
        'EU_COUNTRY': EU_COUNTRY,
        'TREND_TOOLTIP': make_tooltip(TREND_OPTIONS),
        'TREND_CLASSES': TREND_CLASSES,
        'population_size_unit': population_size_unit,
        'population_trend': population_trend,
        'population_trend_long': population_trend_long,
        'range_trend': range_trend,
        'range_trend_long': range_trend_long,
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


def population_trend(season):
    min_size = season['population_trend_magnitude_min'] or ''
    max_size = season['population_trend_magnitude_max'] or ''
    trend = season['population_trend'] or 'N/A'

    if trend in list(set(TREND_CLASSES.keys()) - {'+', '-'}):
        return trend

    if min_size or max_size:
        trend_values = '(%s - %s)' % (str2num(min_size), str2num(max_size))
    else:
        trend_values = 'N/A'

    return '%s %s' % (trend, trend_values)


def population_trend_long(season):
    min_size = season['population_trend_long_magnitude_min'] or ''
    max_size = season['population_trend_long_magnitude_max'] or ''
    trend = season['population_trend_long'] or 'N/A'

    if trend in list(set(TREND_CLASSES.keys()) - {'+', '-'}):
        return trend

    if min_size or max_size:
        trend_values = '(%s - %s)' % (str2num(min_size), str2num(max_size))
    else:
        trend_values = 'N/A'

    return '%s %s' % (trend, trend_values)


def range_trend(range_trend_bs, range_trend_magnitude_min_bs,
                range_trend_magnitude_max_bs):
    mag_min = range_trend_magnitude_min_bs
    mag_max = range_trend_magnitude_max_bs
    trend = range_trend_bs or 'N/A'

    if trend in list(set(TREND_CLASSES.keys()) - {'+', '-'}):
        return trend

    if mag_min or mag_max:
        magnitude_values = '(%s - %s)' % (str2num(mag_min), str2num(mag_max))
    else:
        magnitude_values = 'N/A'

    return '%s %s' % (trend, magnitude_values)


def range_trend_long(range_trend_long_bs, range_trend_long_magnitude_min_bs,
                     range_trend_long_magnitude_max_bs):
    mag_min = range_trend_long_magnitude_min_bs
    mag_max = range_trend_long_magnitude_max_bs
    trend_long = range_trend_long_bs or 'N/A'

    if trend_long in list(set(TREND_CLASSES.keys()) - {'+', '-'}):
        return trend_long

    if mag_min or mag_max:
        magnitude_values = '(%s - %s)' % (str2num(mag_min), str2num(mag_max))
    else:
        magnitude_values = 'N/A'

    return '%s %s' % (trend_long, magnitude_values)
