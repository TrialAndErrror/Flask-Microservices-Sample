from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os


app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Set up a database connection
def get_env_variables():
    pg_user = os.environ.get('POSTGRES_USER')
    pg_pass = os.environ.get('POSTGRES_PASSWORD')
    pg_host = os.environ.get('POSTGRES_DB')
    pg_port = os.environ.get('POSTGRES_PORT')

    if not pg_user or pg_user == "":
        raise EnvironmentError('PG User Not Set')

    if not pg_pass or pg_pass == "":
        raise EnvironmentError('PG Password Not Set')

    if not pg_host or pg_host == "":
        raise EnvironmentError('PG Host Not Set')

    if not pg_port or pg_port == "":
        raise EnvironmentError("PG Port Not Set")

    return f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}'


DB_URL = get_env_variables()

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)


