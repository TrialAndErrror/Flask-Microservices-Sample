from feeding_calc import db
import datetime
from decimal import Context


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
        self.calorie_density = calorie_density
        self.total_volume = total_volume

        # Calculate the amount of Nutramigen needed based on the calorie density and total volume
        scoops, grams, volume_water = calculate_scoops(
            volume=total_volume,
            calorie_density=calorie_density
        )

        self.nutramigen_scoops = scoops
        self.nutramigen_grams = grams
        self.volume_water = f'{volume_water:.2f}'


def calculate_scoops(volume, calorie_density):
    """
    Calculate scoops required and water required to produce the volume and calorie density presented.

    :param volume:
    :param calorie_density:
    :return:
    """

    calories_per_ml = calorie_density / 30

    volume_of_water = volume - ((7/45) * volume * calories_per_ml)
    num_of_scoops = (volume * calories_per_ml) / 45

    num_of_grams = 9 * num_of_scoops

    return num_of_scoops, num_of_grams, volume_of_water
