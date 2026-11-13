import flask
import ldap
from flask_security.utils import encrypt_password
from mock import patch

from art12 import models
from art12.factsheet import format_info, format_subpopulation

from testsuite.conftest import create_user


def _login(client, username, password):
    page = client.get(flask.url_for("views.login"))
    page.form["username"] = username
    page.form["password"] = password
    return page.form.submit()


def _set_password(user_id, password, is_ldap):
    user = models.db.session.get(models.RegisteredUser, user_id)
    user.password = encrypt_password(password)
    user.is_ldap = is_ldap
    models.db.session.commit()


@patch("art12.models.get_ldap_connection")
def test_login_rejects_empty_password(ldap_conn, app, client):
    create_user("foo")
    response = _login(client, "foo", "")
    assert response.status_code == 200
    assert "Invalid username or password" in response.text
    assert not ldap_conn.called


@patch("art12.models.get_ldap_connection")
def test_login_escapes_ldap_dn(ldap_conn, app, client):
    ldap_conn.return_value.simple_bind_s.side_effect = ldap.INVALID_CREDENTIALS
    _login(client, "foo,ou=Admins", "secret")
    user_dn = ldap_conn.return_value.simple_bind_s.call_args[0][0]
    assert user_dn == "uid=foo\\,ou\\=Admins,ou=Users,o=EIONET,l=Europe"


@patch("art12.models.get_ldap_connection")
def test_login_local_user_falls_back_to_local_password(
    ldap_conn, app, plone_auth, client
):
    ldap_conn.return_value.simple_bind_s.side_effect = ldap.INVALID_CREDENTIALS
    create_user("foo")
    _set_password("foo", "p455w4rd", is_ldap=False)
    response = _login(client, "foo", "p455w4rd")
    assert response.status_code == 302
    assert "You have successfully logged in." in response.follow().text


@patch("art12.models.get_ldap_connection")
def test_login_ldap_user_cannot_use_stale_local_password(
    ldap_conn, app, plone_auth, client
):
    ldap_conn.return_value.simple_bind_s.side_effect = ldap.INVALID_CREDENTIALS
    create_user("foo")
    _set_password("foo", "old_eionet_password", is_ldap=True)
    response = _login(client, "foo", "old_eionet_password")
    assert response.status_code == 200
    assert "Invalid username or password" in response.text


def test_format_info_escapes_html():
    value = format_info("<script>alert(1)</script>|second line")
    assert value == "&lt;script&gt;alert(1)&lt;/script&gt;<br>second line"


def test_format_subpopulation_escapes_html():
    value = format_subpopulation("<b>x</b> [all others]")
    assert value == "<i>&lt;b&gt;x&lt;/b&gt; </i>[</i>all others<i>]<i></i>"
