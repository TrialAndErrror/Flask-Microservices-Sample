from logging.config import dictConfig

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def feeding_calc_app_factory():
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


app = feeding_calc_app_factory()

# Set up a database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/feeding_calc.db'

db.init_app(app)
