from typing import List

from django.core.paginator import Paginator

from vehicles.models import Vehicle
from vehicles.entities import VehicleEntity
from vehicles.constants import VehicleListOrderBy


class VehicleRepositoryException(Exception):
    pass


class VehicleDoesNotExistRepositoryException(VehicleRepositoryException):
    pass


class VehicleRepository:
    def __init__(self):
        self.vehicle_manager = Vehicle.objects

    def get(self, id: int) -> VehicleEntity:
        try:
            vehicle = self.vehicle_manager.get(id=id)
        except Vehicle.DoesNotExist as e:
            raise VehicleDoesNotExistRepositoryException(str(e))

        return vehicle.as_entity()

    def list(
        self,
        order_by: VehicleListOrderBy = VehicleListOrderBy.ID,
        descending: bool = False,
        page: int = 1,
        limit: int = 100,
    ) -> List[VehicleEntity]:
        queryset = self.vehicle_manager.all().order_by(
            f"{'-' if descending else ''}{order_by}"
        )
        paginator = Paginator(queryset, limit)
        page = paginator.page(page)

        return [entity.as_entity() for entity in page.object_list]

    def create(self, vehicle: VehicleEntity) -> VehicleEntity:
        vehicle = Vehicle(
            ncap_year=vehicle.ncap_year,
            model_year=vehicle.model_year,
            make=vehicle.make,
            model=vehicle.model,
            drivetrain=vehicle.drivetrain,
            body_style=vehicle.body_style,
            engine_type=vehicle.engine_type,
            transmission_type=vehicle.transmission_type,
            front_track=vehicle.front_track,
            rear_track=vehicle.rear_track,
            average_track=vehicle.average_track,
            wheelbase=vehicle.wheelbase,
            test_weight=vehicle.test_weight,
            cg_long=vehicle.cg_long,
            cg_lat=vehicle.cg_lat,
            cg_height=vehicle.cg_height,
            stability_factor=vehicle.stability_factor,
            weight_distribution=vehicle.weight_distribution,
        )
        vehicle.save()

        return vehicle.as_entity()
