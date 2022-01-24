from factory.django import DjangoModelFactory

from vehicles.models import Vehicle
from vehicles.constants import VehicleDrivetrainTypes, VehicleBodyStyles


class VehicleFactory(DjangoModelFactory):
    class Meta:
        model = Vehicle

    ncap_year = 2004
    model_year = 2003
    make = "Toyota"
    model = "Tacoma XCab SR5"
    drivetrain = VehicleDrivetrainTypes.FOUR_WD
    body_style = VehicleBodyStyles.PICKUP
    engine_type = "2.7 I4"
    transmission_type = "Auto"
    front_track = 59.3
    rear_track = 59.0
    average_track = 59.1
    wheelbase = 122.6
    test_weight = 3833.9
    cg_long = 50.5
    cg_lat = -1.3
    cg_height = 26.33
    stability_factor = 1.123
    weight_distribution = 0.588091354
