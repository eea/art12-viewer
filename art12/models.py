# coding: utf-8
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager

db = SQLAlchemy()
db_manager = Manager()
