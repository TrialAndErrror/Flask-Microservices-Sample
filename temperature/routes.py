from flask import request, render_template, jsonify
import datetime
import os
import pytz
from flask_cors import cross_origin

from temperature.models.report import Report, get_reports, make_report
from temperature.models.message import parse_request_data

from . import app, db

# Create the database tables if they don't already exist
with app.app_context():
    db.create_all()


def datetimefilter(value, format='%m/%d/%Y | %H:%M:%S'):
    tz = pytz.timezone('US/Eastern')
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)


app.jinja_env.filters['datetimefilter'] = datetimefilter


@app.route("/data", methods=['GET'])
@cross_origin()
def get_data():
    reports = [item.serialize() for item in Report.query.all()]
    response = jsonify(reports)
    return response


@app.route('/', methods=['GET', 'POST'])
def all_data():
    # Get all entries from the database
    reports = Report.query.all()
    date = None

    if request.method == 'POST':
        # Get the JSON data from the request body
        if date := request.form.get('date'):
            date_str = datetime.datetime.strptime(date, '%Y-%m-%d')

            reports = get_reports(date_str)
            date = date_str

    # Render the template with the commands
    return render_template('entryList.html', reports=reports, date=date)


# Set up a route to receive POST requests at the /commands endpoint
@app.route('/message', methods=['GET', 'POST'])
def receive_message():
    """ Receive command and process """

    """
    Command:
        {
            'temperature': float
            'humidity': str
        }
    """
    if request.method == 'POST':
        # Get the JSON data from the request body
        message = parse_request_data(request.get_json())
        print(message)

        response = make_report(message.temperature, message.humidity)

        return jsonify(response)


@app.route('/api', methods=['POST'])
def api_request():
    if request.method == 'POST':
        json_data = request.get_json()
        # Currently params are unused, returning all data for debug purposes
        parameters = json_data.get('params')
        return jsonify(Report.query.all())


def run_app():
    port = os.environ.get("TEMPERATURE_PORT")
    debug = os.environ.get("DEBUG")
    print(f"Running Temperature on {port} {'in debug mode' if debug else ''}")
    app.run(port=port, debug=debug)


if __name__ == '__main__':
    run_app()

