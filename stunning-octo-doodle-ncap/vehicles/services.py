from typing import List, Optional

from vehicles.constants import VehicleListOrderBy
from vehicles.datatypes import VehicleServiceCreateArgs
from vehicles.repositories import (
    VehicleRepository,
    VehicleDoesNotExistRepositoryException,
)
from vehicles.entities import VehicleEntity


class VehicleServiceException(Exception):
    pass


class VehicleDoesNotExistServiceException(VehicleServiceException):
    pass


class VehicleCreateValidationServiceException(VehicleServiceException):
    pass


class VehicleService:
    def __init__(self, vehicle_repository: Optional[VehicleRepository] = None) -> None:
        self.vehicle_repository = vehicle_repository or VehicleRepository()

    def get(self, id: int) -> VehicleEntity:
        try:
            vehicle = self.vehicle_repository.get(id=id)
        except VehicleDoesNotExistRepositoryException as e:
            raise VehicleDoesNotExistServiceException(str(e))

        return vehicle

    def list(
        self,
        order_by: VehicleListOrderBy = VehicleListOrderBy.ID,
        descending: bool = False,
        page: int = 1,
        limit: int = 100,
    ) -> List[VehicleEntity]:
        vehicles = self.vehicle_repository.list(
            order_by=order_by, descending=descending, page=page, limit=limit
        )

        return vehicles

    def create(self, args: VehicleServiceCreateArgs) -> VehicleEntity:
        try:
            vehicle = VehicleEntity(**args.as_dict())
            vehicle = vehicle.compute_derived_attributes()
        except (TypeError, ValueError) as e:
            raise VehicleCreateValidationServiceException(str(e))

        vehicle = self.vehicle_repository.create(vehicle)

        return vehicle
