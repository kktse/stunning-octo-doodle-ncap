import math

from attrs import define, field, validators, asdict, evolve, cmp_using
from typing import Any, Dict, TypeVar

from vehicles.constants import VehicleBodyStyles, VehicleDrivetrainTypes

T = TypeVar("T", bound="VehicleEntity")


@define(kw_only=True)
class VehicleEntity:
    id: int = field(default=None)

    ncap_year: int = field(converter=int, validator=[validators.gt(0)])
    model_year: int = field(converter=int, validator=[validators.gt(0)])

    make: str = field(validator=[validators.max_len(128)])
    model: str = field(validator=[validators.max_len(256)])

    drivetrain: str = field(validator=[validators.in_(VehicleDrivetrainTypes.KEYS)])
    body_style: str = field(validator=[validators.in_(VehicleBodyStyles.KEYS)])
    engine_type: str = field(validator=[validators.max_len(128)])
    transmission_type: str = field(validator=[validators.max_len(128)])

    front_track: float = field(converter=float, validator=[validators.gt(0)])
    rear_track: float = field(converter=float, validator=[validators.gt(0)])
    average_track: float = field(converter=float, validator=[validators.gt(0)])
    wheelbase: float = field(converter=float, validator=[validators.gt(0)])

    test_weight: float = field(converter=float, validator=[validators.gt(0)])

    cg_long: float = field(converter=float, validator=[validators.gt(0)])
    cg_lat: float = field(converter=float)
    cg_height: float = field(converter=float, validator=[validators.gt(0)])

    stability_factor: float = field(
        default=None,
        validator=[validators.optional(validators.gt(0))],
        eq=cmp_using(eq=lambda a, b: math.isclose(a, b, abs_tol=1e-3)),
    )
    weight_distribution: float = field(
        default=None,
        validator=[
            validators.optional(validators.gt(0)),
            validators.optional(validators.lt(1)),
        ],
        eq=cmp_using(eq=lambda a, b: math.isclose(a, b, abs_tol=1e-3)),
    )

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def compute_derived_attributes(self: T) -> T:
        attribute_to_computation_map = {
            "stability_factor": self._compute_stability_factor,
            "weight_distribution": self._compute_weight_distribution,
        }

        entity = self
        for (attribute, method) in attribute_to_computation_map.items():
            if not getattr(self, attribute):
                entity = evolve(entity, **{attribute: method()})

        return entity

    def _compute_stability_factor(self) -> float:
        # Static stability factor is defined as SSF = T/2h
        return 0.5 * self.average_track / self.cg_height

    def _compute_weight_distribution(self) -> float:
        # Weight distribution is ratio of the total weight on the front axle
        return 1 - (self.cg_long / self.wheelbase)
