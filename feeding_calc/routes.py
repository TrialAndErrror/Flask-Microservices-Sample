from flask import request, render_template, jsonify

from dotenv import load_dotenv
import os
from feeding_calc import app, db
from feeding_calc.models.VolumeRequest import VolumeRequest
from feeding_calc.models.NutramigenCalculation import NutramigenCalculation
from flask_cors import cross_origin

load_dotenv(dotenv_path=".env")

# Need to import your models before creating database
with app.app_context():
    db.create_all()


def save_volume_request(calories: int, volume: int):
    if not calories:
        return dict(
            message='Missing Calorie Density',
            success=False
        )
    if not volume:
        return dict(
            message='Missing Final Volume',
            success=False
        )

    new_entry = VolumeRequest(
        calorie_density=calories,
        final_volume=volume
    )

    db.session.add(new_entry)
    db.session.commit()

    return dict(
        success=True,
        message=f"Successfully created Volume Request ({volume} @ {calories} cal)"
    )


def save_calculation(calorie_density: int, total_volume: int):
    # Create a new NutramigenCalculation entry
    calculation = NutramigenCalculation(calorie_density=calorie_density, total_volume=total_volume)

    # Add the calculation to the database session
    db.session.add(calculation)

    # Commit the transaction
    db.session.commit()

    return calculation


@app.route("/data", methods=['GET'])
@cross_origin()
def get_data():
    query = NutramigenCalculation.query.order_by(
        NutramigenCalculation.created_at.desc()
    )
    reports = [item.serialize() for item in query.all()]
    response = jsonify(reports)
    return response


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def all_data():
    if request.method == 'POST':
        if request.form.get("_method") == "DELETE":
            # Delete all NutramigenCalculation entries
            NutramigenCalculation.query.delete()

            # Commit the transaction
            db.session.commit()
        else:
            save_calculation(
                int(request.form['calorie_density']),
                int(request.form['total_volume']),
            )

    # Get the list of calculations from the database
    calculations = NutramigenCalculation.query.all()
    # Render the template and pass the calculations to the template context
    return render_template('index.html', calculations=calculations)


# Set up a route to receive POST requests at the /commands endpoint
@app.route('/message', methods=['GET', 'POST'])
def receive_command():
    """ Receive command and process """

    """
    Command:
        {
            'calories': float
            'volume': float
        }
    """

    if request.method == 'POST':
        if request.form.get("_method") == "DELETE":
            # Delete all VolumeRequest entries
            VolumeRequest.query.delete()

            # Commit the transaction
            db.session.commit()
        else:
            # Get the JSON data from the request body
            data = request.get_json()

            calories = int(data['calories'])
            volume = int(data['volume'])

            # Create a new Command object and save it to the database
            save_request = save_volume_request(
                calories=calories,
                volume=volume
            )

            if save_request.get('success'):
                formula_calc = save_calculation(
                    calorie_density=calories,
                    total_volume=volume
                )
                # calculate volume

                response = dict(
                    success=True,
                    message=f"{formula_calc.nutramigen_scoops:.2f} scoops ({formula_calc.nutramigen_grams:.2f}g) of powder required to make {formula_calc.total_volume:.0f} mL of formula @ {formula_calc.calorie_density:.0f} cal"
                )

                return jsonify(response)

            else:
                return jsonify(save_request)

    volume_requests = VolumeRequest.query.all()

    return render_template('requests.html', volume_requests=volume_requests)


def run_app():
    port = os.environ.get("FEEDING_CALC_PORT")
    debug = os.environ.get("DEBUG")
    print(f"Running Feeding Calc on {port} {'in debug mode' if debug else ''}")
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    run_app()

