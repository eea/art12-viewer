from flask import render_template, request, current_app as app
from flask.views import MethodView

from art12.models import db, EtcBirdsEu, EtcDataBird, Wiki, WikiChange
from art12.queries import SPECIESNAME_Q, SUBUNIT_Q, ANNEX_Q, PLAN_Q


def get_arg(kwargs, key, default=None):
    arg = kwargs.get(key)
    return arg[0] if isinstance(arg, list) else arg or default


class Bird(object):
    pass


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

    def get_context_data(self, **kwargs):
        self.engine = db.get_engine(app, 'factsheet')

        bird_obj = Bird()
        self.set_properties(bird_obj)
        self.set_wiki(bird_obj)
        self.set_etc_birds(bird_obj)

        return {'obj': bird_obj}

    def get(self):
        self.period = get_arg(request.args, 'period',
                              app.config['FACTSHEET_DEFAULT_PERIOD'])
        self.subject = get_arg(request.args, 'subject')

        if not self.subject:
            return self.list_all()

        context = self.get_context_data()
        return render_template('factsheet/species.html', **context)
