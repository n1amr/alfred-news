import json
import os

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from .db import DBModelBase, make_session, ROOT_PATH


class Source(DBModelBase):
    __tablename__ = 'source'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    url = Column(String(256), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))

    def __init__(self, name, url, category=None):
        self.name = name
        self.url = url
        self.category = category

    @staticmethod
    def create(name, url):
        s = Source(name, url)
        session = make_session()
        session.add(s)
        session.commit()
        session.close()


class Category(DBModelBase):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    sources = relationship(Source, backref='category')

    def __init__(self, name):
        self.name = name

    @staticmethod
    def create(name):
        c = Category(name)
        session = make_session()
        session.add(c)
        session.commit()
        session.close()


def create_new_database():
    with open(os.path.join(ROOT_PATH, 'resources', 'sample_data.json'), 'r') as f:
        sample_data = json.loads(f.read())

    session = make_session()
    for category, sources in sample_data.items():
        category_obj = Category(name=category)
        for source_name, source_url in sources:
            source_obj = Source(source_name, source_url, category_obj)
            session.add(source_obj)
        session.add(category_obj)
    session.commit()
