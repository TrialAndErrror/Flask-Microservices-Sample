from feeding_calc import db
import datetime
from decimal import Context
import math

STANDARD_SCOOP_RATIO = Context(prec=20).create_decimal(f'{1 / 60}')


class NutramigenCalculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calorie_density = db.Column(db.Float)
    total_volume = db.Column(db.Float)
    nutramigen_scoops = db.Column(db.Numeric(100, 4))
    nutramigen_grams = db.Column(db.Numeric(100, 4))
    volume_water = db.Column(db.String(20))

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, calorie_density, total_volume):
        super().__init__()
        self.calorie_density = int(calorie_density)
        self.total_volume = int(total_volume)

        # Calculate the amount of Nutramigen needed based on the calorie density and total volume
        result = calculate_scoops(
            output_volume=total_volume,
            calorie_density=calorie_density
        )

        self.nutramigen_scoops = result['scoops']
        self.nutramigen_grams = result['grams']
        self.volume_water = f'{result["input_water"]:.2f}'

    def serialize(self):
        return {
            "calorie_density": self.calorie_density,
            "total_volume": self.total_volume,
            "nutramigen_scoops": self.nutramigen_scoops,
            "nutramigen_grams": self.nutramigen_grams,
            "volume_water": self.volume_water
        }


def calculate_scoops(output_volume, calorie_density):
    """
    Calculate scoops required and water required to produce the volume and calorie density presented.

    :param output_volume: Total final volume of prepared formula
    :param calorie_density: Kcal/oz calorie density
    :return:
    """

    input_water = math.ceil((1200 * output_volume) / (7 * calorie_density + 1200))

    num_scoops = (calorie_density / 20) * (input_water / 60)

    grams_per_scoop = 7
    return {
        "scoops": num_scoops,
        "grams": num_scoops * grams_per_scoop,
        "input_water": input_water
    }
