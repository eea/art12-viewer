import flask
from flask.ext.security import Security

auth = flask.Blueprint('auth', __name__, template_folder='templates')

from .security import UserDatastore, current_user
from .providers import DebugAuthProvider, ZopeAuthProvider
from .forms import EeaForgotPasswordForm
from .common import ugly_fix


class Auth(object):
    def __init__(self, models, security_ext, homepage):
        self.models = models
        self.security_ext = security_ext
        self.homepage = homepage

    def init_app(self, app):
        if app.config.get('AUTH_DEBUG'):
            DebugAuthProvider().init_app(app)

        if app.config.get('AUTH_ZOPE'):
            ZopeAuthProvider().init_app(app)

        app.config.update({
            'SECURITY_CONFIRMABLE': True,
            'SECURITY_POST_CONFIRM_VIEW': self.homepage,
            'SECURITY_PASSWORD_HASH': 'ldap_salted_sha1',
            'SECURITY_SEND_PASSWORD_CHANGE_EMAIL': False,
            'SECURITY_EMAIL_SUBJECT_REGISTER': (
                "Please confirm your email address for "
                "the Biological Diversity website"
            ),
            'SECURITY_MSG_EMAIL_CONFIRMED': (
                ("Your email has been confirmed. You can now log in by "
                 "clicking the link at the top."),
                'success',
            ),
            'SECURITY_RECOVERABLE': True,
            'SECURITY_RESET_URL': '/auth/recover_password',
            'SECURITY_POST_LOGIN_VIEW': self.homepage,
            'SECURITY_MSG_PASSWORD_RESET': (
                "You have successfully reset your password.",
                'success',
            ),
            'SECURITY_FORGOT_PASSWORD_TEMPLATE': 'auth/forgot_password.html',
            'SECURITY_RESET_PASSWORD_TEMPLATE': 'auth/reset_password.html',
            'SECURITY_PASSWORD_SCHEMES': ['ldap_salted_sha1'],
        })
        Security.init_app(self.security_ext, app)
        security_state = app.extensions['security']
        security_state.pwd_context.update(ldap_salted_sha1__salt_size=7)
        security_state.forgot_password_form = EeaForgotPasswordForm

        app.register_blueprint(auth)
        app.jinja_env.globals['AUTH_BLUEPRINT_INSTALLED'] = True
        app.jinja_env.filters['ugly_fix'] = ugly_fix
        auth.models = self.models
        auth.HOMEPAGE = self.homepage


import eea_integration.auth.views  # make sure views get registered
