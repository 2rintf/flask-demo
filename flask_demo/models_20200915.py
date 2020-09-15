# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


# todo:修改成__init__.py里面的db.
# db = SQLAlchemy()

from flask_demo import db


class EncodingTable(db.Model):
    __tablename__ = 'encoding_table'

    name = db.Column(db.String(100, 'utf8mb4_0900_ai_ci'), nullable=False)
    id = db.Column(db.Integer, primary_key=True, unique=True)
    pic_path = db.Column(db.String(100, 'utf8mb4_0900_ai_ci'))
    encoding = db.Column(db.JSON, nullable=False)
    attr_encoding = db.Column(db.JSON, nullable=False)



class ModelInfo(db.Model):
    __tablename__ = 'model_info'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(45), nullable=False)
    sex = db.Column(db.Integer, nullable=False)
    pic_path = db.Column(db.String(255))
    encoding = db.Column(db.JSON, nullable=False)
    black_hair = db.Column(db.Integer, nullable=False)
    blond_hair = db.Column(db.Integer, nullable=False)
    brown_hair = db.Column(db.Integer, nullable=False)
    bald = db.Column(db.Integer, nullable=False)
    bangs = db.Column(db.Integer, nullable=False)
    recending_hairline = db.Column(db.Integer, nullable=False)
    straight_hair = db.Column(db.Integer, nullable=False)
    wavy_hair = db.Column(db.Integer, nullable=False)
    goatee = db.Column(db.Integer, nullable=False)
    mustache = db.Column(db.Integer, nullable=False)
    no_beard = db.Column(db.Integer, nullable=False)
    pale_skin = db.Column(db.Integer, nullable=False)
    arched_eyebrows = db.Column(db.Integer, nullable=False)
    bags_under_eyes = db.Column(db.Integer, nullable=False)
    bushy_eyebrows = db.Column(db.Integer, nullable=False)
    eye_glasses = db.Column(db.Integer, nullable=False)
    narrow_eyes = db.Column(db.Integer, nullable=False)
