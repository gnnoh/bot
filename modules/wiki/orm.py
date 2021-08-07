from sqlalchemy import Column, String, Text, TIMESTAMP, text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base

from database.orm import engine, session

Base = declarative_base()
table_prefix = 'module_wiki_'


class WikiTargetSetInfo(Base):
    __tablename__ = table_prefix + 'TargetSetInfo'
    targetId = Column(String(512), primary_key=True)
    link = Column(Text)
    iws = Column(Text)
    headers = Column(Text)


class WikiInfo(Base):
    __tablename__ = table_prefix + 'WikiInfo'
    apiLink = Column(String(512), primary_key=True)
    siteInfo = Column(LONGTEXT if session.bind.dialect.name == 'mysql' else Text)
    timestamp = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))


Base.metadata.create_all(bind=engine, checkfirst=True)
