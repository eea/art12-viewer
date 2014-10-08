import flask
from mock import patch
from art12 import models
from art12.common import get_config
from art12.models import db
from conftest import create_user
from eea_integration.auth.providers import set_user


def _set_config(**kwargs):
    for key in kwargs:
        setattr(get_config(), key, kwargs[key])
    db.session.commit()


def test_identity_is_set_from_zope_whoami(app, zope_auth, client):
    create_user('ze_admin', ['admin'])

    @app.route('/identity')
    def get_identity():
        identity = flask.g.identity
        return flask.jsonify(
            id=identity.id,
            provides=sorted(list(identity.provides)),
        )

    zope_auth.update({'user_id': 'ze_admin', 'is_ldap_user': False})

    identity = client.get('/identity').json
    assert identity['id'] == 'ze_admin'
    assert identity['provides'] == [['id', 'ze_admin'], ['role', 'admin']]


def test_self_registration_flow(app, zope_auth, client, outbox, ldap_user_info):
    from .factories import DatasetFactory

    _set_config(admin_email='admin@example.com')
    create_user('ze_admin', ['admin'])
    DatasetFactory()
    models.db.session.commit()

    register_page = client.get(flask.url_for('auth.register_local'))
    register_page.form['id'] = 'foo'
    register_page.form['email'] = 'foo@example.com'
    register_page.form['password'] = 'p455w4rd'
    register_page.form['name'] = 'foo me'
    register_page.form['institution'] = 'foo institution'
    result_page = register_page.form.submit()
    assert "Confirmation instructions have been sent" in result_page.text

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.email == 'foo@example.com'
    assert foo_user.confirmed_at is None
    assert not foo_user.active
    assert not foo_user.is_ldap
    assert foo_user.password.startswith('{SSHA}')

    assert len(outbox) == 1
    confirm_message = outbox.pop()
    assert 'Dear foo me,' in confirm_message.body
    assert 'foo@example.com' in confirm_message.body
    url = confirm_message.body.splitlines()[4].strip()
    assert url.startswith("http://localhost/confirm/")

    with patch('eea_integration.auth.zope_acl_manager.create') as create_in_zope:
        client.get(url)
        assert create_in_zope.call_count == 1

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.confirmed_at is not None
    assert foo_user.active

    assert len(outbox) == 1
    admin_message = outbox.pop()
    assert admin_message.recipients == ['admin@example.com']
    assert "Local user has registered" in admin_message.body
    url = admin_message.body.split()[-1]
    assert url == 'http://localhost/auth/users/foo'

    with patch('eea_integration.auth.zope_acl_manager.delete') as delete_in_zope:
        zope_auth['user_id'] = 'ze_admin'
        activation_page = client.get(url)
        activation_page.form['active'] = False
        activation_page.form.submit()
        assert delete_in_zope.call_count == 1

    foo_user = models.RegisteredUser.query.get('foo')
    assert not foo_user.active


def test_admin_creates_local(app, zope_auth, client, outbox, ldap_user_info):
    from .factories import DatasetFactory

    _set_config(admin_email='admin@example.com')
    create_user('ze_admin', ['admin'])
    zope_auth['user_id'] = 'ze_admin'
    DatasetFactory()
    models.db.session.commit()

    register_page = client.get(flask.url_for('auth.admin_create_local'))
    register_page.form['id'] = 'foo'
    register_page.form['email'] = 'foo@example.com'
    register_page.form['password'] = 'p455w4rd'
    register_page.form['name'] = 'foo me'
    register_page.form['institution'] = 'foo institution'

    with patch('eea_integration.auth.zope_acl_manager.create') as create_in_zope:
        result_page = register_page.form.submit().follow()
        assert create_in_zope.call_count == 1

    assert "User foo created successfully." in result_page

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.email == 'foo@example.com'
    assert foo_user.confirmed_at is not None
    assert foo_user.active
    assert not foo_user.is_ldap
    assert foo_user.password.startswith('{SSHA}')

    assert len(outbox) == 1
    message = outbox.pop()
    assert 'Dear foo me,' in message.body
    assert '"foo"' in message.body
    assert '"p455w4rd"' in message.body


def test_admin_creates_ldap(app, zope_auth, client, outbox, ldap_user_info):
    from .factories import DatasetFactory

    _set_config(admin_email='admin@example.com')
    create_user('ze_admin', ['admin'])
    zope_auth['user_id'] = 'ze_admin'
    DatasetFactory()
    models.db.session.commit()

    ldap_user_info['foo'] = {
        'full_name': 'foo me',
        'email': 'foo@example.com',
    }

    enter_user_id_page = client.get(flask.url_for('auth.admin_create_ldap'))
    enter_user_id_page.form['user_id'] = 'foo'
    register_page = enter_user_id_page.form.submit()

    register_page.form['institution'] = 'foo institution'

    with patch('eea_integration.auth.zope_acl_manager.create') as create_in_zope:
        result_page = register_page.form.submit().follow()
        assert create_in_zope.call_count == 0

    assert "User foo created successfully." in result_page

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.email == 'foo@example.com'
    assert foo_user.confirmed_at is not None
    assert foo_user.active
    assert foo_user.is_ldap

    assert len(outbox) == 1
    message = outbox.pop()
    assert 'Dear foo me,' in message.body
    assert '"foo"' in message.body


def test_ldap_account_activation_flow(
        app,
        zope_auth,
        client,
        outbox,
        ldap_user_info,
):
    from .factories import DatasetFactory

    _set_config(admin_email='admin@example.com')
    ldap_user_info['foo'] = {'email': 'foo@example.com', 'full_name': 'foo'}
    create_user('ze_admin', ['admin'])
    DatasetFactory()
    models.db.session.commit()

    @app.before_request
    def set_testing_user():
        set_user('foo', is_ldap_user=True)

    register_page = client.get(flask.url_for('auth.register_ldap'))
    register_page.form['institution'] = 'foo institution'

    with patch('eea_integration.auth.zope_acl_manager.create') as create_in_zope:
        result_page = register_page.form.submit()
        assert create_in_zope.call_count == 0

    assert "has been registered" in result_page.text

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.email == 'foo@example.com'
    assert foo_user.confirmed_at is not None
    assert foo_user.active
    assert foo_user.is_ldap

    assert len(outbox) == 1
    admin_message = outbox.pop()
    assert admin_message.recipients == ['admin@example.com']
    assert "Eionet user has registered" in admin_message.body
    url = admin_message.body.split()[-1]
    assert url == 'http://localhost/auth/users/foo'

    with patch('eea_integration.auth.zope_acl_manager.delete') as delete_in_zope:
        zope_auth['user_id'] = 'ze_admin'
        activation_page = client.get(url)
        activation_page.form['active'] = False
        activation_page.form.submit()
        assert delete_in_zope.call_count == 0

    foo_user = models.RegisteredUser.query.get('foo')
    assert not foo_user.active


def test_view_requires_admin(app, zope_auth, client):
    from .factories import DatasetFactory

    create_user('ze_admin', ['admin'])
    create_user('foo')
    DatasetFactory()
    models.db.session.commit()
    admin_user_url = flask.url_for('auth.admin_user', user_id='foo')

    assert client.get(admin_user_url, expect_errors=True).status_code == 403

    zope_auth.update({'user_id': 'ze_admin'})
    assert client.get(admin_user_url).status_code == 200


def test_change_local_password(app, zope_auth, client):
    from flask.ext.security.utils import encrypt_password
    foo = create_user('foo')
    old_enc_password = encrypt_password('my old pw')
    foo.password = old_enc_password
    models.db.session.commit()

    zope_auth.update({'user_id': 'foo'})
    page = client.get(flask.url_for('auth.change_password'))
    page.form['password'] = 'my old pw'
    page.form['new_password'] = 'the new pw'
    page.form['new_password_confirm'] = 'the new pw'
    with patch('eea_integration.auth.zope_acl_manager.edit') as edit_user_in_zope:
        confirmation_page = page.form.submit().follow()

    assert "password has been changed" in confirmation_page.text
    assert edit_user_in_zope.call_count == 1

    foo = models.RegisteredUser.query.filter_by(id='foo').first()
    assert foo.password != old_enc_password


def test_change_anonymous_password(app, zope_auth, client):
    page = client.get(flask.url_for('auth.change_password'))
    assert "You must log in before changing your password" in page


def test_change_ldap_password(app, zope_auth, client):
    foo = create_user('foo')
    foo.is_ldap = True
    models.db.session.commit()
    zope_auth.update({'user_id': 'foo', 'is_ldap_user': True})
    page = client.get(flask.url_for('auth.change_password'))
    assert "Your password can be changed only from the EIONET website (http://www.eionet.europa.eu/profile)." in page


def test_admin_edit_user_info(app, zope_auth, client, outbox):
    from .factories import DatasetFactory

    _set_config(admin_email='admin@example.com')
    create_user('ze_admin', ['admin'])
    foo = create_user('foo', ['etc', 'stakeholder'], name="Foo Person")
    DatasetFactory()
    models.db.session.commit()
    zope_auth.update({'user_id': 'ze_admin'})

    page = client.get(flask.url_for('auth.admin_user', user_id='foo'))
    page.form['name'] = "Foo Person"
    page.form['email'] = "foo@example.com"
    page.form['institution'] = "Foo Institution"
    page.form['qualification'] = "Foo is web developer"
    result_page = page.form.submit()

    assert "User information updated" in result_page.follow().text
    assert not result_page.status_code == 200
    assert not 'already associated with an account' in result_page.text

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.email == 'foo@example.com'
    assert foo_user.name == 'Foo Person'
    assert foo_user.institution == 'Foo Institution'
    assert foo_user.qualification == 'Foo is web developer'
    assert not foo_user.is_ldap

    bar = create_user('bar', ['etc'], name="Bar Person")
    models.db.session.commit()

    page = client.get(flask.url_for('auth.admin_user', user_id='bar'))
    page.form['name'] = "Bar Person"
    page.form['email'] = "foo@example.com"
    page.form['institution'] = "Bar Institution"
    page.form['qualification'] = "Bar is web developer"
    result_page = page.form.submit()

    assert result_page.status_code == 200
    assert 'already associated with an account' in result_page.text


def test_email_notification_for_role_changes(app, zope_auth, client, outbox):
    from .factories import DatasetFactory

    create_user('ze_admin', ['admin'])
    foo = create_user('foo', ['etc', 'stakeholder'], name="Foo Person")
    DatasetFactory()
    models.db.session.commit()
    zope_auth.update({'user_id': 'ze_admin'})
    page = client.get(flask.url_for('auth.admin_user', user_id='foo'))
    page.form['roles'] = ['stakeholder', 'nat']
    page.form['name'] = "Foo Person"
    page.form['email'] = "foo@example.com"
    page.form['institution'] = "Foo Institution"
    page.form.submit()
    assert len(outbox) == 0

    page.form['roles'] = ['etc', 'stakeholder']
    page.form['name'] = "Foo Person"
    page.form['email'] = "foo@example.com"
    page.form['institution'] = "Foo Institution"
    page.form['notify_user'] = True
    page.form.submit()

    assert len(outbox) == 1
    [msg] = outbox
    assert msg.recipients == ['foo@example.com']
    assert "* European topic center" in msg.body
    assert "* Stakeholder" in msg.body