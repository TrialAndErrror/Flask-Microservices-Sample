from logging.config import dictConfig

from flask_sqlalchemy import SQLAlchemy
from flask import Flask


def journal_app_factory():
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


app = journal_app_factory()

# FIXME: This makes little to no sense
# Set up a database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/commands.db'
db = SQLAlchemy(app)

# Set up a database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/journal.db'
db = SQLAlchemy(app)



