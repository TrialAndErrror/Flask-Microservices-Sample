from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


app = Flask(__name__, template_folder="templates", static_folder="static")

# Set up a database connection
pg_user = os.environ.get('POSTGRES_USER')
pg_pass = os.environ.get('POSTGRES_PASS')
pg_host = os.environ.get('POSTGRES_HOST')
pg_port = os.environ.get('POSTGRES_PORT')

PROD_DB = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}'
app.config['SQLALCHEMY_DATABASE_URI'] = PROD_DB

db.init_app(app)
