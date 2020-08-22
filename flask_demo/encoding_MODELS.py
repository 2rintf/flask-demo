# coding: utf-8
from sqlalchemy import Column, Integer, JSON, String
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class EncodingTable(Base):
    __tablename__ = 'encoding_table'

    name = Column(VARCHAR(100), nullable=False)
    id = Column(Integer, primary_key=True, unique=True)
    encoding = Column(JSON, nullable=False)


class ModelInfo(Base):
    __tablename__ = 'model_info'

    id = Column(INTEGER, primary_key=True, unique=True)
    name = Column(String(45), nullable=False)
    sex = Column(TINYINT(1), nullable=False)
    pic_path = Column(String(255))
    black_hair = Column(TINYINT(1), nullable=False)
