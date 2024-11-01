from datetime import datetime, UTC
import flask
import flask_security.utils
import flask_security as flask_security
from flask_login import current_user as c_user
from flask_security import user_registered
from flask_security import SQLAlchemyUserDatastore
from flask_security.core import AnonymousUser as BaseAnonymousUser
from flask_login import LoginManager
from werkzeug.local import LocalProxy
from wtforms import ValidationError
from .auth import auth

login_manager = LoginManager()

# current_user = LocalProxy(lambda: flask.g.get('user') or AnonymousUser())
# current_user = LocalProxy(
#     lambda: AnonymousUser() if not hasattr(c_user, "id") else c_user
# )


class AnonymousUser(BaseAnonymousUser):
    id = None


current_user = LocalProxy(
    lambda: AnonymousUser() if not c_user.is_authenticated else c_user
)

# current_user = LocalProxy(lambda: _get_user())
flask_security.core.current_user = current_user
flask_security.core.AnonymousUser = AnonymousUser
flask_security.forms.current_user = current_user
flask_security.decorators.current_user = current_user
flask_security.views.current_user = current_user
flask_security.views.logout_user = lambda: None
flask_security.views.login_user = lambda new_user, authn_via: None
flask_security.views.register = flask_security.views.register
flask_security.core._get_login_manager = lambda app, anonymous_user: None


def encrypt_password(password):
    pwd_context = flask.current_app.extensions["security"].pwd_context
    return pwd_context.hash(password.encode("utf-8"))


def verify(password, user):
    pwd_context = flask.current_app.extensions["security"].pwd_context
    return pwd_context.verify(password, user.password)


# override encrypt_password with our simplified version
flask_security.registerable.encrypt_password = encrypt_password
flask_security.utils.encrypt_password = encrypt_password
flask_security.recoverable.encrypt_password = encrypt_password
flask_security.utils.encrypt_password = encrypt_password
flask_security.changeable.encrypt_password = encrypt_password
flask_security.forms.verify_and_update_password = verify


class UserDatastore(SQLAlchemyUserDatastore):
    def create_user(self, **kwargs):
        kwargs.setdefault("active", False)
        kwargs["account_date"] = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
        return super(UserDatastore, self).create_user(**kwargs)

    def _prepare_role_modify_args(self, role):
        if isinstance(role, str):
            role = self.find_role(role)
        return role


def check_duplicate_with_ldap(form, field):
    from .providers import get_ldap_user_info

    user = get_ldap_user_info(field.data)
    if user is not None:
        raise ValidationError("Username already exists in the EIONET database.")


def check_duplicate_with_local_db(form, field):
    user = auth.models.db.session.get(auth.models.RegisteredUser, field.data)
    if user is not None:
        raise ValidationError("Username already exists")


def custom_unique_user_email(form, field):
    obj = getattr(form, "obj", None)
    datastore = flask.current_app.extensions["security"].datastore
    check = datastore.find_user(email=field.data)

    # check for editing existing objects
    if check and getattr(obj, "id", None) != check.id:
        raise ValidationError("%s is already associated with an account" % field.data)


def no_ldap_user(form, field):
    if form.user is not None:
        if form.user.is_ldap:
            raise ValidationError(
                "Please use the password recovery " "system for Eionet accounts"
            )


def user_registered_sighandler(app, user, confirm_token):
    from .common import add_default_role

    add_default_role(user)


user_registered.connect(user_registered_sighandler)
