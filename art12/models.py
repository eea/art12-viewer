# coding: utf-8
import argparse
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, Integer, Numeric, String, Text, text, \
    ForeignKey
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

    def _season(self, season):
        return {field: getattr(self, field + season, None) for field in
                SEASON_FIELDS}

    @property
    def bs(self):
        return self._season('_bs')

    @property
    def ws(self):
        return self._season('_ws')


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
