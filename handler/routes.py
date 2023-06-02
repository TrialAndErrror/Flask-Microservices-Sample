import json
import os
import requests
from flask import request, render_template, jsonify

from handler.models.command import Command
from . import app, db


AUTHORIZED_COMMANDS = [
    "feeding_calc",
    "temperature",
    "journal"
    "frontend"
]

# Create the database tables if they don't already exist
with app.app_context():
    db.create_all()


def send_message_and_receive_response(data, service: str):
    endpoint = f'http://{service}:8000/message'
    response = requests.post(url=endpoint, json=data)

    response_data = response.json()

    if response_data.get('success'):
        return jsonify(response_data)
    else:
        return jsonify(response_data)


@app.route("/message", methods=['GET'])
def receive_message():
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Access the data as a dictionary
    command = json_data.get('command')
    data = json_data.get('data')

    # Create a new Command object and save it to the database
    new_command = Command(command=command, data=json.dumps(data))
    db.session.add(new_command)
    db.session.commit()

    if command not in AUTHORIZED_COMMANDS:
        return {"error": f"Not an installed command ({command}). Please enable the feature and try again."}

    endpoint = f'http://{command}:8000/message'
    response = requests.post(url=endpoint, json=data)

    response_data = response.json()

    if response_data.get('success'):
        return jsonify(response_data)
    else:
        return jsonify(response_data)


# Set up a route to receive POST requests at the /commands endpoint
@app.route('/api', methods=['POST'])
def receive_api_request():
    """ Receive an API request and dispatch accordingly"""

    """
        Command Format:
        {
            'source': 'frontend'
            'data': {}
        }
        
        Frontend Data:
            {
                'name': str
                'params': dict or None
            }
    """
    if request.method == 'POST':
        # Get the JSON data from the request body
        json_data = request.get_json()

        # Access the data as a dictionary
        request_source = json_data.get('source')
        data = json_data.get('data')

        if request_source == "frontend":
            target_service = data.get("name")
            params = {}
            if request_params := data.get("params"):
                params.update(request_params)

            endpoint = f'http://{target_service}:8000/api'

            response = requests.post(url=endpoint, json=params)

            response_data = response.json()

            return jsonify(response_data)


# Set up a route to receive POST requests at the /commands endpoint
@app.route('/', methods=['GET', 'POST'])
def receive_command():
    """ Receive command and dispatch accordingly"""

    """
    Command Format:
        {
            'command': 'calc' | 'journal'
            'data': {}
        }
        
    Calc Data:
        {
            'calories': float
            'volume': float
        }
        
    Journal Data:
        {
            'entry_type': str
            'amount': float
            'name': str
        }
        

    """

    if request.method == 'POST':
        # Get the JSON data from the request body
        json_data = request.get_json()

        # Access the data as a dictionary
        command = json_data.get('command')
        data = json_data.get('data')

        # Create a new Command object and save it to the database
        new_command = Command(command=command, data=data)
        db.session.add(new_command)
        db.session.commit()

        return send_message_and_receive_response(data, command)
    else:
        # Get all commands from the database
        commands = Command.query.all()

        # Render the template with the commands
        return render_template('commands.html', commands=commands)


def run_app():
    port = os.environ.get("HANDLER_PORT")
    debug = os.environ.get("DEBUG")
    print(f"Running Handler on {port} {'in debug mode' if debug else ''}")
    app.run(port=port, debug=debug)


if __name__ == '__main__':
    run_app()

