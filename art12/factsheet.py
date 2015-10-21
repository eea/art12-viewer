from flask import Blueprint
from flask import render_template, request, current_app as app, url_for
from flask.ext.script import Manager
from flask.views import MethodView
import jinja2

from art12.models import db, EtcBirdsEu, EtcDataBird, Wiki, WikiChange
from art12.queries import (
    SPECIESNAME_Q, SUBUNIT_Q, ANNEX_Q, PLAN_Q, MS_TABLE_Q,
    SPA_TRIGGER_Q, PRESS_THRE_Q, N2K_Q, CONS_MEASURES_Q)
from art12.pdf import PdfRenderer

factsheet_manager = Manager()
factsheet = Blueprint('factsheet', __name__)


@factsheet.app_template_filter('format_subpopulation')
def format_subpopulation(subpopulation):
    subpopulation = '<i>{}</i>'.format(subpopulation)
    return jinja2.Markup(
        subpopulation
        .replace('[', '</i>[')
        .replace(']', ']<i>')
        .replace('all others', '</i>all others<i>')
    )


def get_arg(kwargs, key, default=None):
    arg = kwargs.get(key)
    return arg[0] if isinstance(arg, list) else arg or default


class DummyCls(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)


class BirdFactsheet(MethodView):
    template_name = 'factsheet/species.html'
    property_to_query = {
        'speciesname': SPECIESNAME_Q,
        'subunit': SUBUNIT_Q,
        'annex': ANNEX_Q,
        'plan': PLAN_Q,
    }

    def list_all(self):
        objects = EtcDataBird.query.filter_by(dataset_id=self.period)
        return render_template('factsheet/list_all.html', objects=objects)

    def set_properties(self, obj):
        for prop_name, query in self.property_to_query.iteritems():
            result = self.engine.execute(query.format(code=self.subject))
            value = ', '.join([row[0] for row in result if row[0]])
            setattr(obj, prop_name, value)

    def set_wiki(self, obj):
        wiki_change = WikiChange.query.join(Wiki).filter(
            WikiChange.dataset_id == self.period,
            Wiki.speciescode == self.subject,
        ).first()
        obj.wiki = wiki_change.body if wiki_change else ''

    def set_etc_birds(self, obj):
        obj.etc_birds = EtcBirdsEu.query.filter_by(
            speciescode=self.subject,
            dataset_id=self.period,
        )

    def set_conclusion_status_levels(self, obj):
        def get_bird_values(attr):
            return [getattr(b, attr) for b in obj.etc_birds if getattr(b, attr)]

        for attr in ['conclusion_status_level1_record',
                     'conclusion_status_level2_record']:
            setattr(obj, attr, any(get_bird_values(attr)))

        for attr in ['conclusion_status_level1',
                     'conclusion_status_level2']:
            setattr(obj, attr, ', '.join(get_bird_values(attr)))

    def set_ms_birds(self, obj):
        query = MS_TABLE_Q.format(subject=self.subject, period=self.period)
        result = self.tool_engine.execute(query)
        obj.ms_birds = [DummyCls(**dict(row.items())) for row in result]

    def is_spa_trigger(self):
        query = SPA_TRIGGER_Q.format(subject=self.subject)
        result = self.engine.execute(query)
        row = result and result.first()
        return row and row['count'] > 0

    def set_list_property(self, obj, prop_name, query):
        result = self.engine.execute(query.format(subject=self.subject))
        list_obj = [DummyCls(**dict(row.items())) for row in result]
        setattr(obj, prop_name, list_obj)

    def get_context_data(self, **kwargs):
        self.period = get_arg(kwargs, 'period', app.config['DEFAULT_PERIOD'])
        self.subject = get_arg(kwargs, 'subject')

        self.engine = db.get_engine(app, 'factsheet')
        self.tool_engine = db.get_engine(app)

        bird_obj = DummyCls()
        self.set_properties(bird_obj)
        self.set_wiki(bird_obj)
        self.set_etc_birds(bird_obj)
        self.set_conclusion_status_levels(bird_obj)
        self.set_ms_birds(bird_obj)
        bird_obj.url = url_for('views.summary',
                               subject=self.subject,
                               period=self.period,
                               _external=True)
        bird_obj.code = self.subject

        if self.is_spa_trigger():
            bird_obj.is_spa_trigger = True
            spa_properties = {
                'threats': PRESS_THRE_Q,
                'n2k': N2K_Q,
                'cons_measures': CONS_MEASURES_Q,
            }
            for prop, query in spa_properties.iteritems():
                self.set_list_property(bird_obj, prop, query)

        return {'obj': bird_obj}

    def get(self):
        context = self.get_context_data(**request.args)

        if not self.subject:
            return self.list_all()

        return render_template(self.template_name, **context)

    def get_pdf(self, **kwargs):
        context = self.get_context_data(**kwargs)
        header_url = url_for('factsheet.header',
                             subject=self.subject,
                             period=self.period,
                             _external=True)
        footer_url = url_for('factsheet.footer', _external=True)
        return PdfRenderer(self.template_name, pdf_file=self.subject,
                           height='11.693in', width='8.268in',
                           context=context,
                           header_url=header_url, footer_url=footer_url)


class FactsheetHeader(MethodView):
    def get_context_data(self, **kwargs):
        subject = get_arg(kwargs, 'subject')
        period = get_arg(kwargs, 'period')

        bird = (EtcDataBird.query
                .filter_by(speciescode=subject, dataset_id=period)
                .first_or_404())

        factsheet_engine = db.get_engine(app, 'factsheet')
        result = factsheet_engine.execute(SUBUNIT_Q.format(code=subject))
        row = result and result.first()
        subunit = row and row['sub_unit']

        return {
            'period': bird.dataset.name,
            'subject': bird.speciesname,
            'subunit': subunit,
        }

    def get(self):
        context = self.get_context_data(**request.args)
        return render_template('factsheet/header.html', **context)


class FactsheetFooter(MethodView):
    def get(self):
        return render_template('factsheet/footer.html')


@factsheet_manager.command
def species(subject, period):
    fs = BirdFactsheet()
    renderer = fs.get_pdf(subject=subject, period=period)
    renderer._generate()
    print("Generated: " + renderer.pdf_path)
