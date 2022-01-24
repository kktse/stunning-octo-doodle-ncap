from typing import Optional

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from vehicles.datatypes import VehicleServiceCreateArgs
from vehicles.constants import VehicleListOrderBy
from vehicles.services import (
    VehicleService,
    VehicleDoesNotExistServiceException,
    VehicleCreateValidationServiceException,
)


class VehicleListView(APIView):
    def __init__(self, vehicle_service: Optional[VehicleService] = None) -> None:
        self.vehicle_service = vehicle_service or VehicleService()

    def get(self, request: Request, format=None) -> Response:

        vehicles = self.vehicle_service.list(
            order_by=request.query_params.get("order_by", VehicleListOrderBy.ID),
            descending=request.query_params.get("descending", False),
            page=request.query_params.get("page", 1),
        )

        return Response([entity.as_dict() for entity in vehicles])

    def post(self, request: Request, format=None) -> Response:
        try:
            args = VehicleServiceCreateArgs(**request.data)
            vehicle = self.vehicle_service.create(args=args)
        except (TypeError, VehicleCreateValidationServiceException) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(vehicle.as_dict())


class VehicleDetailView(APIView):
    def __init__(self, vehicle_service: Optional[VehicleService] = None) -> None:
        self.vehicle_service = vehicle_service or VehicleService()

    def get(self, request: Request, id: int, format=None):
        try:
            vehicle = self.vehicle_service.get(id=id)
        except VehicleDoesNotExistServiceException as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response(vehicle.as_dict())
