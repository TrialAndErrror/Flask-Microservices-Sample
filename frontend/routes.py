import datetime
import os
import requests
from flask import request, render_template, jsonify
import matplotlib.pyplot as plt

from . import app
from flask_htmx import HTMX


htmx = HTMX(app)


def send_message_and_receive_response(data_category, parameters: dict or None):
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
#     return {}, 405


# Set up a route to receive POST requests at the /commands endpoint
@app.route('/', methods=['GET', 'POST'])
def receive_command():
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

