from sqlalchemy import Column, String, Text, TIMESTAMP, text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base

from database.orm import DBSession

Base = declarative_base()
table_prefix = 'module_wiki_'
db = DBSession()
session = db.session
engine = db.engine


class WikiTargetSetInfo(Base):
    __tablename__ = table_prefix + 'TargetSetInfo'
    targetId = Column(String(512), primary_key=True)
    link = Column(LONGTEXT if session.bind.dialect.name == 'mysql' else Text)
    iws = Column(LONGTEXT if session.bind.dialect.name == 'mysql' else Text)
    headers = Column(LONGTEXT if session.bind.dialect.name == 'mysql' else Text)


class WikiInfo(Base):
    __tablename__ = table_prefix + 'WikiInfo'
    apiLink = Column(String(512), primary_key=True)
    siteInfo = Column(LONGTEXT if session.bind.dialect.name == 'mysql' else Text)
    timestamp = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))


Base.metadata.create_all(bind=engine, checkfirst=True)
