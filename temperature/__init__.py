import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Set up a database connection
pg_user = os.environ.get('POSTGRES_USER')
pg_pass = os.environ.get('POSTGRES_PASSWORD')
pg_host = os.environ.get('POSTGRES_DB')
pg_port = os.environ.get('POSTGRES_PORT')

PROD_DB = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}'

app.config['SQLALCHEMY_DATABASE_URI'] = PROD_DB
db = SQLAlchemy(app)



