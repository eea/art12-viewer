import flask
from flask.ext.script import Manager
from art12.assets import assets_env
from art12.models import db, db_manager
from art12.urls import views
from art12.common import common
from eea_integration.layout import layout


def create_app():
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('settings.py', silent=True)

    db.init_app(app)
    assets_env.init_app(app)
    app.register_blueprint(common)
    app.register_blueprint(views)
    app.register_blueprint(layout)

    url_prefix = app.config.get('URL_PREFIX')
    if url_prefix:
        app.wsgi_app = create_url_prefix_middleware(app.wsgi_app, url_prefix)

    if app.config.get('SENTRY_DSN'):
        from raven.contrib.flask import Sentry

        Sentry(app)

    return app


def create_url_prefix_middleware(wsgi_app, url_prefix):
    def middleware(environ, start_response):
        path_info = environ['PATH_INFO']
        if path_info.startswith(url_prefix):
            environ['PATH_INFO'] = path_info[len(url_prefix):]
            environ['SCRIPT_NAME'] += url_prefix
        return wsgi_app(environ, start_response)

    return middleware


def create_manager(app):
    manager = Manager(app)
    manager.add_command('db', db_manager)
    return manager
