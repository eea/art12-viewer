import flask
from flask.ext.mail import Mail
from flask.ext.script import Manager
from flask.ext.security import Security
from art12.assets import assets_env
from art12 import models
from art12.models import db, db_manager
from art12.urls import views
from art12.common import common, HOMEPAGE_VIEW_NAME
from eea_integration.layout import layout
from eea_integration.auth import auth, UserDatastore, Auth

security_ext = Security(
    datastore=UserDatastore(
        models.db,
        models.RegisteredUser,
        models.Role,
    ),
)


def create_app(config={}, testing=False):
    app = flask.Flask(__name__, instance_relative_config=True)
    if testing:
        app.testing = True
    else:
        app.config.from_pyfile('settings.py', silent=True)
    app.config.update(config)

    db.init_app(app)
    assets_env.init_app(app)
    app.register_blueprint(common)
    app.register_blueprint(views)
    app.register_blueprint(layout)
    if not app.testing:
        auth_ext = Auth(models=models, security_ext=security_ext,
                        homepage=HOMEPAGE_VIEW_NAME)
        auth_ext.init_app(app)
    Mail().init_app(app)

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
