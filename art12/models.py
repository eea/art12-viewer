# coding: utf-8
import argparse
from datetime import datetime
from flask.ext.script import Manager
from flask.ext.security import UserMixin, RoleMixin
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column, Float, Integer, Numeric, String, Text, ForeignKey, DateTime, text,
    Boolean, SmallInteger,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from art12.definitions import SEASON_FIELDS

alembic_ignore_tables = []

db = SQLAlchemy()
db_manager = Manager()

Base = db.Model
metadata = Base.metadata


class Dataset(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)


class EtcDataBird(Base):
    __tablename__ = 'etc_data_birds'

    country = Column(String(8), primary_key=True, nullable=False)
    country_isocode = Column(String(4))
    delivery = Column(Integer)
    envelope = Column(String(60), nullable=False)
    filename = Column(String(60), nullable=False)
    group = Column(String(30), index=True)
    family = Column(String(30))
    annex = Column(String(11))
    priority = Column(String(1))
    redlist = Column(Integer)
    euringcode = Column(String(30))
    code = Column(String(50))
    speciescode = Column(String(10), primary_key=True, nullable=False,
                         server_default=text("''"))
    speciesname = Column(String(128))
    species_name_different = Column(Integer)
    subspecies_name = Column(String(128))
    eunis_species_code = Column(Integer)
    alternative_speciesname = Column(String(128))
    common_speciesname = Column(String(128))
    valid_speciesname = Column(String(128))
    n2000_species_code = Column(Integer)
    assesment_speciesname = Column(String(128))
    assesment_speciesname_changed = Column(Integer)
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
    population_minimum_size_bs = Column(Float(asdecimal=True))
    percentage_population_minimum_size_bs = Column(Float(asdecimal=True))
    population_maximum_size_bs = Column(Float(asdecimal=True))
    percentage_population_maximum_size_bs = Column(Float(asdecimal=True))
    filled_population_bs = Column(String(3))
    population_size_unit_bs = Column(String(10))
    population_units_agreed_bs = Column(String(50))
    population_units_other_bs = Column(String(50))
    population_change_reason_bs = Column(String(150))
    number_of_different_population_units_bs = Column(Integer)
    different_population_percentage_bs = Column(Integer)
    percentage_population_mean_size_bs = Column(Float(asdecimal=True))
    population_additional_info_record_bs = Column(String(1))
    population_additional_info_bs = Column(Text)
    population_trend_period_bs = Column(String(30))
    population_trend_bs = Column(String(2))
    population_trend_magnitude_min_bs = Column(Numeric(18, 5))
    population_trend_magnitude_max_bs = Column(Numeric(18, 5))
    population_trend_long_period_bs = Column(String(30))
    population_trend_long_bs = Column(String(2))
    population_trend_long_magnitude_min_bs = Column(Numeric(18, 5))
    population_trend_long_magnitude_max_bs = Column(Numeric(18, 5))
    population_trend_additional_info_record_bs = Column(String(1))
    population_trend_additional_info_bs = Column(Text)
    population_yearly_magnitude_bs = Column(Float(asdecimal=True))
    complementary_favourable_population_op_bs = Column(String(2))
    complementary_favourable_population_bs = Column(Float(asdecimal=True))
    filled_complementary_favourable_population_bs = Column(String(3))
    population_minimum_size_ws = Column(Float(asdecimal=True))
    percentage_population_minimum_size_ws = Column(Float(asdecimal=True))
    population_maximum_size_ws = Column(Float(asdecimal=True))
    percentage_population_maximum_size_ws = Column(Float(asdecimal=True))
    filled_population_ws = Column(String(3))
    population_size_unit_ws = Column(String(10))
    percentage_population_mean_size_ws = Column(Float(asdecimal=True))
    population_additional_info_record_ws = Column(String(1))
    population_additional_info_ws = Column(Text)
    population_trend_period_ws = Column(String(30))
    population_trend_ws = Column(String(2))
    population_trend_magnitude_min_ws = Column(Numeric(18, 5))
    population_trend_magnitude_max_ws = Column(Numeric(18, 5))
    population_trend_long_period_ws = Column(String(30))
    population_trend_long_ws = Column(String(2))
    population_trend_long_magnitude_min_ws = Column(Numeric(18, 5))
    population_trend_long_magnitude_max_ws = Column(Numeric(18, 5))
    population_trend_additional_info_record_ws = Column(String(1))
    population_trend_additional_info_ws = Column(Text)
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
    distribution_grid_area = Column(Float(asdecimal=True))
    percentage_distribution_grid_area = Column(Float(asdecimal=True))
    dataset_id = Column('ext_dataset_id', ForeignKey('datasets.id'),
                        primary_key=True, nullable=False,
                        server_default=text("'0'"))
    dataset = relationship(Dataset)
    presence_bs = Column(String(30))
    presence_ws = Column(String(30))

    def _season(self, season):
        return {field: getattr(self, field + season, None) for field in
                SEASON_FIELDS}

    @property
    def bs(self):
        return self._season('_bs')

    @property
    def ws(self):
        return self._season('_ws')

    @property
    def is_assesm(self):
        return self.species_type_asses == 0


class EtcBirdsEu(Base):
    __tablename__ = 'etc_birds_eu_view'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    speciescode = Column(String(10), nullable=False, server_default=text("''"))
    speciesname = Column(String(255))
    speciesname_subpopulation = Column(String(255))
    assessment_speciesname = Column(String(255))
    assessment_subpopulation = Column(String(255))
    euringcode = Column(String(30))
    non_native = Column(String(8))
    br_range_surface_area = Column(String(35))
    br_range_surface_area_downrounded = Column(String(35))
    br_range_trend = Column(String(25))
    br_range_trend_long = Column(String(25))
    br_population_size = Column(String(35))
    br_population_minimum_size = Column(Numeric(18, 5))
    br_population_minimum_size_downrounded = Column(Numeric(18, 5))
    br_population_maximum_size = Column(Numeric(18, 5))
    br_population_maximum_size_uprounded = Column(Numeric(18, 5))
    br_population_size_unit = Column(String(10))
    br_population_trend = Column(String(25))
    br_population_trend_long = Column(String(25))
    wi_population_size = Column(String(35))
    wi_population_minimum_size = Column(Numeric(18, 5))
    wi_population_minimum_size_downrounded = Column(Numeric(18, 5))
    wi_population_maximum_size = Column(Numeric(18, 5))
    wi_population_maximum_size_uprounded = Column(Numeric(18, 5))
    wi_population_size_unit = Column(String(10))
    wi_population_trend = Column(String(25))
    wi_population_trend_long = Column(String(25))
    conclusion_status_label = Column(String(25))
    conclusion_status_improving = Column(String(4))
    conclusion_status_br_wi = Column(String(3))
    conclusion_status_level1_record = Column(String(1))
    conclusion_status_level1 = Column(String(512))
    conclusion_status_level2_record = Column(String(1))
    conclusion_status_level2 = Column(String(512))
    conclusion_population_size_unit = Column(String(10))
    conclusion_population_minimum_size = Column(Numeric(18, 5))
    conclusion_population_minimum_size_downrounded = Column(Numeric(18, 5))
    conclusion_population_maximum_size = Column(Numeric(18, 5))
    conclusion_population_maximum_size_uprounded = Column(Numeric(18, 5))
    conclusion_population_trend = Column(String(25))
    conclusion_population_trend_long = Column(String(25))
    contribution_target1 = Column(String(3))
    contribution_target1_label = Column(String(25))
    user = Column(String(50))
    last_update = Column(String(16))
    deleted_record = Column(Integer)
    decision = Column(String(3))
    user_decision = Column(String(50))
    last_update_decision = Column(String(50))
    additional_record = Column('addtionnal_record', Integer)
    dataset_id = Column('ext_dataset_id', ForeignKey('datasets.id'),
                        primary_key=True, nullable=False,
                        server_default=text("'0'"))
    dataset = relationship(Dataset)


class LuDataBird(Base):
    __tablename__ = 'lu_birds_name'

    speciescode = Column(String(10), primary_key=True, nullable=False,
                         server_default=text("''"))
    speciesname = Column(String(128))
    dataset_id = Column('ext_dataset_id', ForeignKey('datasets.id'),
                        primary_key=True, nullable=False,
                        server_default=text("'0'"))
    dataset = relationship(Dataset)


class LuRestrictedDataBird(Base):
    __tablename__ = 'lu_restricted_birds'

    speciescode = Column(String(10), nullable=False, primary_key=True)
    country = Column(String(8), nullable=False, primary_key=True)
    show_data = Column(SmallInteger(), nullable=False)
    dataset_id = Column('ext_dataset_id', ForeignKey('datasets.id'),
                        primary_key=True, nullable=False,
                        server_default=text("'0'"))
    dataset = relationship(Dataset)


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True, autoincrement=True)
    default_dataset_id = Column(Integer, default=1)
    species_map_url = Column(db.String(255))
    sensitive_species_map_url = Column(db.String(255))
    eu_species_map_breeding_url = Column(db.String(255))
    eu_sensitive_species_map_breeding_url = Column(db.String(255))
    eu_species_map_winter_url = Column(db.String(255))
    eu_sensitive_species_map_winter_url = Column(db.String(255))


class Wiki(Base):
    __tablename__ = 'wiki'

    id = Column(Integer, primary_key=True)
    speciescode = Column(String(10))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
    )
    dataset = relationship(Dataset)

    @hybrid_property
    def subject(self):
        return self.speciescode


class WikiChange(Base):
    __tablename__ = 'wiki_changes'

    id = Column(Integer, primary_key=True)
    wiki_id = Column(ForeignKey('wiki.id'), nullable=False)
    body = Column(String(6000), nullable=False)
    editor = Column(String(60), nullable=False)
    changed = Column(DateTime, nullable=False,
                     default=datetime.now)
    active = Column(Integer, default=0)
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
    )
    dataset = relationship(Dataset)
    wiki = relationship(
        u'Wiki',
        primaryjoin="and_(WikiChange.wiki_id==Wiki.id,"
                    "WikiChange.dataset_id==Wiki.dataset_id)",
        foreign_keys=[wiki_id, dataset_id],
        backref='changes',
    )


class WikiTrail(Base):
    __tablename__ = 'wiki_trail'

    id = Column(Integer, primary_key=True)
    speciescode = Column(String(10))
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
    )
    dataset = relationship(Dataset)

    @hybrid_property
    def subject(self):
        return self.speciescode


class WikiTrailChange(Base):
    __tablename__ = 'wiki_trail_changes'

    id = Column(Integer, primary_key=True)
    wiki_id = Column(ForeignKey('wiki_trail.id'), nullable=False)
    body = Column(String(6000), nullable=False)
    editor = Column(String(60), nullable=False)
    changed = Column(DateTime, nullable=False,
                     default=datetime.now)
    active = Column(Integer, default=0)
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
    )
    dataset = relationship(Dataset)
    wiki = relationship(
        u'WikiTrail',
        primaryjoin="and_(WikiTrailChange.wiki_id==WikiTrail.id,"
                    "WikiTrailChange.dataset_id==WikiTrail.dataset_id)",
        foreign_keys=[wiki_id, dataset_id],
        backref='changes',
    )


roles_users = db.Table(
    'roles_users',
    db.Column('registered_users_user', db.String(50),
              db.ForeignKey('registered_users.user')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')),
)


class RegisteredUser(Base, UserMixin):
    __tablename__ = 'registered_users'

    id = Column('user', String(50), primary_key=True)
    name = Column(String(255))
    institution = Column(String(45))
    abbrev = Column(String(10))
    MS = Column(String(255))
    email = Column(String(255))
    qualification = Column(String(255))
    account_date = Column(String(16), nullable=False)
    show_assessment = Column(Integer, nullable=False, default=1)
    active = Column(Boolean)
    confirmed_at = db.Column(db.DateTime())
    is_ldap = db.Column(Boolean, nullable=False, default=False)
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'),
    )
    password = db.Column(String(60))

    def has_role(self, role):
        return role in [r.name for r in self.roles]


class Role(Base, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False, unique=True)


@db_manager.option('alembic_args', nargs=argparse.REMAINDER)
def alembic(alembic_args):
    from alembic.config import CommandLine

    CommandLine().main(argv=alembic_args)


@db_manager.command
def revision(message=None):
    if message is None:
        message = raw_input('revision name: ')
    return alembic(['revision', '--autogenerate', '-m', message])


@db_manager.command
def upgrade(revision='head'):
    return alembic(['upgrade', revision])


@db_manager.command
def downgrade(revision):
    return alembic(['downgrade', revision])
