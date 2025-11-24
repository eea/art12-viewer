# coding: utf-8
import json
import ldap
import os
import sqlalchemy
import sys

from datetime import datetime
from sqlalchemy import inspect

from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
from sqlalchemy import (
    Column,
    Float,
    Integer,
    Numeric,
    String,
    Text,
    ForeignKey,
    DateTime,
    text,
    Boolean,
    SmallInteger,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from art12.definitions import SEASON_FIELDS, SEASON_FIELDS_CONVERT

alembic_ignore_tables = []

db = SQLAlchemy()

Base = db.Model
metadata = Base.metadata


def get_ldap_connection():
    ldap_url = "{}://{}:{}".format(
        app.config["EEA_LDAP_PROTOCOL"],
        app.config["EEA_LDAP_SERVER"],
        app.config["EEA_LDAP_PORT"],
    )
    conn = ldap.initialize(ldap_url)
    return conn


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)


class EtcDataBird(Base):
    __tablename__ = "etc_data_birds"

    country = Column(String(8), primary_key=True, nullable=False)
    country_isocode = Column(String(4))
    delivery = Column(Integer)
    envelope = Column(Text, nullable=False)
    filename = Column(String(60), nullable=True)
    reported_name = Column(Text)
    group = Column(String(30), index=True)
    family = Column(String(30))
    annex = Column(String(11))
    priority = Column(String(1))
    redlist = Column(Integer)
    euringcode = Column(String(30))
    code = Column(String(50))
    speciescode = Column(
        String(255), primary_key=True, nullable=False, server_default=text("''")
    )
    speciesname = Column(String(255))
    species_name_different = Column(Integer)
    subspecies_name = Column(String(255))
    eunis_species_code = Column(Integer)
    alternative_speciesname = Column(String(255))
    common_speciesname = Column(String(128))
    valid_speciesname = Column(Text)
    n2000_species_code = Column(Integer)
    assessment_speciescode = Column(String(10))
    assessment_speciesname = Column(String(255))
    assessment_speciesname_changed = Column(Integer)
    grouped_assesment = Column(Integer)
    species_type = Column(String(10))
    species_type_asses = Column(Integer)
    range_surface_area_bs = Column(Float(asdecimal=True))
    range_change_reason_bs = Column(String(150))
    percentage_range_surface_area_bs = Column(Float(asdecimal=True))
    range_additional_info_record_bs = Column(String(1))
    range_additional_info_bs = Column(Text)
    range_trend_period_bs = Column(String(30))
    range_trend_bs = Column(String(2))
    range_trend_magnitude_min_bs = Column(Numeric(18, 5))
    range_trend_magnitude_max_bs = Column(Numeric(18, 5))
    range_trend_long_period_bs = Column(String(30))
    range_trend_long_bs = Column(String(2))
    range_trend_long_magnitude_min_bs = Column(Numeric(18, 5))
    range_trend_long_magnitude_max_bs = Column(Numeric(18, 5))
    range_trend_additional_info_record_bs = Column(String(1))
    range_trend_additional_info_bs = Column(Text)
    range_yearly_magnitude_bs = Column(Float(asdecimal=True))
    complementary_favourable_range_op_bs = Column(String(2))
    complementary_favourable_range_bs = Column(Float(asdecimal=True))
    population_minimum_size_bs = Column(String(30))
    percentage_population_minimum_size_bs = Column(Float(asdecimal=True))
    population_maximum_size_bs = Column(String(30))
    percentage_population_maximum_size_bs = Column(Float(asdecimal=True))
    population_size_bs = Column(Text)
    population_size_method_bs = Column(String(255))
    filled_population_bs = Column(String(3))
    population_size_unit_bs = Column(String(255))
    population_units_agreed_bs = Column(String(50))
    population_units_other_bs = Column(String(50))
    population_estimateType_bs = Column("population_estimatetype_bs", String(255))
    population_change_reason_bs = Column(String(200))
    number_of_different_population_units_bs = Column(Integer)
    different_population_percentage_bs = Column(Integer)
    percentage_population_mean_size_bs = Column(String(30))
    population_additional_info_record_bs = Column(String(1))
    population_additional_info_bs = Column(Text)
    population_trend_period_bs = Column(String(255))
    population_trend_bs = Column(String(3))
    population_trend_magnitude_min_bs = Column(Numeric(18, 5))
    population_trend_magnitude_max_bs = Column(Numeric(18, 5))
    population_trend_magnitude_bs = Column(String(131))
    population_trend_long_period_bs = Column(String(255))
    population_trend_long_bs = Column(String(3))
    population_trend_long_magnitude_min_bs = Column(Numeric(18, 5))
    population_trend_long_magnitude_max_bs = Column(Numeric(18, 5))
    population_trend_long_magnitude_bs = Column(String(131))
    population_trend_additional_info_record_bs = Column(String(1))
    population_trend_additional_info_bs = Column(Text)
    population_yearly_magnitude_bs = Column(Float(asdecimal=True))
    complementary_favourable_population_op_bs = Column(String(2))
    complementary_favourable_population_bs = Column(Float(asdecimal=True))
    filled_complementary_favourable_population_bs = Column(String(3))
    distribution_surface_area_bs = Column(Text)
    distribution_surface_area_method_bs = Column(String(255))
    distribution_additional_info_record_bs = Column(String(1))
    distribution_additional_info_bs = Column(Text)
    percentage_distribution_surface_area_bs = Column(Text)
    distribution_trend_period_bs = Column(String(255))
    distribution_trend_bs = Column(String(3))
    distribution_trend_magnitude_min_bs = Column(Text)
    distribution_trend_magnitude_max_bs = Column(Text)
    distribution_trend_magnitude_bs = Column(String(131))
    distribution_trend_long_period_bs = Column(String(255))
    distribution_trend_long_bs = Column(String(3))
    distribution_trend_long_magnitude_min_bs = Column(Text)
    distribution_trend_long_magnitude_max_bs = Column(Text)
    distribution_trend_long_magnitude_bs = Column(String(131))
    distribution_trend_additional_info_record_bs = Column(String(1))
    distribution_trend_additional_info_bs = Column(Text)
    population_minimum_size_ws = Column(String(30))
    percentage_population_minimum_size_ws = Column(Float(asdecimal=True))
    population_maximum_size_ws = Column(String(30))
    percentage_population_maximum_size_ws = Column(Float(asdecimal=True))
    population_size_ws = Column(Text)
    population_size_method_ws = Column(String(255))
    filled_population_ws = Column(String(3))
    population_size_unit_ws = Column(String(255))
    population_units_agreed_ws = Column(String(10))
    population_units_other_ws = Column(String(10))
    population_estimateType_ws = Column("population_estimatetype_ws", String(255))
    population_change_reason_ws = Column(String(200))
    number_of_different_population_units_ws = Column(Integer)
    different_population_percentage_ws = Column(Integer)
    percentage_population_mean_size_ws = Column(String(30))
    population_additional_info_record_ws = Column(String(1))
    population_additional_info_ws = Column(Text)
    population_trend_period_ws = Column(String(255))
    population_trend_ws = Column(String(3))
    population_trend_magnitude_min_ws = Column(Numeric(18, 5))
    population_trend_magnitude_max_ws = Column(Numeric(18, 5))
    population_trend_magnitude_ws = Column(String(131))
    population_trend_long_period_ws = Column(String(255))
    population_trend_long_ws = Column(String(3))
    population_trend_long_magnitude_min_ws = Column(Numeric(18, 5))
    population_trend_long_magnitude_max_ws = Column(Numeric(18, 5))
    population_trend_long_magnitude_ws = Column(String(131))
    population_trend_additional_info_record_ws = Column(String(1))
    population_trend_additional_info_ws = Column(Text)
    status_ws = Column(String(18))
    presence_bs = Column(String(30))
    presence_ws = Column(String(30))
    future_prospects = Column(String(4))
    conclusion_range_bs = Column(String(4))
    conclusion_population_bs = Column(String(4))
    conclusion_population_ws = Column(String(4))
    conclusion_future = Column(String(4))
    conclusion_assessment = Column(String(4))
    conclusion_assessment_trend = Column(String(2))
    conclusion_assessment_prev = Column(String(4))
    conclusion_assessment_change = Column(String(2))
    range_quality_bs = Column(String(13))
    range_trend_quality_bs = Column(String(13))
    range_trend_long_quality_bs = Column(String(13))
    population_quality_bs = Column(String(13))
    population_trend_quality_bs = Column(String(13))
    population_trend_long_quality_bs = Column(String(13))
    population_quality_ws = Column(String(13))
    population_trend_quality_ws = Column(String(13))
    population_trend_long_quality_ws = Column(String(13))
    further_information = Column(Text)
    further_information_english = Column(Text)
    range_grid_area = Column(Float(asdecimal=True))
    percentage_range_grid_area = Column(Float(asdecimal=True))
    distribution_grid_area = Column(String(20))
    percentage_distribution_grid_area = Column(String(30))
    use_for_statistics = Column(Text)
    dataset_id = Column(
        "ext_dataset_id",
        ForeignKey("datasets.id"),
        primary_key=True,
        nullable=False,
        server_default=text("'0'"),
    )
    dataset = relationship(Dataset)

    def convert_to_float(self, value, field):
        if field in SEASON_FIELDS_CONVERT:
            try:
                if value:
                    return float(value)
            except ValueError:
                return value
        return value

    def _season(self, season):
        return {
            field: self.convert_to_float(getattr(self, field + season, None), field)
            for field in SEASON_FIELDS
        }

    @property
    def bs(self):
        return self._season("_bs")

    @property
    def ws(self):
        return self._season("_ws")

    @property
    def is_assesm(self):
        if self.dataset.id == 3:
            return self.use_for_statistics == "0"
        return self.species_type_asses == 0


class EtcBirdsEu(Base):
    __tablename__ = "etc_birds_eu_view"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    speciescode = Column(String(10), nullable=False, server_default=text("''"))
    speciesname = Column(String(255))
    reported_name = Column(Text)
    speciesname_subpopulation = Column(String(255))
    assessment_speciescode = Column(String(10))
    assessment_speciesname = Column(String(255))
    assessment_subpopulation = Column(String(255))
    euringcode = Column(String(30))
    non_native = Column(String(20))
    br_range_surface_area = Column(String(35))
    br_range_surface_area_downrounded = Column(String(35))
    br_range_trend = Column(String(25))
    br_range_trend_long = Column(String(25))
    br_population_size = Column(String(255))
    br_distribution_surface_area = Column(Integer)
    br_distribution_trend = Column(String(3))
    br_distribution_trend_long = Column(String(3))
    br_population_minimum_size = Column(Numeric(18, 5))
    br_population_minimum_size_downrounded = Column(Numeric(18, 5))
    br_population_maximum_size = Column(Numeric(18, 5))
    br_population_maximum_size_uprounded = Column(Numeric(18, 5))
    br_population_size_unit = Column(String(20))
    br_population_trend = Column(String(25))
    br_population_trend_long = Column(String(25))
    br_conclusion_status_label = Column(String(255))
    br_contribution_target1 = Column(String(50))
    br_red_list_cat = Column(String(255))
    wi_population_size = Column(String(255))
    wi_population_minimum_size = Column(Numeric(18, 5))
    wi_population_minimum_size_downrounded = Column(Numeric(18, 5))
    wi_population_maximum_size = Column(Numeric(18, 5))
    wi_population_maximum_size_uprounded = Column(Numeric(18, 5))
    wi_population_size_unit = Column(String(20))
    wi_population_trend = Column(String(25))
    wi_population_trend_long = Column(String(25))
    wi_conclusion_status_label = Column(String(255))
    wi_contribution_target1 = Column(String(50))
    wi_red_list_cat = Column(String(255))
    conclusion_status_label = Column(String(50))
    conclusion_status_improving = Column(String(50))
    conclusion_status_br_wi = Column(String(20))
    conclusion_status_level1_record = Column(String(20))
    conclusion_status_level1 = Column(String(512))
    conclusion_status_level2_record = Column(String(20))
    conclusion_status_level2 = Column(String(512))
    conclusion_population_size_unit = Column(String(20))
    conclusion_population_minimum_size = Column(Numeric(18, 5))
    conclusion_population_minimum_size_downrounded = Column(Numeric(18, 5))
    conclusion_population_maximum_size = Column(Numeric(18, 5))
    conclusion_population_maximum_size_uprounded = Column(Numeric(18, 5))
    conclusion_population_trend = Column(String(30))
    conclusion_population_trend_long = Column(String(30))
    contribution_target1 = Column(String(20))
    contribution_target1_label = Column(String(30))
    user = Column(String(50))
    last_update = Column(String(20))
    deleted_record = Column(Integer)
    decision = Column(String(20))
    user_decision = Column(String(50))
    last_update_decision = Column(String(50))
    additional_record = Column("addtionnal_record", Boolean)
    dataset_id = Column(
        "ext_dataset_id",
        ForeignKey("datasets.id"),
        primary_key=True,
        nullable=False,
        server_default=text("'0'"),
    )
    dataset = relationship(Dataset)
    use_for_statistics = Column(Text)
    conclusion_status_label_prev = Column(String(50))
    conclusion_status_br_wi_prev = Column(String(20))
    red_list_cat_prev = Column(String(255))

    lu_bird = relationship(
        "LuDataBird",
        primaryjoin="and_(EtcBirdsEu.speciescode==LuDataBird.speciescode,"
        "EtcBirdsEu.dataset_id==LuDataBird.dataset_id)",
        foreign_keys=[speciescode, dataset_id],
        overlaps="dataset",
        backref=db.backref("eu_objects", overlaps="dataset"),
    )


class LuDataBird(Base):
    __tablename__ = "lu_birds_name"

    speciescode = Column(
        String(10), primary_key=True, nullable=False, server_default=text("''")
    )
    speciesname = Column(String(128))
    dataset_id = Column(
        "ext_dataset_id",
        ForeignKey("datasets.id"),
        primary_key=True,
        nullable=False,
        server_default=text("'0'"),
    )
    dataset = relationship(Dataset)

    def has_additional_record(self):
        return any([obj.additional_record for obj in self.eu_objects])


class LuRestrictedDataBird(Base):
    __tablename__ = "lu_restricted_birds"

    speciescode = Column(String(10), nullable=False, primary_key=True)
    country = Column(String(8), nullable=False, primary_key=True)
    show_data = Column(SmallInteger(), nullable=False)
    dataset_id = Column(
        "ext_dataset_id",
        ForeignKey("datasets.id"),
        primary_key=True,
        nullable=False,
        server_default=text("'0'"),
    )
    dataset = relationship(Dataset)


class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    default_dataset_id = Column(Integer, default=1)
    species_map_url = Column(db.String(255))
    sensitive_species_map_url = Column(db.String(255))
    eu_species_map_breeding_url = Column(db.String(255))
    eu_sensitive_species_map_breeding_url = Column(db.String(255))
    eu_species_map_winter_url = Column(db.String(255))
    eu_sensitive_species_map_winter_url = Column(db.String(255))


class Wiki(Base):
    __tablename__ = "wiki"

    id = Column(Integer, primary_key=True)
    speciescode = Column(String(10))

    dataset_id = Column(
        "ext_dataset_id",
        ForeignKey("datasets.id"),
    )
    dataset = relationship(Dataset)

    @hybrid_property
    def subject(self):
        return self.speciescode


class WikiChange(Base):
    __tablename__ = "wiki_changes"

    id = Column(Integer, primary_key=True)
    wiki_id = Column(ForeignKey("wiki.id"), nullable=False)
    body = Column(String(6000), nullable=False)
    editor = Column(String(60), nullable=False)
    changed = Column(DateTime, nullable=False, default=datetime.now)
    active = Column(Integer, default=0)
    dataset_id = Column(
        "ext_dataset_id",
        ForeignKey("datasets.id"),
    )
    dataset = relationship(Dataset)
    wiki = relationship(
        "Wiki",
        primaryjoin="and_(WikiChange.wiki_id==Wiki.id,"
        "WikiChange.dataset_id==Wiki.dataset_id)",
        foreign_keys=[wiki_id, dataset_id],
        overlaps="dataset",
        backref=db.backref("changes", overlaps="dataset"),
    )


class WikiTrail(Base):
    __tablename__ = "wiki_trail"

    id = Column(Integer, primary_key=True)
    speciescode = Column(String(50))
    reported_name = Column(String(100))
    reported_name_code = Column(String(100))
    dataset_id = Column(
        "ext_dataset_id",
        ForeignKey("datasets.id"),
    )
    dataset = relationship(Dataset)

    @hybrid_property
    def subject(self):
        return self.speciescode


class WikiTrailChange(Base):
    __tablename__ = "wiki_trail_changes"

    id = Column(Integer, primary_key=True)
    wiki_id = Column(ForeignKey("wiki_trail.id"), nullable=False)
    body = Column(String(6000), nullable=False)
    editor = Column(String(60), nullable=False)
    changed = Column(DateTime, nullable=False, default=datetime.now)
    active = Column(Integer, default=0)
    dataset_id = Column(
        "ext_dataset_id",
        ForeignKey("datasets.id"),
    )
    dataset = relationship(Dataset)
    wiki = relationship(
        "WikiTrail",
        primaryjoin="and_(WikiTrailChange.wiki_id==WikiTrail.id,"
        "WikiTrailChange.dataset_id==WikiTrail.dataset_id)",
        foreign_keys=[wiki_id, dataset_id],
        overlaps="dataset",
        backref=db.backref("changes", overlaps="dataset"),
    )


roles_users = db.Table(
    "roles_users",
    db.Column(
        "registered_users_user", db.String(50), db.ForeignKey("registered_users.user")
    ),
    db.Column("role_id", db.Integer(), db.ForeignKey("roles.id")),
)


class RegisteredUser(Base, UserMixin):
    __tablename__ = "registered_users"

    id = Column("user", String(50), primary_key=True)
    name = Column(String(255))
    institution = Column(String(45))
    abbrev = Column(String(10))
    MS = Column("ms", String(255))
    email = Column(String(255))
    qualification = Column(String(255))
    account_date = Column(String(100), nullable=False)
    show_assessment = Column(Integer, nullable=False, default=1)
    active = Column(Boolean)
    confirmed_at = db.Column(db.DateTime())
    is_ldap = db.Column(Boolean, nullable=False, default=False)
    roles = db.relationship(
        "Role",
        secondary=roles_users,
        backref=db.backref("users", lazy="dynamic"),
    )
    password = db.Column(String(60))
    fs_uniquifier = db.Column(String(64))

    def has_role(self, role):
        return role in [r.name for r in self.roles]

    @staticmethod
    def try_login(username, password):
        conn = get_ldap_connection()
        conn.simple_bind_s("uid=%s,ou=Users,o=EIONET,l=Europe" % username, password)

    @property
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Role(Base, RoleMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False, unique=True)


def dumpdata(model):
    thismodule = sys.modules[__name__]
    base_class = getattr(thismodule, model)

    entries = base_class.query.all()
    relationship_fields = [
        rfield for rfield, _ in inspect(base_class).relationships.items()
    ]
    model_fields = [
        field
        for field in inspect(base_class).attrs.keys()
        if field not in relationship_fields
    ]

    objects = []
    primary_keys = []

    for field in model_fields:
        value = getattr(inspect(base_class).attrs, field)

        if value.columns[0].primary_key:
            primary_keys.append(field)

    for entry in entries:
        kwargs = {"model": model, "filter_fields": ",".join(primary_keys), "fields": {}}

        for field in model_fields:
            value = getattr(entry, field)

            if isinstance(value, datetime):
                value = value.isoformat()

            kwargs["fields"][field] = value

        for rfield in relationship_fields:
            class_field = getattr(entry, rfield)

            if isinstance(class_field, sqlalchemy.orm.collections.InstrumentedList):
                kwargs["fields"][rfield] = []
                for subfield in class_field:
                    kwargs["fields"][rfield].append(subfield.id)
            else:
                try:
                    kwargs["fields"][rfield] = class_field.id
                except AttributeError:
                    pass

        app_json = json.dumps(kwargs)
        objects.append(app_json)

    json_dir = os.path.abspath(os.path.dirname("manage.py"))
    json_name = model + ".json"

    with open(os.path.join(json_dir, json_name), "w") as f:
        f.write("[" + ",".join(objects) + "]")
