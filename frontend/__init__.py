from logging.config import dictConfig
from flask import Flask
from dotenv import load_dotenv
import os


load_dotenv()
HANDLER_ENDPOINT = os.getenv("HANDLER_URL", f'http://handler:8000/api')


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
