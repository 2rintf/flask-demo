from flask_sqlalchemy import SQLAlchemy





# # import sqlite3
#
# import pymysql
# from flask_sqlalchemy import SQLAlchemy
#
# import click
# from flask import current_app,g
# from flask.cli import with_appcontext
#
# from config import config
#
#
# def get_db():
#     if 'db' not in g:
#         g.db = pymysql.connect(
#
#         )
#         g.db.row_factory = sqlite3.Row
#
#     return g.db
#
# def close_db(e=None):
#     db = g.pop('db',None)
#     if db is not None:
#         db.close()
#
#
# def init_db():
#     db = get_db()
#
#     with current_app.open_resource('model.sql') as f:
#         db.executescript(f.read().decode('utf-8'))
#
#
# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     init_db()
#     click.echo('Init the database.')
#
#
# def init_app(app):
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)