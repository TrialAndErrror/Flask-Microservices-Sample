import datetime
import os
import requests
from flask import request, render_template, jsonify, abort

from . import app
from flask_htmx import HTMX


htmx = HTMX(app)


NO_DATA_CHART_IMAGE = "https://user-images.githubusercontent.com/15953522/49493502-63e21d00-f882-11e8-911c-1d7655f393e8.png"


def send_message_and_receive_response(data_category, parameters: dict or None = None):
    if parameters is None:
        parameters = {}

    endpoint = f'http://handler:8000/api'

    message_data = {
        "name": data_category,
        "params": parameters
    }

    message = dict(
        source="frontend",
        data=message_data
    )

    response = requests.post(url=endpoint, json=message)

    response_data = response.json()

    if response_data.get('success'):
        return jsonify(response_data)
    else:
        return jsonify(response_data)

"""
Disabled for errors:
ImportError: libstdc++.so.6: cannot open shared object file: No such file or directory
"""
# @app.route("/htmx/temperature", methods=['GET', 'POST'])
# def make_temp_chart():
#     if htmx:
#         # Generate your chart using Matplotlib
#         x = [1, 2, 3, 4, 5]
#         y = [10, 20, 30, 40, 50]
#         plt.plot(x, y)
#         plt.xlabel('X-axis')
#         plt.ylabel('Y-axis')
#
#         # Save the chart as an image file
#         chart_file = f'/chart_{datetime.datetime.utcnow().isoformat()}'  # Replace with the desired file path
#         plt.savefig(chart_file)
#
#         # Pass the file path to the template
#         return render_template('services/temperature/chart.html', chart_file=chart_file)
#     abort(405)


def render_template_with_data(template_location: str, service_name: str, human_readable_service_name: str):
    failed = False
    error_message = ""

    try:
        data = send_message_and_receive_response(service_name)
    except requests.exceptions.ConnectionError:
        data = []
        failed = True
        error_message = f"The frontend {human_readable_service_name} page isn't able to connect to the handler service, " \
                        f"so check the logs of the '{service_name}' service to see why the request failed."

    return render_template(
        template_location,
        data=data,
        chart_file=NO_DATA_CHART_IMAGE,
        failed=failed,
        error_message=error_message,
        service_name=human_readable_service_name
    )


@app.route("/temperature", methods=['GET', 'POST'])
def temperature_dashboard():
    return render_template_with_data(
        template_location="services/temperature/dashboard.html",
        service_name="temperature",
        human_readable_service_name="Temperature Sensor"
    )


@app.route("/feeding", methods=['GET', 'POST'])
def feeding_calc_dashboard():
    return render_template_with_data(
        template_location="services/feeding_calc/dashboard.html",
        service_name="feeding_calc",
        human_readable_service_name="Feeding Calculator"
    )

# Set up a route to receive POST requests at the /commands endpoint
@app.route('/', methods=['GET', 'POST'])
def home():
    """ Receive command and dispatch accordingly"""

    """
    Command Format:
        {
            'name': ''
            'parameters': {} or None
        }
        
    """

    if request.method == 'POST':
        # Get the JSON data from the request body
        json_data = request.get_json()

        # Access the data as a dictionary
        data_category = json_data.get('name')
        parameters = json_data.get('parameters')
        return send_message_and_receive_response(data_category, parameters)
    else:
        # Get all commands from the database
        # commands = Command.query.all()

        # Render the template with the commands
        # return render_template('commands.html', commands=commands)
        return render_template('home/home.html')


def run_app():
    port = os.environ.get("FRONTEND_PORT")
    debug = os.environ.get("DEBUG")
    print(f"Running Frontend on {port} {'in debug mode' if debug else ''}")
    app.run(port=port, debug=debug)


if __name__ == '__main__':
    run_app()

