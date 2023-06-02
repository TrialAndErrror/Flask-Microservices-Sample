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


def calculate_scoops(volume: str, calorie_density: str):
    """
    Calculate scoops required and water required to produce the volume and calorie density presented.

    :param volume:
    :param calorie_density:
    :return:
    """

    """
    Write a formula that calculates the amount of Nutramigen powder and volume of water to mix to make a target volume 
    and calorie density. One scoop of powder adds 7 mL of total volume. One scoop of powder with 60 mL of water makes a
    calorie density of 20. 
    
    total_volume = volume_of_water +  (7mL * scoops required)
    
    Calorie density results from 1 scoop / 60mL at 20 calories; higher calorie densities can be calculated by dividing
    the target density by 20 and multiplying the ratio by this scoop to volume ratio
    """
    # calorie_density_ratio = (
    #      Context(prec=20).create_decimal(calorie_density)
    #      / Context(prec=20).create_decimal('20')
    # )

    """
    Custom scoop ratio determines how many scoops to mix with 60 mL of water to make formula
    """
    # custom_scoop_ratio = calorie_density_ratio * STANDARD_SCOOP_RATIO

    """
    Adjusted volume total is how much volume of mixed formula results from mixing up 60 mL of formula
    """
    # adjusted_volume_total = 60 + (7 * custom_scoop_ratio)

    ratio = Context(prec=4).create_decimal(calorie_density) / Context(prec=4).create_decimal('20')

    # Adjust volume to compensate for added volume of powder in formula
    adjusted_volume = Context(prec=10).create_decimal(volume) * (Context(prec=10).create_decimal('.9') * ratio)

    # volume_of_water = volume - (7 * ratio * volume / 60)

    scoops_to_water = ratio / Context(prec=10).create_decimal('60')

    scoops = scoops_to_water * adjusted_volume

    grams = Context(prec=10).create_decimal('9') * scoops

    return scoops, grams, adjusted_volume

