import flask
from flask_security import Security
from flask_webtest import TestApp
from pytest import fixture
from alembic import config
from path import Path
from mock import patch
from datetime import datetime
import urllib
from smart_getenv import getenv

from art12.app import create_app
from art12 import models
from art12.common import HOMEPAGE_VIEW_NAME
from eea_integration.auth import UserDatastore, Auth


if getenv("DB_PASSWORD_TEST"):
    db_pass_test = ":" + getenv("DB_PASSWORD_TEST")
else:
    db_pass_test = ""

TEST_CONFIG = {
    "SERVER_NAME": "localhost",
    "SECRET_KEY": "test",
    "ASSETS_DEBUG": True,
    "EEA_LDAP_SERVER": "test_ldap_server",
    "ADMIN_EMAIL": "admin@example.com",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "EEA_PASSWORD_RESET": "pw_reset",
    "SQLALCHEMY_DATABASE_URI": "postgresql://{}{}@{}/{}".format(
        getenv("DB_USER_TEST"),
        db_pass_test,
        getenv("DB_HOST_TEST"),
        getenv("DB_NAME_TEST"),
    ),
}

alembic_cfg_path = Path((__file__)).dirname() / ".." / "alembic.ini"
alembic_cfg = config.Config(alembic_cfg_path.abspath())


def create_generic_fixtures():
    models.db.drop_all()
    models.db.create_all()
    models.db.session.execute(
        "insert into roles(name, description) values "
        "('admin', 'Administrator'), "
        "('etc', 'European topic center'), "
        "('stakeholder', 'Stakeholder'), "
        "('nat', 'National expert')"
    )
    models.db.session.execute("insert into config(default_dataset_id) values (3)")


def create_testing_app():
    test_config = dict(TEST_CONFIG)

    app = create_app(test_config, testing=True)
    models.db.init_app(app)
    return app


@fixture
def app(request):
    app = create_testing_app()

    @app.before_request
    def set_identity():
        from flask_principal import AnonymousIdentity

        flask.g.identity = AnonymousIdentity()

    app_context = app.app_context()
    app_context.push()
    create_generic_fixtures()

    @request.addfinalizer
    def fin():
        app_context.pop()

    return app


@fixture
def client(app):
    client = TestApp(app, db=models.db, use_session_scopes=True)
    return client


@fixture
def outbox(app, request):
    outbox_ctx = app.extensions["mail"].record_messages()

    @request.addfinalizer
    def cleanup():
        outbox_ctx.__exit__(None, None, None)

    return outbox_ctx.__enter__()


@fixture
def ldap_user_info(request):
    library = {}
    ldap_patch = patch("eea_integration.auth.providers.UsersDB")
    mock = ldap_patch.start()
    mock.return_value.user_info.side_effect = library.get
    request.addfinalizer(ldap_patch.stop)
    return library


@fixture
def plone_auth(app, request):
    app.config["AUTH_PLONE"] = True
    app.config["AUTH_PLONE_WHOAMI_URL"] = "http://example.com/"
    security_ext = Security(
        datastore=UserDatastore(
            models.db,
            models.RegisteredUser,
            models.Role,
        ),
    )
    auth_ext = Auth(
        models=models, homepage=HOMEPAGE_VIEW_NAME, security_ext=security_ext
    )
    auth_ext.init_app(app)

    requests_patch = patch("eea_integration.auth.providers.requests")
    requests = requests_patch.start()
    request.addfinalizer(requests_patch.stop)

    whoami_data = {"user_id": None, "is_ldap_user": False}
    requests.get.return_value.json.return_value = whoami_data

    return whoami_data


def create_user(user_id, role_names=[], name="", institution="", ms=""):
    user = models.RegisteredUser(
        id=user_id,
        account_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
        active=True,
        name=name,
        email="%s@example.com" % user_id,
        institution=institution,
        MS=ms,
    )
    models.db.session.add(user)
    for name in role_names:
        role = models.Role.query.filter_by(name=name).first()
        user.roles.append(role)
    models.db.session.commit()

    return user


def get_request_params(request_type, request_args, post_params=None):
    request_args[0] = urllib.parse.quote(request_args[0])
    if request_type == "post":
        query_string = urllib.parse.urlencode(request_args[1])
        final_url = "?".join((request_args[0], query_string))
        request_args = [final_url, post_params]
    return request_args
