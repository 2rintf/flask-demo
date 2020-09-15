# coding: utf-8
# from sqlalchemy import Column, String
# from sqlalchemy.dialects.mysql import INTEGER, TINYINT
# from sqlalchemy.ext.declarative import declarative_base

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_demo import db


class EncodingTable(db.Model):
    __tablename__ = 'encoding_table'

    name = db.Column(db.String(100), nullable=False)
    id = db.Column(db.INTEGER, primary_key=True, unique=True)
    encoding = db.Column(db.JSON, nullable=False)

    def __init__(self, name, encoding):
        self.name = name
        self.encoding = encoding

    def __repr__(self):
        return '<User %r>' % self.name


class ModelInfo(db.Model):
    __tablename__ = 'model_info'

    # todo:2020年9月14日14点35分 数据库model_info表添加了新的列值此处还未修改！
    id = db.Column(db.INTEGER, primary_key=True, unique=True)
    name = db.Column(db.String(45), nullable=False)
    sex = db.Column(db.BOOLEAN, nullable=False)
    pic_path = db.Column(db.String(255))
    black_hair = db.Column(db.BOOLEAN, nullable=False)

    def __init__(self, name, sex, pic_path, blac_hair):
        self.name = name
        self.sex = sex
        self.pic_path = pic_path
        self.black_hair = blac_hair

    def __repr__(self):
        return '<User %r>' % self.name
