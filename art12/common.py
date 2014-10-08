from flask import (
    Blueprint, url_for, render_template, flash, redirect, request,
)
from flask.views import MethodView
from art12.definitions import TREND_OPTIONS, EU_COUNTRY, TREND_CLASSES
from art12.utils import str2num
from art12.models import Config, db

common = Blueprint('common', __name__)

HOMEPAGE_VIEW_NAME = 'views.homepage'

EMPTY = ''


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
        'get_conclusion': get_conclusion,
        }


class TemplateView(MethodView):
    def get_context_data(self, **kwargs):
        return kwargs

    def get(self):
        return render_template(self.template_name,
                               **self.get_context_data())


def get_default_period():
    return 1  # FIXME


def _double_na(field1, field2):
    return True if (field1, field2) == (EMPTY, EMPTY) else False


def population_size_unit(season):
    min_size = season['population_minimum_size'] or ''
    max_size = season['population_maximum_size'] or ''
    filled = season['filled_population'] or EMPTY
    size_unit = season['population_size_unit'] or EMPTY

    if filled == 'Min':
        min_size = '(%s)' % min_size
    if filled == 'Max':
        max_size = '(%s)' % max_size

    if min_size and max_size:
        size_unit_value = '%s - %s' % (min_size, max_size)
    elif min_size:
        size_unit_value = '%s' % min_size
    elif max_size:
        size_unit_value = '%s' % max_size
    else:
        size_unit_value = EMPTY

    return EMPTY if _double_na(size_unit_value, size_unit) \
        else '%s %s' % (str2num(size_unit_value), size_unit)


def population_trend(season):
    min_size = season['population_trend_magnitude_min'] or ''
    max_size = season['population_trend_magnitude_max'] or ''
    trend = season['population_trend'] or EMPTY

    if trend in list(set(TREND_CLASSES.keys()) - {'+', '-'}):
        return trend

    if min_size or max_size:
        trend_values = '(%s - %s)' % (str2num(min_size), str2num(max_size))
    else:
        trend_values = EMPTY

    return EMPTY if _double_na(trend, trend_values) \
        else '%s %s' % (trend, trend_values)


def population_trend_long(season):
    min_size = season['population_trend_long_magnitude_min'] or ''
    max_size = season['population_trend_long_magnitude_max'] or ''
    trend = season['population_trend_long'] or EMPTY

    if trend in list(set(TREND_CLASSES.keys()) - {'+', '-'}):
        return trend

    if min_size or max_size:
        trend_values = '(%s - %s)' % (str2num(min_size), str2num(max_size))
    else:
        trend_values = EMPTY

    return EMPTY if _double_na(trend, trend_values) \
        else '%s %s' % (trend, trend_values)


def range_trend(range_trend_bs, range_trend_magnitude_min_bs,
                range_trend_magnitude_max_bs):
    mag_min = range_trend_magnitude_min_bs
    mag_max = range_trend_magnitude_max_bs
    trend = range_trend_bs or EMPTY

    if trend in list(set(TREND_CLASSES.keys()) - {'+', '-'}):
        return trend

    if mag_min or mag_max:
        magnitude_values = '(%s - %s)' % (str2num(mag_min), str2num(mag_max))
    else:
        magnitude_values = EMPTY

    return EMPTY if _double_na(trend, magnitude_values) \
        else '%s %s' % (trend, magnitude_values)


def range_trend_long(range_trend_long_bs, range_trend_long_magnitude_min_bs,
                     range_trend_long_magnitude_max_bs):
    mag_min = range_trend_long_magnitude_min_bs
    mag_max = range_trend_long_magnitude_max_bs
    trend_long = range_trend_long_bs or EMPTY

    if trend_long in list(set(TREND_CLASSES.keys()) - {'+', '-'}):
        return trend_long

    if mag_min or mag_max:
        magnitude_values = '(%s - %s)' % (str2num(mag_min), str2num(mag_max))
    else:
        magnitude_values = EMPTY

    return EMPTY if _double_na(trend_long, magnitude_values) \
        else '%s %s' % (trend_long, magnitude_values)


def get_conclusion(conclusions, species_code):
    if not conclusions:
        return None
    for conclusion in conclusions:
        if conclusion.code == species_code:
            return conclusion[2]
    return None


def get_config():
    rows = Config.query.all()
    if len(rows) != 1:
        raise RuntimeError("There should be exactly one config row")
    return rows[0]


def generate_map_url(subject, sensitive=False):
    config = get_config()

    if sensitive:
        map_href = config.sensitive_species_map_url
    else:
        map_href = config.species_map_url

    if not map_href:
        return ''

    return map_href + '&CCode=' + subject


@common.route('/config', methods=['GET', 'POST'])
def config():
    from art12.forms import ConfigForm
    ### TO DO
    ### admin_perm.test()
    row = get_config()

    form = ConfigForm(request.form, row)
    if form.validate_on_submit():
        form.populate_obj(row)
        db.session.commit()
        return redirect(url_for('.config'))

    return render_template('config.html', form=form)
