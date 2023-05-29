from flask import request, render_template, jsonify
import datetime
from dotenv import load_dotenv
import os

from journal.models.food import Food, make_food, get_foods
from journal.models.water import Water, make_water, get_waters
from journal.models.message import parse_request_data

from . import app, db

load_dotenv(dotenv_path=".env")

# Create the database tables if they don't already exist
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def all_data():
    # Get all entries from the database
    foods = Food.query.all()
    waters = Water.query.all()
    date = None

    if request.method == 'POST':
        # Get the JSON data from the request body
        if date := request.form.get('date'):
            date_str = datetime.datetime.strptime(date, '%Y-%m-%d')

            foods = get_foods(date_str)
            waters = get_waters(date_str)
            date = date_str

    # Render the template with the commands
    return render_template('entryList.html', foods=foods, waters=waters, date=date)


# Set up a route to receive POST requests at the /commands endpoint
@app.route('/message', methods=['GET', 'POST'])
def receive_message():
    """ Receive command and process """

    """
    Command:
        {
            'entry_type': str
            'amount': float
            'name': str
        }
    """
    if request.method == 'POST':
        # Get the JSON data from the request body
        message = parse_request_data(request.get_json())

        match message.entry_type:
            case "food":
                response = make_food(message.amount, message.name)

            case "drink":
                response = make_water(message.amount)
            case _:
                response = dict(
                    success=False,
                    message=f"Unknown command type {message.entry_type}; data not saved."
                )

        return jsonify(response)


@app.route('/food', methods=['GET', 'POST'])
def food():
    if request.method == 'POST':
        # Get the JSON data from the request body
        make_food(
            amount=request.form['amount'],
            name=request.form.get("name", "")
        )

    foods = Food.query.all()

    return render_template('food.html', foods=foods)


@app.route('/water', methods=['GET', 'POST'])
def water():
    if request.method == 'POST':
        # Get the JSON data from the request body
        make_water(amount=request.form['amount'])

    waters = Water.query.all()

    return render_template('water.html', waters=waters)


@app.route('/api', methods=['POST'])
def api_request():
    if request.method == 'POST':
        json_data = request.get_json()
        # Currently params are unused, returning all data for debug purposes
        parameters = json_data.get('params')

        all_data = {
            "food": Food.query.all(),
            "water": Water.query.all()
        }
        return jsonify(all_data)


def run_app():
    port = os.environ.get("JOURNAL_PORT")
    debug = os.environ.get("DEBUG")
    print(f"Running Journal on {port} {'in debug mode' if debug else ''}")
    app.run(port=port, debug=debug)


if __name__ == '__main__':
    run_app()

