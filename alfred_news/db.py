import json
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

DBModelBase = declarative_base()
SessionMaker = None
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


def init_db():
    filepath = os.path.join(ROOT_PATH, '../data/news.sqlite')
    engine = create_engine('sqlite:///{}'.format(filepath))
    DBModelBase.metadata.bind = engine

    # TODO
    if not os.path.isfile(filepath):
        DBModelBase.metadata.create_all()
        # TODO
        # create_new_database()

    global SessionMaker
    SessionMaker = sessionmaker(engine)


def make_session():
    if SessionMaker is None:
        init_db()
    return SessionMaker()
