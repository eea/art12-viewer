import flask
import json
from sqlalchemy import text
from flask_login import login_user

from art12 import models
from art12.common import get_config
from art12.models import db, RegisteredUser
from .conftest import create_user
from eea_integration.auth.providers import set_user
from flask import current_app
from flask_security.utils import encrypt_password

from testsuite.factories import DatasetFactory, LuDataBirdFactory, EtcDataBirdFactory, EtcBirdsEuFactory

def force_login(client, fs_uniquifier=None):
    with client.session_transaction() as sess:
        sess["_user_id"] = fs_uniquifier
        sess["_fresh"] = True


def test_homepage_get(
    app,
    plone_auth,
    client,
):
    create_user("test_user")
    force_login(client, "test_user")
    url = flask.url_for("views.homepage")
    response = client.get(url)
    assert response.status_code == 200

def test_summary_get(
    app,
    plone_auth,
    client,
):
    dataset = DatasetFactory()
    create_user("test_user")
    force_login(client, "test_user")
    url = flask.url_for("views.summary")
    response = client.get(url, params={"period": dataset.id})
    assert response.status_code == 200

def test_summary_filter_form(
    app,
    plone_auth,
    client,
):
    dataset = DatasetFactory()
    subject = LuDataBirdFactory(dataset=dataset)
    create_user("test_user")
    force_login(client, "test_user")
    url = flask.url_for("views.filter_form")
    response = client.get(url, params={"dataset_id": dataset.id})
    assert response.status_code == 200
    data = json.loads(response.body)
    assert data[1][0] == subject.speciescode
    assert data[1][1] == subject.speciesname

def test_summary_filter_form_reported_name(
    app,
    plone_auth,
    client,
):
    dataset = DatasetFactory()
    subject = LuDataBirdFactory(dataset=dataset)
    entry = EtcDataBirdFactory(dataset=dataset, assessment_speciesname=subject.speciesname)
    create_user("test_user")
    force_login(client, "test_user")
    url = flask.url_for("views.filter_form_reported_name")
    params = {
        "dataset_id": dataset.id,
        "subject": subject.speciesname,
    }
    response = client.get(url, params=params)
    assert response.status_code == 200
    data = json.loads(response.body)
    assert data[1][0] == entry.speciescode
    assert data[1][1] == entry.reported_name

def test_summary_filter_form_countries(
    app,
    plone_auth,
    client,
):
    dataset = DatasetFactory()
    entry = EtcDataBirdFactory(dataset=dataset)
    create_user("test_user")
    force_login(client, "test_user")
    url = flask.url_for("views.filter_form_countries")
    response = client.get(url, params={"dataset_id": dataset.id})
    assert response.status_code == 200
    data = json.loads(response.body)
    assert data[1][0] == entry.country_isocode
    assert data[1][1] == entry.country

def test_progress_get(
    app,
    plone_auth,
    client,
):
    dataset = DatasetFactory()
    subject = LuDataBirdFactory(dataset=dataset)
    entry = EtcDataBirdFactory(dataset=dataset, assessment_speciesname=subject.speciesname)
    eu_entry = EtcBirdsEuFactory(dataset=dataset, speciescode='1112')
    models.db.session.commit()
    create_user("test_user")
    force_login(client, "test_user")
    url = flask.url_for("views.progress")
    response = client.get(url, params={"period": dataset.id, "conclusion": "bs"})
    assert response.status_code == 200
    assert len(response.context['species']) == 2
    assert response.context['species'][0][0] == entry.speciescode
    assert response.context['species'][0][1] == entry.speciesname
    assert response.context['species'][1][0] == eu_entry.speciescode
    assert response.context['species'][1][1] == eu_entry.speciesname

def test_report_get(
    app,
    plone_auth,
    client,
):
    dataset = DatasetFactory()
    entry = EtcDataBirdFactory(dataset=dataset)
    create_user("test_user")
    force_login(client, "test_user")
    url = flask.url_for("views.report")
    response = client.get(url, params={"period": dataset.id, "country": entry.country_isocode})
    assert response.status_code == 200
    assert response.context['objects'].count() == 1
    assert response.context['objects'][0].speciescode == entry.speciescode
    assert response.context['objects'][0].speciesname == entry.speciesname

def test_eu_map_get(
    app,
    plone_auth,
    client,
):
    dataset = DatasetFactory()
    entry = EtcBirdsEuFactory(dataset=dataset)
    create_user("test_user")
    force_login(client, "test_user")
    url = flask.url_for("views.eu_map")
    response = client.get(url, params={"suffix": 'PR', "speciescode": entry.speciescode})
    assert response.status_code == 200
