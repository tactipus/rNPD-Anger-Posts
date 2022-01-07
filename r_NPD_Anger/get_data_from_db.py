import sqlite3
from flask import g
import sys
sys.path.append('//')
from r_NPD_Anger.__init__ import create_app

DATABASE = '/Users/pnalzate/Documents/GitHub/Server/instance/r_NPD_Anger.sqlite'
app = create_app()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


with app.app_context():
    db = get_db()

db.row_factory = make_dicts


def query_db(query, args=(), one=False):
    with app.app_context():
        cur = get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
    return (rv[0] if rv else None) if one else rv


def email_getter():
    emails = {}
    key = 0

    for email in query_db('select * from email'):
        emails[key] = email[1]
        key += 1

    return emails
