import flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_security import Security
from art12.assets import assets_env
from art12 import models
from art12.definitions import TREND_CLASSES
from art12.models import db
from art12.urls import views
from art12.wiki import wiki
from art12.factsheet import factsheet
from art12.common import common, HOMEPAGE_VIEW_NAME
from art12.utils import inject_static_file
from art12.factsheet import factsheet_manager
from art12.management.import_greece import import_greece
from art12.management.generate_lu_data_bird import generate_lu_data_bird
from art12.management.generate_wiki_trail import generate_wiki_trail
from art12.management.import_new_data import import_new_data
from art12.management.generate_new_period import generate_new_period

from eea_integration.auth.script import user_manager, role_manager
from eea_integration.layout import layout
from eea_integration.auth import UserDatastore, Auth
from eea_integration.auth.security import login_manager

security_ext = Security(
    datastore=UserDatastore(
        models.db,
        models.RegisteredUser,
        models.Role,
    ),
)

DEFAULT_CONFIG = {
    "WTF_CSRF_ENABLED": False,
    "PDF_DESTINATION": ".",
    "DEFAULT_PERIOD": 3,
}


def create_app(config={}, testing=False):
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.update(DEFAULT_CONFIG)
    if testing:
        app.testing = True
        app.config.from_pyfile("test_settings.py", silent=True)
    else:
        app.config.from_pyfile("settings.py", silent=True)
    app.config.update(config)
    create_cli_commands(app)
    assets_env.init_app(app)
    migrate = Migrate()

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(common)
    app.register_blueprint(views)
    app.register_blueprint(layout)
    app.register_blueprint(wiki)
    app.register_blueprint(factsheet)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    app.add_template_global(inject_static_file)

    app.jinja_env.globals["TREND_CLASSES"] = TREND_CLASSES
    app.jinja_env.globals["SCRIPT_NAME"] = app.config.get("SCRIPT_NAME", "/article12")
    app.jinja_env.globals["EEA_PASSWORD_RESET"] = app.config.get("EEA_PASSWORD_RESET")

    if not app.testing:
        auth_ext = Auth(
            models=models, security_ext=security_ext, homepage=HOMEPAGE_VIEW_NAME
        )
        auth_ext.init_app(app)
    Mail().init_app(app)

    url_prefix = app.config.get("URL_PREFIX")
    if url_prefix:
        app.wsgi_app = create_url_prefix_middleware(app.wsgi_app, url_prefix)

    if app.config.get("SENTRY_DSN"):
        from raven.contrib.flask import Sentry

        Sentry(app)

    return app


def create_url_prefix_middleware(wsgi_app, url_prefix):
    def middleware(environ, start_response):
        path_info = environ["PATH_INFO"]
        if path_info.startswith(url_prefix):
            environ["PATH_INFO"] = path_info[len(url_prefix):]
            environ["SCRIPT_NAME"] += url_prefix
        return wsgi_app(environ, start_response)

    return middleware


def create_cli_commands(app):
    app.cli.add_command(user_manager)
    app.cli.add_command(import_greece)
    app.cli.add_command(generate_new_period)
    app.cli.add_command(import_new_data)
    app.cli.add_command(generate_lu_data_bird)
    app.cli.add_command(generate_wiki_trail)
    app.cli.add_command(role_manager)
    app.cli.add_command(factsheet_manager)
