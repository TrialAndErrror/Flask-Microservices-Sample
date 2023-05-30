import json

from handler import db


class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(200), nullable=False)
    data = db.Column(db.BLOB, nullable=False)

    def __init__(self, command, data):
        self.command = command
        self.data = json.dumps(data)

    @property
    def data(self):
        return json.loads(self.data_json)

    @data.setter
    def data(self, value):
        self.data_json = json.dumps(value)

    def __repr__(self):
        return '<Command %r>' % self.command
