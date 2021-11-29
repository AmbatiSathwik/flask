import datetime
import random
import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext

# user = "web"
# password = "123"
host = "ec2-3-95-130-249.compute-1.amazonaws.com"


def get_db():
    if 'db' not in g:
        url = current_app.config['URL']
        dbname = url.path[1:]
        user = url.username
        password = url.password
        #host = url.
        # dbname = "hms"
        g.db = psycopg2.connect(dbname=dbname,
            user=user,
            password=password,
            host=host
            )
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    f = current_app.open_resource('sql/000_create.sql')
    sql_code = f.read().decode('ascii')
    cur = db.cursor()
    cur.execute(sql_code)
    cur.close()
    db.commit()
    close_db()


@click.command('initdb', help='database initializing')
@with_appcontext
def db_command():
    init_db()
    click.echo('Database initialized')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(db_command)