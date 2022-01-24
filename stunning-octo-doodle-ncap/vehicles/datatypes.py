from attrs import define, asdict


@define(kw_only=True)
class VehicleServiceCreateArgs:
    ncap_year: int
    model_year: int

    make: str
    model: str

    drivetrain: str
    body_style: str
    engine_type: str
    transmission_type: str

    front_track: float
    rear_track: float
    average_track: float
    wheelbase: float

    test_weight: float

    cg_long: float
    cg_lat: float
    cg_height: float

    def as_dict(self):
        return asdict(self)
