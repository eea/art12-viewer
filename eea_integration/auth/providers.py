import logging
import ldap
import requests
import flask
from eea.usersdb import UsersDB, UserNotFound
from .security import current_user
from . import auth

logger = logging.getLogger(__name__)


def set_user(user_id, is_ldap_user=False):
    user = auth.models.RegisteredUser.query.get(user_id)
    flask.g.user_credentials = {
        'user_id': user_id,
        'is_ldap_user': is_ldap_user,
    }
    if user is None:
        logger.warn("Autheticated user %r not found in database", user_id)
    elif user.is_ldap != is_ldap_user:
        logger.warn(
            "Mix-up between LDAP and non-LDAP users: "
            "Zope says %r, database says %r",
            is_ldap_user, user.is_ldap,
        )
    else:
        if user.is_active():
            flask.g.user = user
        else:
            logger.warn("User %r is marked as inactive", user_id)


class DebugAuthProvider(object):

    def init_app(self, app):
        app.before_request(self.before_request_handler)
        app.add_url_rule(
            '/auth/debug',
            endpoint='auth.debug',
            methods=['GET', 'POST'],
            view_func=self.view,
        )
        app.context_processor(lambda: {
            'art17_auth_debug': True,
        })

    def before_request_handler(self):
        auth_data = flask.session.get('auth')
        if auth_data and auth_data.get('user_id'):
            set_user(user_id=auth_data['user_id'])

    def view(self):
        auth_debug_allowed = bool(flask.current_app.config.get('AUTH_DEBUG'))
        if flask.request.method == 'POST':
            if not auth_debug_allowed:
                flask.abort(403)
            user_id = flask.request.form['user_id']
            if user_id:
                flask.session['auth'] = {'user_id': user_id}
            else:
                flask.session.pop('auth', None)
            return flask.redirect(flask.url_for('.debug'))

        return flask.render_template('auth/debug.html', **{
            'user_id': current_user.get_id(),
            'auth_debug_allowed': auth_debug_allowed,
        })


class ZopeAuthProvider(object):

    def init_app(self, app):
        self.whoami_url = app.config['AUTH_ZOPE_WHOAMI_URL']
        app.before_request(self.before_request_handler)
        app.context_processor(lambda: {
            'art17_auth_zope': True,
        })

    def before_request_handler(self):
        auth_cookie = flask.request.cookies.get('__ac')
        resp = requests.get(
            self.whoami_url,
            cookies={'__ac': auth_cookie},
            verify=False
        )
        resp_data = resp.json()
        if resp_data['user_id']:
            set_user(
                user_id=resp_data['user_id'],
                is_ldap_user=resp_data['is_ldap_user'],
            )


def _get_initial_ldap_data(user_id):
    ldap_user_info = get_ldap_user_info(user_id)
    if ldap_user_info is None:
        return None
    return {
        'name': ldap_user_info.get('full_name'),
        'institution': ldap_user_info.get('organisation'),
        'qualification': ldap_user_info.get('job_title'),
        'email': ldap_user_info.get('email'),
    }


def get_ldap_user_info(user_id):
    ldap_server = flask.current_app.config.get('EEA_LDAP_SERVER', '')
    users_db = UsersDB(ldap_server=ldap_server)
    try:
        return users_db.user_info(user_id)
    except UserNotFound:
        return None
    except ldap.INVALID_DN_SYNTAX:
        return None
