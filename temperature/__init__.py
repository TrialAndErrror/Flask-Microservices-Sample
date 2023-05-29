import os
from logging.config import dictConfig

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask


def default_app_factory():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    app = Flask(__name__, template_folder="templates", static_folder="static")

    return app


app = default_app_factory()

# FIXME: Remove CORS and limit access
"""
Shouldn't need CORS on the temperature endpoint, it's really supposed to just talk to the API.
Remove this and make sure this container only communicates with Handler only.
"""
CORS(app)

# Set up a database connection
pg_user = os.environ.get('POSTGRES_USER')
pg_pass = os.environ.get('POSTGRES_PASS')
pg_host = os.environ.get('POSTGRES_HOST')
pg_port = os.environ.get('POSTGRES_PORT')

PROD_DB = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/temperature.db'
db = SQLAlchemy(app)



