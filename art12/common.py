from path import path
from urlparse import urlparse
from flask import Blueprint, url_for, render_template, redirect, request, flash
from flask import current_app as app
from flask.views import MethodView
from art12.definitions import (
    TREND_OPTIONS, EU_COUNTRY, TREND_CLASSES, TREND_OPTIONS_EU,
    CONTRIB_OPTIONS, STATUS_CLASSES,
)
from art12.utils import str2num
from art12.models import Config, db
from eea_integration.auth import current_user
from eea_integration.auth.common import admin_perm

common = Blueprint('common', __name__)

HOMEPAGE_VIEW_NAME = 'views.homepage'

EMPTY = ''


@common.app_context_processor
def inject_globals():
    make_tooltip = lambda d: '\n' + '\n'.join(
        ['%s: %s' % (k, v) for k, v in d])
    return {
        'APP_BREADCRUMBS': [
            ('Eionet', app.config['LAYOUT_PLONE_URL']),
            ('Article 12', url_for(HOMEPAGE_VIEW_NAME))
        ],
        'EU_COUNTRY': EU_COUNTRY,
        'TREND_TOOLTIP': make_tooltip(TREND_OPTIONS),
        'TREND_TOOLTIP_EU': make_tooltip(TREND_OPTIONS_EU),
        'CONTRIB_OPTIONS': make_tooltip(CONTRIB_OPTIONS)[1:],
        'TREND_CLASSES': TREND_CLASSES,
        'STATUS_CLASSES': STATUS_CLASSES,
        'population_size_unit': population_size_unit,
        'population_trend': population_trend,
        'population_trend_long': population_trend_long,
        'range_trend': range_trend,
        'range_trend_long': range_trend_long,
        'get_conclusion': get_conclusion,
        # summary functions
        'get_original_url': get_original_url,
        'get_title_for_country': get_title_for_species_country,
        'current_user': current_user,
    }


class TemplateView(MethodView):
    def get_context_data(self, **kwargs):
        return kwargs

    def get(self):
        return render_template(self.template_name,
                               **self.get_context_data())


def get_default_period():
    return 1  # FIXME


def get_zero(value):
    if value in ('', None):
        return EMPTY
    return int(0 + value)


def population_size_unit(season):
    min_size = get_zero(season['population_minimum_size'])
    max_size = get_zero(season['population_maximum_size'])
    filled = season['filled_population'] or EMPTY
    size_unit = season['population_size_unit'] or EMPTY

    if filled == 'Min':
        min_size = '(%s)' % min_size
    if filled == 'Max':
        max_size = '(%s)' % max_size

    if min_size != '' and max_size != '':
        size_unit_value = '%s - %s' % (min_size, max_size)
    elif min_size != '':
        size_unit_value = '%s' % min_size
    elif max_size != '':
        size_unit_value = '%s' % max_size
    else:
        size_unit_value = EMPTY

    return '%s %s' % (str2num(size_unit_value), size_unit)


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

    return '%s %s' % (trend, trend_values)


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

    return '%s %s' % (trend, trend_values)


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

    return '%s %s' % (trend, magnitude_values)


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

    return '%s %s' % (trend_long, magnitude_values)


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


def get_map_url(subject, sensitive=False):
    config = get_config()

    if sensitive and current_user.is_authenticated():
        map_href = config.sensitive_species_map_url
    else:
        map_href = config.species_map_url

    if not map_href:
        return ''

    return map_href + '&CCode=' + subject


def get_eu_map_breeding_url(subject, sensitive=False):
    config = get_config()

    if sensitive:
        eu_map_breeding_href = config.eu_sensitive_species_map_breeding_url
    else:
        eu_map_breeding_href = config.eu_species_map_breeding_url

    if not eu_map_breeding_href:
        return url_for('views.eu_map', speciescode=subject, suffix='breeding')

    return eu_map_breeding_href + '&CCode=' + subject


def get_eu_map_winter_url(subject, sensitive=False):
    config = get_config()

    if sensitive:
        eu_map_winter_href = config.eu_sensitive_species_map_winter_url
    else:
        eu_map_winter_href = config.eu_species_map_winter_url

    if not eu_map_winter_href:
        return url_for('views.eu_map', speciescode=subject, suffix='winter')

    return eu_map_winter_href + '&CCode=' + subject


def get_original_url(row):
    if not row.envelope:
        return ''
    CONVERTER_URL = (
        '{scheme}://{host}/Converters/run_conversion?'
        'file={path}/{filename}&conv={convertor}&source=remote#{subject}_B'
    )
    url_format = CONVERTER_URL
    info = urlparse(row.envelope)
    convertor = 343
    if row.country == 'CZ':
        convertor = 345

    return url_format.format(
        scheme=info.scheme, host=info.netloc, path=info.path,
        filename=row.filename,
        subject=row.speciescode,
        convertor=convertor,
    )


def get_title_for_species_country(row):
    s_name, s_info, s_type = '', '', ''
    if row.speciesname != row.assesment_speciesname:
        s_name = row.speciesname or row.assesment_speciesname or ''
        s_info = ''
    if row.species_type_asses == 0:
        # s_type = row.species_type_details.SpeciesType \
        #     if row.species_type_details else row.species_type
        pass
    if s_info:
        s_info = 'Information provided in the field 2.8.2: ' + s_info.replace(
            '\n', '<br/>')
    return s_name, s_info, s_type


@common.route('/config', methods=['GET', 'POST'])
def config():
    from art12.forms import ConfigForm

    admin_perm.test()
    row = get_config()

    form = ConfigForm(request.form, row)
    if form.validate_on_submit():
        form.populate_obj(row)
        db.session.commit()
        flash('Configuration updated successfully.')
        return redirect(url_for('.config'))

    return render_template('config.html', form=form)


@common.route('/auth/details', methods=['GET', 'POST'])
def change_details():
    if current_user.is_anonymous():
        flash('You need to login to access this page.')
        return redirect(url_for(HOMEPAGE_VIEW_NAME))
    else:
        from art12.forms import ChangeDetailsForm

        form = ChangeDetailsForm(request.form, current_user)
        if form.validate_on_submit():
            flash('Details updated successfully!', 'success')
            form.populate_obj(current_user)
            db.session.commit()

    return render_template('change_details.html', **{
        'form': form,
    })


@common.app_template_global('get_map_path')
def get_map_path(code, suffix):
    maps_format = app.config['MAPS_FORMAT']
    filename = maps_format.format(code=code, suffix=suffix)
    maps_path = path(app.static_folder) / app.config['MAPS_STATIC'] / filename
    if maps_path.exists():
        return path(app.config['MAPS_STATIC']) / filename
