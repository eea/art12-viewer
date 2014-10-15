from collections import defaultdict
import logging
from functools import wraps
from smtplib import SMTPException
import flask
from flask import current_app
from flask_principal import Permission, RoleNeed
from flask.ext.security import signals as security_signals
from flask.ext.mail import Message
from . import auth, zope_acl_manager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DEFAULT_ROLE = 'stakeholder'

admin_perm = Permission(RoleNeed('admin'))


def safe_send_mail(app, msg):
    try:
        app.extensions['mail'].send(msg)
    except SMTPException:
        flask.flash(
            "The mail could not be sent to the specified email address."
            "Please contact the administrator.")


@security_signals.user_confirmed.connect
def activate_and_notify_admin(app, user, **extra):
    set_user_active(user, True)
    auth.models.db.session.commit()
    admin_email = current_app.config.get('ADMIN_EMAIL')

    if not admin_email:
        logger.warn("No admin_email is configured; not sending email")

    else:
        msg = Message(
            subject="User has registered",
            sender=app.extensions['security'].email_sender,
            recipients=admin_email.split(),
        )
        msg.body = flask.render_template(
            'auth/email_admin_new_user.txt',
            user=user,
            activation_link=flask.url_for(
                'auth.admin_user',
                user_id=user.id,
                _external=True,
            ),
        )
        safe_send_mail(app, msg)


@security_signals.password_reset.connect
def save_reset_password_in_zope(app, user, **extra):
    if user.is_active:
        zope_acl_manager.create(user)


def require_admin(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        admin_perm.test()
        return view(*args, **kwargs)

    return wrapper


def set_user_active(user, new_active):
    was_active = user.active
    user.active = new_active
    auth.models.db.session.commit()
    if not user.is_ldap:
        if was_active and not new_active:
            zope_acl_manager.delete(user)
        if new_active and not was_active:
            zope_acl_manager.create(user)


def add_default_role(user):
    datastore = flask.current_app.extensions['security'].datastore
    default_role = datastore.find_role(DEFAULT_ROLE)
    datastore.add_role_to_user(user, default_role)
    auth.models.db.session.commit()


def get_roles_for_all_users():
    roles_query = (
        auth.models.db.session.query(
            auth.models.roles_users.c.registered_users_user,
            auth.models.Role.name,
        )
        .join(
            auth.models.Role,
            auth.models.roles_users.c.role_id == auth.models.Role.id,
        )
    )

    rv = defaultdict(list)
    for user_id, role_name in roles_query:
        rv[user_id].append(role_name)
    return dict(rv)


def send_role_change_notification(user, new_roles):
    app = flask.current_app
    role_description = {row.name: row.description for row in auth.models.Role.query}
    msg = Message(
        subject="Role update on the Biological Diversity website",
        sender=app.extensions['security'].email_sender,
        recipients=[user.email],
    )
    msg.body = flask.render_template('auth/email_user_role_change.txt', **{
        'user': user,
        'new_roles': [role_description[r] for r in new_roles],
    })
    safe_send_mail(app, msg)


def send_welcome_email(user, plaintext_password=None):
    app = flask.current_app
    msg = Message(
        subject="Role update on the Biological Diversity website",
        sender=app.extensions['security'].email_sender,
        recipients=[user.email],
    )
    msg.body = flask.render_template('auth/email_user_welcome.txt', **{
        'user': user,
        'plaintext_password': plaintext_password,
        'home_url': flask.url_for(auth.HOMEPAGE, _external=True),
    })
    safe_send_mail(app, msg)


def ugly_fix(value):
    return value.replace('art12.eionet', 'bd.eionet')
