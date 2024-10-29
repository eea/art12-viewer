import flask
from flask import current_app
from flask_security.utils import encrypt_password

from art12 import models
from art12.common import get_config
from art12.models import db, RegisteredUser

from testsuite.conftest import create_user


def force_login(client, fs_uniquifier=None):
    with client.session_transaction() as sess:
        sess["_user_id"] = fs_uniquifier
        sess["_fresh"] = True


def _set_config(**kwargs):
    for key in kwargs:
        setattr(get_config(), key, kwargs[key])
    db.session.commit()


def test_admin_creates_local(app, plone_auth, client, outbox, ldap_user_info):
    from .factories import DatasetFactory

    _set_config(admin_email="admin@example.com")
    create_user("ze_admin", ["admin"])
    DatasetFactory()
    models.db.session.commit()
    force_login(client, "ze_admin")

    register_page = client.get(flask.url_for("auth.admin_create_local"))
    register_page.form["id"] = "foo"
    register_page.form["email"] = "foo@example.com"
    register_page.form["password"] = "p455w4rd"
    register_page.form["name"] = "foo me"
    register_page.form["institution"] = "foo institution"

    result_page = register_page.form.submit().follow()
    assert "User foo created successfully." in result_page

    foo_user = db.session.get(RegisteredUser, "foo")
    assert foo_user.email == "foo@example.com"
    assert foo_user.confirmed_at is not None
    assert foo_user.active
    assert not foo_user.is_ldap
    assert foo_user.password.startswith("{SSHA}")

    assert len(outbox) == 1
    message = outbox.pop()
    assert "Dear foo me," in message.body
    assert '"foo"' in message.body
    assert '"p455w4rd"' in message.body


def test_admin_creates_ldap(app, plone_auth, client, outbox, ldap_user_info):
    from .factories import DatasetFactory

    _set_config(admin_email="admin@example.com")
    create_user("ze_admin", ["admin"])
    force_login(client, "ze_admin")
    DatasetFactory()
    models.db.session.commit()

    ldap_user_info["foo"] = {
        "full_name": "foo me",
        "email": "foo@example.com",
    }

    enter_user_id_page = client.get(flask.url_for("auth.admin_create_ldap"))
    enter_user_id_page.form["user_id"] = "foo"
    register_page = enter_user_id_page.form.submit()

    register_page.form["institution"] = "foo institution"

    result_page = register_page.form.submit().follow()

    assert "User foo created successfully." in result_page

    foo_user = db.session.get(RegisteredUser, "foo")
    assert foo_user.email == "foo@example.com"
    assert foo_user.confirmed_at is not None
    assert foo_user.active
    assert foo_user.is_ldap

    assert len(outbox) == 1
    message = outbox.pop()
    assert "Dear foo me," in message.body
    assert '"foo"' in message.body


def test_ldap_account_activation_flow(
    app,
    plone_auth,
    client,
    outbox,
    ldap_user_info,
):
    from .factories import DatasetFactory

    DatasetFactory()
    models.db.session.commit()
    ldap_user_info["foo"] = {"email": "foo@example.com", "full_name": "foo"}
    create_user("ze_admin", ["admin"])
    register_page = client.get(flask.url_for("auth.register_ldap"))
    register_page.context["message"] = (
        'First log into your EIONET account by clicking "login" at the top of the page.'
    )


def test_admin_user_view(app, plone_auth, client):
    create_user("ze_admin", ["admin"])
    create_user("foo")
    force_login(client, "ze_admin")
    admin_user_url = flask.url_for("auth.admin_user", user_id="foo")
    resp = client.get(admin_user_url)
    assert resp.status_code == 200


def test_admin_user_view_forbidden(app, plone_auth, client):
    create_user("foo")
    force_login(client, "foo")
    admin_user_url = flask.url_for("auth.admin_user", user_id="foo")
    resp = client.get(admin_user_url, expect_errors=True)
    assert resp.status_code == 403


def test_change_local_password(app, plone_auth, client):
    foo = create_user("foo")
    models.db.session.commit()
    old_enc_password = encrypt_password("my old pw")
    foo.password = old_enc_password
    force_login(client, "foo")
    models.db.session.add(foo)
    models.db.session.commit()
    page = client.get(flask.url_for("auth.change_password"))
    page.form["password"] = "my old pw"
    page.form["new_password"] = "the new pw"
    page.form["new_password_confirm"] = "the new pw"
    models.db.session.expire_on_commit = False
    confirmation_page = page.form.submit()
    confirmation_page = confirmation_page.follow()
    assert "password has been changed" in confirmation_page.text
    foo = RegisteredUser.query.filter_by(id="foo").first()
    assert foo.password != old_enc_password


def test_change_anonymous_password(app, plone_auth, client):
    page = client.get(flask.url_for("auth.change_password"))
    assert "You must log in before changing your password" in page


def test_change_ldap_password(app, plone_auth, client):
    EEA_PASSWORD_RESET = current_app.config["EEA_PASSWORD_RESET"]
    foo = create_user("foo")
    foo.is_ldap = True
    models.db.session.add(foo)
    models.db.session.commit()
    force_login(client, "foo")
    page = client.get(flask.url_for("auth.change_password"))
    msg = f"Your password can be changed only from the EIONET website ({EEA_PASSWORD_RESET})."
    assert page.context["message"] == msg


def test_admin_edit_user_info(app, plone_auth, client, outbox):
    from .factories import DatasetFactory

    _set_config(admin_email="admin@example.com")
    create_user("ze_admin", ["admin"])
    create_user("foo", ["etc", "stakeholder"], name="Foo Person")
    DatasetFactory()
    models.db.session.commit()
    force_login(client, "ze_admin")

    page = client.get(flask.url_for("auth.admin_user", user_id="foo"))
    page.form["name"] = "Foo Person"
    page.form["email"] = "foo@example.com"
    page.form["institution"] = "Foo Institution"
    page.form["qualification"] = "Foo is web developer"
    result_page = page.form.submit()

    assert "User information updated" in result_page.follow().text
    assert not result_page.status_code == 200
    assert "already associated with an account" not in result_page.text

    foo_user = db.session.get(RegisteredUser, "foo")
    assert foo_user.email == "foo@example.com"
    assert foo_user.name == "Foo Person"
    assert foo_user.institution == "Foo Institution"
    assert foo_user.qualification == "Foo is web developer"
    assert not foo_user.is_ldap

    create_user("bar", ["etc"], name="Bar Person")
    models.db.session.commit()

    page = client.get(flask.url_for("auth.admin_user", user_id="bar"))
    page.form["name"] = "Bar Person"
    page.form["email"] = "foo@example.com"
    page.form["institution"] = "Bar Institution"
    page.form["qualification"] = "Bar is web developer"
    result_page = page.form.submit()

    assert result_page.status_code == 200
    assert "already associated with an account" in result_page.text


def test_email_notification_for_role_changes(app, plone_auth, client, outbox):
    from .factories import DatasetFactory

    create_user("ze_admin", ["admin"])
    create_user("foo", ["etc", "stakeholder"], name="Foo Person")
    DatasetFactory()
    models.db.session.commit()
    force_login(client, "ze_admin")
    page = client.get(flask.url_for("auth.admin_user", user_id="foo"))
    page.form["roles"] = ["stakeholder", "nat"]
    page.form["name"] = "Foo Person"
    page.form["email"] = "foo@example.com"
    page.form["institution"] = "Foo Institution"
    page.form.submit()
    assert len(outbox) == 0

    page.form["roles"] = ["etc", "stakeholder"]
    page.form["name"] = "Foo Person"
    page.form["email"] = "foo@example.com"
    page.form["institution"] = "Foo Institution"
    page.form["notify_user"] = True
    page.form.submit()

    assert len(outbox) == 1
    [msg] = outbox
    assert msg.recipients == ["foo@example.com"]
    assert "* European topic center" in msg.body
    assert "* Stakeholder" in msg.body
