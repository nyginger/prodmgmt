# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy, BaseQuery
import sqlite3
import os


app=Flask(__name__)


APP_ROOT= os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + APP_ROOT + os.sep + 'DATABASE.db'
app.config['SECRET_KEY']='Sskieeutkwitlkg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config.from_pyfile('config.cfg')

db=SQLAlchemy(app)

conn=sqlite3.connect(APP_ROOT+os.sep+'DATABASE.db', check_same_thread=False)
cur=conn.cursor()


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    c = cur.execute(query, args)
    conn.commit()
    rv = [dict((c.description[idx][0], value)
               for idx, value in enumerate(row)) for row in c.fetchall()]
    return (rv[0] if rv else None) if one else rv

