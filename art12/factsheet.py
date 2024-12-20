import jinja2
import subprocess
import urllib

from flask import Blueprint, abort
from flask import render_template, request, current_app as app, url_for
from flask.cli import AppGroup
from flask.views import MethodView
from path import Path

from sqlalchemy import text
from sqlalchemy.sql.expression import bindparam
from sqlalchemy.types import String, Integer

from art12.common import get_map_path
from art12.models import (
    db,
    EtcBirdsEu,
    EtcDataBird,
    LuDataBird,
    Wiki,
    WikiChange,
)
from art12.pdf import PdfRenderer
from art12.queries import (
    SPECIESNAME_Q,
    SUBUNIT_Q,
    ANNEX_Q,
    PLAN_Q,
    MS_TABLE_Q,
    SPA_TRIGGER_Q,
    PRESS_THRE_Q,
    N2K_Q,
    CONS_MEASURES_Q,
)
from art12.utils import slugify

factsheet_manager = AppGroup("factsheet")
factsheet = Blueprint("factsheet", __name__)


@factsheet.app_template_filter("format_subpopulation")
def format_subpopulation(subpopulation):
    subpopulation = f"<i>{subpopulation}</i>"
    return jinja2.Markup(
        subpopulation.replace("[", "</i>[")
        .replace("]", "]<i>")
        .replace("all others", "</i>all others<i>")
    )


@factsheet.app_template_filter("format_info")
def format_info(value):
    return value.replace("|", "<br>")


@factsheet.app_template_global("get_map_url")
def get_map_url(code, suffix):
    map = get_map_path(code=code, suffix=suffix)
    if map:
        return app.config["MAP_URL_PREFIX"] + url_for("static", filename=map)


def get_arg(kwargs, key, default=None):
    arg = kwargs.get(key)
    return arg[0] if isinstance(arg, list) else arg or default


def get_query_result(engine, query, value):
    sql = text(query).bindparams(bindparam("value", String))
    result = []
    with engine.connect() as conn:
        result = conn.execute(statement=sql, parameters={"value": value})
    return ", ".join([row[0] for row in result if row[0]])


class DummyCls(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class BirdFactsheet(MethodView):
    template_name = "factsheet/species.html"
    property_to_query = {
        "speciesname": SPECIESNAME_Q,
        "subunit": SUBUNIT_Q,
        "annex": ANNEX_Q,
        "plan": PLAN_Q,
    }

    def list_all(self):
        objects = EtcDataBird.query.filter_by(dataset_id=self.period)
        return render_template("factsheet/list_all.html", objects=objects)

    def set_properties(self, obj):
        for prop_name, query in self.property_to_query.items():
            value = get_query_result(self.engine, query, self.subject)
            setattr(obj, prop_name, value)

    def set_wiki(self, obj):
        wiki_change = (
            WikiChange.query.join(Wiki)
            .filter(
                WikiChange.dataset_id == self.period,
                Wiki.speciescode == self.subject,
            )
            .first()
        )
        obj.wiki = wiki_change.body if wiki_change else ""

    def set_etc_birds(self, obj):
        obj.etc_birds = EtcBirdsEu.query.filter_by(
            speciescode=self.subject,
            dataset_id=self.period,
        )

    def set_conclusion_status_levels(self, obj):
        def get_bird_values(attr):
            return [getattr(b, attr) for b in obj.etc_birds if getattr(b, attr)]

        for attr in [
            "conclusion_status_level1_record",
            "conclusion_status_level2_record",
        ]:
            setattr(obj, attr, any(get_bird_values(attr)))

        for attr in ["conclusion_status_level1", "conclusion_status_level2"]:
            setattr(obj, attr, ", ".join(get_bird_values(attr)))

    def set_ms_birds(self, obj):
        sql = text(MS_TABLE_Q).bindparams(
            bindparam("subject", String), bindparam("period", Integer)
        )
        result = []
        with self.tool_engine.connect() as conn:
            result = conn.execute(
                sql,
                subject=str(self.subject),  # Explicitly cast subject to String
                period=int(self.period),  # Explicitly cast period to Integer
            )
        obj.ms_birds = [DummyCls(**dict(row.items())) for row in result]

    def is_spa_trigger(self):
        sql = text(SPA_TRIGGER_Q).bindparams(bindparam("subject", String))
        result = []
        with self.engine.connect() as conn:
            result = conn.execute(sql, subject=self.subject)
        row = result and result.first()
        return row and row["count"] > 0

    def set_list_property(self, obj, prop_name, query):
        result = self.get_query_result(self.engine, query, self.subject)
        list_obj = [DummyCls(**dict(row.items())) for row in result]
        setattr(obj, prop_name, list_obj)

    def get_context_data(self, **kwargs):
        try:
            self.period = int(get_arg(kwargs, "period", app.config["DEFAULT_PERIOD"]))
        except ValueError:
            self.period = app.config["DEFAULT_PERIOD"]
        self.subject = get_arg(kwargs, "subject")
        self.engine = db.get_engine("factsheet")
        self.tool_engine = db.get_engine()

        bird_obj = DummyCls()
        self.set_properties(bird_obj)
        self.set_wiki(bird_obj)
        self.set_etc_birds(bird_obj)
        self.set_conclusion_status_levels(bird_obj)
        self.set_ms_birds(bird_obj)
        bird_obj.url = app.config["LOCAL_PDF_URL_PREFIX"] + url_for(
            "views.summary", subject=self.subject, period=self.period
        )
        bird_obj.code = self.subject

        if self.is_spa_trigger():
            bird_obj.is_spa_trigger = True
            spa_properties = {
                "threats": PRESS_THRE_Q,
                "n2k": N2K_Q,
                "cons_measures": CONS_MEASURES_Q,
            }
            for prop, query in spa_properties.items():
                self.set_list_property(bird_obj, prop, query)

        return {"obj": bird_obj}

    def get(self):
        context = self.get_context_data(**request.args)

        if not self.subject:
            return self.list_all()

        return render_template(self.template_name, **context)

    @classmethod
    def get_pdf_file_name(cls, subject, engine=None):
        engine = engine or db.get_engine("factsheet")
        name = get_query_result(engine, SPECIESNAME_Q, subject)
        subunit = get_query_result(engine, SUBUNIT_Q, subject)
        return slugify(f"{name} {subunit}")

    def _get_pdf_file_name(self):
        return self.get_pdf_file_name(self.subject, self.engine)

    def get_pdf(self, **kwargs):
        context = self.get_context_data(**kwargs)
        header_url = app.config["LOCAL_PDF_URL_PREFIX"] + url_for(
            "factsheet.header", subject=self.subject, period=self.period
        )
        footer_url = app.config["LOCAL_PDF_URL_PREFIX"] + url_for("factsheet.footer")
        return PdfRenderer(
            self.template_name,
            pdf_file=self._get_pdf_file_name(),
            height="11.693in",
            width="8.268in",
            context=context,
            header_url=header_url,
            footer_url=footer_url,
        )

    @classmethod
    def get_all(cls, period):
        return (
            db.session.query(EtcDataBird.speciescode)
            .filter(EtcDataBird.dataset_id == period)
            .distinct()
        )


class FactsheetHeader(MethodView):
    def get_context_data(self, **kwargs):
        try:
            period = int(get_arg(kwargs, "period", app.config["DEFAULT_PERIOD"]))
        except ValueError:
            abort(404)
        subject = get_arg(kwargs, "subject")
        period = get_arg(kwargs, "period")

        bird = EtcDataBird.query.filter_by(
            speciescode=subject, dataset_id=period
        ).first_or_404()
        factsheet_engine = db.get_engine("factsheet")
        result = get_query_result(factsheet_engine, SUBUNIT_Q, subject)
        row = result and result.first()
        subunit = row and row["sub_unit"]

        return {
            "period": bird.dataset.name,
            "subject": bird.speciesname,
            "subunit": subunit,
        }

    def get(self):
        context = self.get_context_data(**request.args)
        return render_template("factsheet/header.html", **context)


class FactsheetFooter(MethodView):
    def get(self):
        return render_template("factsheet/footer.html")


def get_pdf_path(subject):
    pdf_path = Path(app.config["PDF_DESTINATION"]) / (
        BirdFactsheet.get_pdf_file_name(subject) + ".pdf"
    )
    real_path = Path(app.static_folder) / pdf_path
    if real_path.exists():
        return pdf_path


def check_if_species_is_non_native(subject, dataset):
    """
    Check if the subject is non-native and if there is a native version.
    """
    native_exists = LuDataBird.query.filter_by(
        dataset=dataset, speciescode=subject[:-2]
    ).count()
    if subject.endswith("-X") and native_exists:
        return True


def get_factsheet_url(subject, dataset):
    if check_if_species_is_non_native(subject, dataset):
        return
    pdf_file_name = BirdFactsheet.get_pdf_file_name(subject)

    pdf_url = f"{app.config['PDF_URL_PREFIX']}/{pdf_file_name}.pdf"
    try:
        code = urllib.request.urlopen(pdf_url).getcode()
        if code == 200:
            return pdf_url
    except:
        return None


@factsheet_manager.command
def species(subject, period):
    fs = BirdFactsheet()
    renderer = fs.get_pdf(subject=subject, period=period)
    renderer._generate()
    print(f"Generated for {subject}: {renderer.pdf_path}")


@factsheet_manager.command
def genall(period, overwrite_existing=False):
    for obj in BirdFactsheet.get_all(period):
        if not overwrite_existing and get_pdf_path(obj.speciescode):
            continue
        try:
            species(obj.speciescode, period)
        except subprocess.CalledProcessError:
            print(f"Error occured for: {obj.speciescode}")
    print("Done")
