import json
import ldap
import uuid

from datetime import datetime

from flask import flash, g, redirect, render_template, request, url_for, abort
from flask.views import View

from flask_login import login_user, logout_user

from sqlalchemy.sql.expression import bindparam

from eea_integration.auth.security import (
    current_user,
    login_manager,
    verify,
    encrypt_password,
)
from eea_integration.auth.providers import _get_initial_ldap_data
from eea_integration.auth.common import set_user_active

from art12.common import HOMEPAGE_VIEW_NAME
from art12.common import TemplateView, get_map_path, get_map_url
from art12.common import get_eu_map_breeding_url, get_eu_map_winter_url
from art12.definitions import EU_COUNTRY
from art12.factsheet import get_factsheet_url
from art12.forms import (
    ProgressFilterForm,
    ReportsFilterForm,
    SummaryFilterForm,
    LoginForm,
)
from art12.mixins import SpeciesMixin
from art12.models import Dataset, LuDataBird, LuRestrictedDataBird, RegisteredUser, db


class Homepage(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        context.update(
            {
                "current_user": current_user,
            }
        )
        return context


class Summary(SpeciesMixin, TemplateView):
    template_name = "summary/species.html"

    def get_speciescode(self, dataset, speciesname):
        return (
            LuDataBird.query.filter_by(dataset=dataset, speciesname=speciesname)
            .first_or_404()
            .speciescode
        )

    def get_context_data(self, **kwargs):
        map_url = ""
        map_warning = ""
        map_available = True
        sensitive = False
        eu_map_breeding_url, eu_map_winter_url = "", ""
        factsheet_url = ""
        filter_form = SummaryFilterForm(request.args)
        filter_args = {}
        subject = filter_form.subject.data
        dataset = filter_form.dataset
        speciescode = None
        reported_name = filter_form.reported_name.data
        if subject:
            if dataset.id == 3:
                speciescode = self.get_speciescode(dataset, subject)
                filter_args["assessment_speciesname"] = subject
                if reported_name:
                    filter_args["speciescode"] = reported_name
                else:
                    if len(self.get_reported_name(dataset, subject)) > 1:
                        map_available = False
            else:
                speciescode = subject
                filter_args["speciescode"] = subject
        if filter_args:
            filter_args["dataset"] = dataset
            qs = self.model_cls.query.filter_by(**filter_args)
            content_objects = qs.filter(self.model_cls.country_isocode != EU_COUNTRY)
            eu_objects = self.model_eu_cls.query.filter_by(**filter_args).order_by(
                self.model_eu_cls.additional_record.desc()
            )

            sensitive_records = LuRestrictedDataBird.query.filter_by(
                speciescode=speciescode, dataset=dataset, show_data=0
            ).all()
            if sensitive_records:
                map_warning = ", ".join([s.country for s in sensitive_records])
                sensitive = True

            map_url = get_map_url(
                subject=speciescode,
                reported_name=reported_name,
                dataset=dataset,
                sensitive=sensitive,
            )
            eu_map_breeding_url = get_eu_map_breeding_url(
                subject=speciescode,
                sensitive=sensitive,
            )
            eu_map_winter_url = get_eu_map_winter_url(
                subject=speciescode,
                sensitive=sensitive,
            )
            factsheet_url = get_factsheet_url(subject=speciescode, dataset=dataset)
        else:
            filter_args["dataset"] = dataset
            content_objects = []
            eu_objects = []
        return {
            "filter_form": filter_form,
            "objects": content_objects,
            "eu_objects": eu_objects,
            "current_selection": filter_form.get_selection(),
            "dataset": dataset,
            "speciescode": speciescode,
            "subject": subject,
            "sensitive": sensitive,
            "reported_name": reported_name,
            "map_url": map_url,
            "map_warning": map_warning,
            "map_available": map_available,
            "eu_map_breeding_url": eu_map_breeding_url,
            "eu_map_winter_url": eu_map_winter_url,
            "factsheet_url": factsheet_url,
        }


class Progress(SpeciesMixin, TemplateView):
    template_name = "progress/species.html"
    TREND_LABEL = "trend"
    STATUS_LABEL = "status"

    def get_species_qs(self, dataset, conclusion_value, status_level):

        return (
            self.model_eu_cls.query.filter_by(dataset=dataset)
            .filter(conclusion_value is not None)
            .with_entities(
                self.model_eu_cls.speciescode.label("code"),
                self.model_eu_cls.speciesname.label("name"),
                conclusion_value.label("conclusion"),
                status_level.label("status"),
                self.model_eu_cls.additional_record,
                self.model_eu_cls.assessment_speciesname.label("url_name"),
                self.model_eu_cls.reported_name.label("reported_name"),
            )
        )

    def get_context_data(self, **kwargs):
        filter_form = ProgressFilterForm(request.args)

        conclusion_type = filter_form.conclusion.data
        dataset = filter_form.dataset
        status_level = self.model_eu_cls.conclusion_status_level2
        label_type = self.TREND_LABEL
        species = []
        if conclusion_type:
            if conclusion_type == "bs":
                status_level = self.model_eu_cls.conclusion_status_level1
                conclusion_value = self.model_eu_cls.conclusion_status_label
                label_type = self.STATUS_LABEL
            elif conclusion_type == "stbp":
                conclusion_value = self.model_eu_cls.br_population_trend
            elif conclusion_type == "ltbp":
                conclusion_value = self.model_eu_cls.br_population_trend_long
            elif conclusion_type == "stwp":
                conclusion_value = self.model_eu_cls.wi_population_trend
            elif conclusion_type == "ltwp":
                conclusion_value = self.model_eu_cls.wi_population_trend_long
            else:
                abort(404)
            eu_species = self.get_species_qs(dataset, conclusion_value, status_level)
            ignore_species = self.model_eu_cls.query.with_entities(
                self.model_eu_cls.speciescode
            )
            ms_species = (
                LuDataBird.query.filter(~LuDataBird.speciescode.in_(ignore_species))
                .filter_by(dataset=dataset)
                .with_entities(
                    LuDataBird.speciescode.label("code"),
                    LuDataBird.speciesname.label("name"),
                    bindparam("conclution", ""),
                    bindparam("status", ""),
                    bindparam("additional_record", False),
                    bindparam("", ""),
                    bindparam("", ""),
                )
            )
            species = sorted(eu_species.union(ms_species), key=lambda x: x.name)

        return {
            "filter_form": filter_form,
            "species": species,
            "current_selection": filter_form.get_selection(),
            "dataset": dataset,
            "label_type": label_type,
        }


class Reports(SpeciesMixin, TemplateView):
    template_name = "reports/species.html"

    def get_context_data(self, **kwargs):
        filter_form = ReportsFilterForm(request.args)
        country = filter_form.country.data
        period = filter_form.period.data
        if country:
            objects = (
                self.model_cls.query.filter_by(country_isocode=country)
                .filter_by(dataset_id=period)
                .order_by(self.model_cls.speciesname)
            )
        else:
            objects = []

        return {
            "filter_form": filter_form,
            "current_selection": filter_form.get_selection(),
            "objects": objects,
            "dataset": filter_form.dataset,
        }


class ConnectedSelectBoxes(View, SpeciesMixin):
    methods = ["GET"]

    def dispatch_request(self):
        try:
            dataset_id = int(request.args.get("dataset_id", 3))
        except ValueError:
            abort(404)
        dataset = Dataset.query.get_or_404(dataset_id)
        options = [("", "-")] + self.get_subjects(dataset)
        return json.dumps(options)


class FilterFormReportedName(View, SpeciesMixin):
    methods = ["GET"]

    def dispatch_request(self):
        try:
            dataset_id = int(request.args.get("dataset_id", 4))
        except ValueError:
            abort(404)
        speciesname = request.args.get("subject", "")
        dataset = Dataset.query.get_or_404(dataset_id)
        options = [("", "-")] + self.get_reported_name(dataset, speciesname)
        return json.dumps(options)


class FilterFormCountries(View, SpeciesMixin):
    methods = ["GET"]

    def dispatch_request(self):
        try:
            dataset_id = int(request.args.get("dataset_id", 3))
        except ValueError:
            abort(404)
        dataset = Dataset.query.get_or_404(dataset_id)
        options = [("", "-")] + self.get_countries(dataset)
        return json.dumps(options)


class EuMap(TemplateView):
    template_name = "summary/eu_map.html"

    def get_context_data(self, **kwargs):
        speciescode = request.args["speciescode"]
        suffix = request.args["suffix"]
        map_path = get_map_path(speciescode, suffix)
        map_url = url_for("static", filename=map_path) if map_path else None
        return {"map_url": map_url}


@login_manager.user_loader
def load_user(id=None):
    return db.session.get(RegisteredUser, id)


def try_local_login(username, password, form):
    user = RegisteredUser.query.filter_by(id=username).first()
    if not user or not verify(password, user):
        flash("Please check your login details and try again.")
        return render_template("login.html", form=form)
    login_user(user)
    g.user = user
    flash("You have successfully logged in.", "success")
    return redirect(url_for(HOMEPAGE_VIEW_NAME))


class LoginView(TemplateView):
    template_name = "login.html"

    def get(self, *args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already logged in.")
            return redirect(url_for(HOMEPAGE_VIEW_NAME))
        form = LoginForm(request.form)
        if form.errors:
            flash(form.errors, "danger")
        return render_template("login.html", form=form)

    def post(self, *args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already logged in.")
            return redirect(url_for(HOMEPAGE_VIEW_NAME))
        form = LoginForm(request.form)
        if form.errors:
            flash(form.errors, "danger")
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            RegisteredUser.try_login(username, password)
        except ldap.INVALID_CREDENTIALS:

            try_local_login(username, password, form)
            if not current_user.is_authenticated:
                flash("Invalid username or password. Please try again.", "danger")
                return render_template("login.html", form=form)

        user = RegisteredUser.query.filter_by(id=username).first()

        if not user:
            initial_data = _get_initial_ldap_data(username)
            user = RegisteredUser(
                id=username,
                name=initial_data["name"],
                email=initial_data["email"],
                institution=initial_data["institution"],
                qualification=initial_data["qualification"],
                password=encrypt_password(password),
                is_ldap=True,
                fs_uniquifier=uuid.uuid4().hex,
                confirmed_at=datetime.utcnow(),
                account_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
            )
            set_user_active(user, True)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        g.user = user
        flash("You have successfully logged in.", "success")
        return redirect(url_for(HOMEPAGE_VIEW_NAME))

        if form.errors:
            flash(form.errors, "danger")

        return render_template("login.html", form=form)


class LogoutView(TemplateView):
    def get(self, *args, **kwargs):
        logout_user()
        return redirect(url_for(HOMEPAGE_VIEW_NAME))
