from flask import render_template, request, current_app as app
from flask.views import MethodView

from art12.models import db, EtcDataBird
from art12.queries import SPECIESNAME_Q, SUBUNIT_Q, ANNEX_Q, PLAN_Q


def get_arg(kwargs, key, default=None):
    arg = kwargs.get(key)
    return arg[0] if isinstance(arg, list) else arg or default


class BirdFactsheet(MethodView):
    property_to_query = {
        'speciesname': SPECIESNAME_Q,
        'subunit': SUBUNIT_Q,
        'annex': ANNEX_Q,
        'plan': PLAN_Q,
    }

    def get_all(self):
        period = request.args.get('period', app.config['DEFAULT_PERIOD'])
        return EtcDataBird.query.filter_by(dataset_id=period)

    def list_all(self):
        objects = self.get_all()
        return render_template('factsheet/list_all.html', objects=objects)

    def set_properties(self):
        for prop_name, query in self.property_to_query.iteritems():
            result = self.engine.execute(query.format(code=self.subject))
            value = ', '.join([row[0] for row in result if row[0]])
            setattr(self, prop_name, value)

    def get_context_data(self, **kwargs):
        self.subject = get_arg(kwargs, 'subject')
        self.engine = db.get_engine(app, 'factsheet')
        self.set_properties()
        return {'obj': self}

    def get(self):
        if not request.args.get('subject'):
            return self.list_all()
        context = self.get_context_data(**request.args)
        return render_template('factsheet/species.html', **context)
