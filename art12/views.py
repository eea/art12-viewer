from flask import render_template
from flask.views import MethodView


class Homepage(MethodView):
    def get(self):
        return render_template('homepage.html')


class Summary(MethodView):
    pass


class Report(MethodView):
    pass


class Progress(MethodView):
    pass

