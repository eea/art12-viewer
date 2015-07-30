from flask import render_template, request, current_app as app, url_for
from flask.views import MethodView

from art12.models import db, EtcBirdsEu, EtcDataBird, Wiki, WikiChange
from art12.queries import (
    SPECIESNAME_Q, SUBUNIT_Q, ANNEX_Q, PLAN_Q, LISTS_Q, MS_TABLE_Q,
    SPA_TRIGGER_Q, PRESS_THRE_Q, N2K_Q, CONS_MEASURES_Q)


def get_arg(kwargs, key, default=None):
    arg = kwargs.get(key)
    return arg[0] if isinstance(arg, list) else arg or default


class DummyCls(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)


class BirdFactsheet(MethodView):
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

    def set_ms_birds(self, obj):
        query = MS_TABLE_Q.format(subject=self.subject, period=self.period)
        result = self.tool_engine.execute(query)
        obj.ms_birds = [DummyCls(**dict(row.items())) for row in result]

    def set_subpop_lists(self, obj):
        query = LISTS_Q.format(subject=self.subject, period=self.period)
        result = self.tool_engine.execute(query)
        d = {}
        for row in result:
            for k, v in row.items():
                d.setdefault(k, []).append(v)
        for key, val in d.iteritems():
            setattr(obj, key, val)

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
        self.engine = db.get_engine(app, 'factsheet')
        self.tool_engine = db.get_engine(app)

        bird_obj = DummyCls()
        self.set_properties(bird_obj)
        self.set_wiki(bird_obj)
        self.set_etc_birds(bird_obj)
        self.set_subpop_lists(bird_obj)
        self.set_ms_birds(bird_obj)
        bird_obj.url = url_for('views.summary',
                               period=self.period,
                               subject=self.subject,
                               _external=True)

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
        self.period = get_arg(request.args, 'period',
                              app.config['FACTSHEET_DEFAULT_PERIOD'])
        self.subject = get_arg(request.args, 'subject')

        if not self.subject:
            return self.list_all()

        context = self.get_context_data()
        return render_template('factsheet/species.html', **context)
