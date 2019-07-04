from datetime import datetime

import os
import flask
from flask import current_app
from flask.ext.principal import PermissionDenied
from flask.ext.security.forms import ChangePasswordForm, ResetPasswordForm
from flask.ext.security.changeable import change_user_password
from flask.ext.security.registerable import register_user, encrypt_password
from werkzeug.datastructures import ImmutableMultiDict

from . import current_user, auth
from .forms import EeaAdminEditUserForm, \
    EeaLDAPRegisterForm, EeaLocalRegisterForm
from .providers import _get_initial_ldap_data
from .common import (
    get_roles_for_all_users,
    send_role_change_notification,
    send_welcome_email,
    require_admin,
    set_user_active,
    activate_and_notify_admin,
    add_default_role,
    admin_perm,
)


@auth.app_context_processor
def inject_variables():
    return {
        'admin_perm': admin_perm,
    }


@auth.app_errorhandler(PermissionDenied)
def handle_permission_denied(error):
    html = flask.render_template('auth/permission_denied.html')
    return flask.Response(html, status=403)


@auth.route('/auth/register/local', methods=['GET', 'POST'])
def register_local():
    form = EeaLocalRegisterForm(flask.request.form)

    if form.validate_on_submit():
        register_user(**form.to_dict())
        return flask.render_template('message.html', message="")

    return flask.render_template('auth/register_local.html', **{
        'register_user_form': form,
    })


@auth.route('/auth/create_local', methods=['GET', 'POST'])
@require_admin
def admin_create_local():
    form = EeaLocalRegisterForm(flask.request.form)

    if form.validate_on_submit():
        kwargs = form.to_dict()
        plaintext_password = kwargs['password']
        encrypted_password = encrypt_password(plaintext_password)
        datastore = flask.current_app.extensions['security'].datastore
        user = datastore.create_user(**kwargs)
        user.confirmed_at = datetime.utcnow()
        set_user_active(user, True)
        user.password = encrypted_password
        datastore.commit()
        send_welcome_email(user, plaintext_password)
        flask.flash("User %s created successfully." % kwargs['id'], 'success')
        return flask.redirect(flask.url_for('.users'))

    return flask.render_template('auth/register_local.html', **{
        'register_user_form': form,
    })


@auth.route('/auth/register/ldap', methods=['GET', 'POST'])
def register_ldap():
    user_credentials = flask.g.get('user_credentials', {})
    user_id = user_credentials.get('user_id')

    if not user_credentials.get('is_ldap_user'):
        if user_id:
            message = "You are already logged in."
            return flask.render_template('message.html', message=message)

        else:
            message = (
                'First log into your EIONET account by clicking "login" '
                'at the top of the page.'
            )
            return flask.render_template('message.html', message=message)

    if user_id and flask.g.identity.id:
        return flask.render_template('auth/register_ldap_exists.html', **{
            'admin_email': current_app.config.get('ADMIN_EMAIL'),
        })

    initial_data = _get_initial_ldap_data(user_id)
    form = EeaLDAPRegisterForm(ImmutableMultiDict(initial_data))

    if flask.request.method == 'POST':
        form = EeaLDAPRegisterForm(flask.request.form)
        form.name.data = initial_data.get('name', '')
        form.email.data = initial_data.get('email', '')
        if form.validate():
            datastore = flask.current_app.extensions['security'].datastore
            user = datastore.create_user(
                id=user_id,
                is_ldap=True,
                password='',
                confirmed_at=datetime.utcnow(),
                **form.to_dict()
            )
            datastore.commit()
            flask.flash(
                "Eionet account %s has been activated"
                % user_id,
                'success',
            )
            activate_and_notify_admin(flask._app_ctx_stack.top.app, user)
            add_default_role(user)
            return flask.render_template('auth/register_ldap_done.html')

    return flask.render_template('auth/register_ldap.html', **{
        'already_registered': flask.g.get('user') is not None,
        'user_id': user_id,
        'register_user_form': form,
    })


@auth.route('/auth/create_ldap', methods=['GET', 'POST'])
@require_admin
def admin_create_ldap():
    user_id = flask.request.form.get('user_id')

    if user_id is None:
        return flask.render_template('auth/register_ldap_enter_user_id.html')

    if auth.models.RegisteredUser.query.get(user_id) is not None:
        flask.flash('User "%s" already registered.' % user_id, 'error')
        return flask.redirect(flask.url_for('.admin_create_ldap'))

    initial_data = _get_initial_ldap_data(user_id)

    if '_fields_from_ldap' in flask.request.form:
        if initial_data is None:
            flask.flash('User "%s" not found in Eionet.' % user_id, 'error')
            return flask.redirect(flask.url_for('.admin_create_ldap'))
        form = EeaLDAPRegisterForm(ImmutableMultiDict(initial_data))
    else:
        form = EeaLDAPRegisterForm(flask.request.form)
        form.name.data = initial_data.get('name', '')
        form.email.data = initial_data.get('email') or flask.request.form['email']
        if form.validate():
            kwargs = form.to_dict()
            kwargs['id'] = user_id
            kwargs['is_ldap'] = True
            datastore = flask.current_app.extensions['security'].datastore
            user = datastore.create_user(**kwargs)
            user.confirmed_at = datetime.utcnow()
            set_user_active(user, True)
            datastore.commit()
            send_welcome_email(user)
            flask.flash(
                "User %s created successfully." % kwargs['id'],
                'success',
            )
            return flask.redirect(flask.url_for('.users'))

    return flask.render_template('auth/register_ldap.html', **{
        'user_id': user_id,
        'register_user_form': form,
    })


@auth.route('/auth/me')
def me():
    return flask.render_template('auth/me.html')


@auth.route('/auth/change_password', methods=['GET', 'POST'])
def change_password():
    HOMEPAGE_VIEW_NAME = auth.HOMEPAGE
    if current_user.is_anonymous():
        message = "You must log in before changing your password."
        return flask.render_template('message.html', message=message)

    if current_user.is_ldap:
        message = (
            'Your password can be changed only from the EIONET website '
            + '('
            + os.environ.get('EEA_PASSWORD_RESET', '')
            + ').'
        )
        return flask.render_template('message.html', message=message)

    form = ChangePasswordForm()

    if form.validate_on_submit():
        change_user_password(current_user, form.new_password.data)
        auth.models.db.session.commit()
        msg = "Your password has been changed. Please log in again."
        flask.flash(msg, 'success')
        return flask.redirect(flask.url_for(HOMEPAGE_VIEW_NAME))

    return flask.render_template('auth/change_password.html', **{
        'form': form,
    })


@auth.route('/auth/users')
@require_admin
def users():
    user_query = auth.models.RegisteredUser.query.order_by(
        auth.models.RegisteredUser.id)
    dataset = (
    auth.models.Dataset.query.order_by(auth.models.Dataset.id.desc()).first())
    # countries = (
    #     auth.models.DicCountryCode.query
    #     .with_entities(
    #         auth.models.DicCountryCode.codeEU,
    #         auth.models.DicCountryCode.name
    #     )
    #     .filter(auth.models.DicCountryCode.dataset_id == dataset.id)
    #     .distinct()
    #     .order_by(auth.models.DicCountryCode.name)
    #     .all()
    # )
    countries = []
    return flask.render_template('auth/users.html', **{
        'user_list': user_query.all(),
        'role_map': get_roles_for_all_users(),
        'countries': dict(countries),
    })


@auth.route('/auth/users/<user_id>', methods=['GET', 'POST'])
@require_admin
def admin_user(user_id):
    user = auth.models.RegisteredUser.query.get_or_404(user_id)
    current_user_roles = [r.name for r in user.roles]
    all_roles = (
        auth.models.Role.query
        .with_entities(auth.models.Role.name, auth.models.Role.description)
        .order_by(auth.models.Role.id)
        .all()
    )

    if flask.request.method == 'POST':
        if flask.request.form.get('btn') == u'delete':
            user = auth.models.RegisteredUser.query.get(user_id)
            auth.models.db.session.delete(user)
            auth.models.db.session.commit()
            flask.flash("User %s has successfully been deleted" % user_id,
                        'success')
            return flask.redirect(flask.url_for('.users'))
        else:
            user_form = EeaAdminEditUserForm(flask.request.form, obj=user)
            if user_form.validate():
                # manage status
                set_user_active(user, user_form.active.data)

                # manage roles
                datastore = flask.current_app.extensions['security'].datastore
                new_roles = flask.request.form.getlist('roles')
                expandable_roles = filter(lambda k: k not in new_roles,
                                          current_user_roles)
                for role in new_roles:
                    datastore.add_role_to_user(user_id, role)
                for role in expandable_roles:
                    datastore.remove_role_from_user(user_id, role)
                datastore.commit()

                # manage user info
                user_form.populate_obj(user)
                auth.models.db.session.commit()

                # manage role notifications
                if flask.request.form.get('notify_user', type=bool):
                    send_role_change_notification(user, new_roles)

                flask.flash("User information updated for %s" % user_id,
                            'success')
                return flask.redirect(flask.url_for('.users'))
    else:
        user_form = EeaAdminEditUserForm(obj=user)

    return flask.render_template('auth/admin_user.html', **{
        'user': user,
        'user_form': user_form,
        'current_user_roles': current_user_roles,
        'all_roles': dict(all_roles),
    })


@auth.route('/auth/users/<user_id>/reset_password', methods=['GET', 'POST'])
@require_admin
def admin_user_reset_password(user_id):
    user = auth.models.RegisteredUser.query.get_or_404(user_id)

    if user.is_ldap:
        message = 'The password can be changed only from the EIONET website '\
                  '(https://www.eionet.europa.eu/password-reset).'
        return flask.render_template('message.html', message=message)

    form = ResetPasswordForm()

    if form.validate_on_submit():
        change_user_password(user, form.password.data)
        auth.models.db.session.commit()
        msg = "Your password has been reset successfully"
        flask.flash(msg, 'success')

    return flask.render_template('auth/admin_user_reset_password.html', **{
        'user': user,
        'form': form,
    })

