from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from logging.config import dictConfig


def create_app():
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

    app = Flask(__name__, template_folder="templates")
    CORS(app)
    # Set up a database connection
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/commands.db'

    db = SQLAlchemy(app)

    return app, db


app, db = create_app()