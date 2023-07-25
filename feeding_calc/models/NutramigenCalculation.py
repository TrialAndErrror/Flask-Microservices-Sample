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
    ratio = Context(prec=4).create_decimal(calorie_density) / Context(prec=4).create_decimal('20')

    # Adjust volume to compensate for added volume of powder in formula
    adjusted_volume = Context(prec=10).create_decimal(volume) * (Context(prec=10).create_decimal('.9') * ratio)

    scoops_to_water = ratio / Context(prec=10).create_decimal('60')

    total_num_scoops = scoops_to_water * adjusted_volume

    grams = Context(prec=10).create_decimal('9') * total_num_scoops

    return total_num_scoops, grams, adjusted_volume

