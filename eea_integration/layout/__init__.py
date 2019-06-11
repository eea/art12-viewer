import re
import logging
import requests
import flask
from jinja2 import Markup

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

layout = flask.Blueprint('layout', __name__, template_folder='templates')



@layout.record
def set_up_layout_template(state):
    app = state.app
    plone_url = app.config.get('LAYOUT_PLONE_URL')
    if plone_url:
        app.jinja_env.globals['layout_template'] = 'layout_plone.html'
    else:
        app.jinja_env.globals['layout_template'] = 'layout_default.html'
