import attrs

from unittest import mock
from django.test import TestCase

from vehicles.constants import VehicleListOrderBy
from vehicles.datatypes import VehicleServiceCreateArgs
from vehicles.repositories import (
    VehicleRepository,
    VehicleDoesNotExistRepositoryException,
)
from vehicles.services import (
    VehicleService,
    VehicleDoesNotExistServiceException,
)
from vehicles.tests.factories import VehicleFactory


class VehicleServiceGetTestCase(TestCase):
    def setUp(self):
        self.test_vehicle = VehicleFactory(id=1)
        self.vehicle_repository = mock.create_autospec(VehicleRepository)
        self.vehicle_repository.get.return_value = self.test_vehicle.as_entity()

        self.sut = VehicleService(vehicle_repository=self.vehicle_repository)

    def test_success(self):
        vehicle = self.sut.get(id=self.test_vehicle.id)

        self.assertEquals(vehicle, self.test_vehicle.as_entity())
        self.vehicle_repository.get.assert_called_with(id=self.test_vehicle.id)

    def test_raises_does_not_exist_service_exception(self):
        self.vehicle_repository.get.side_effect = VehicleDoesNotExistRepositoryException

        with self.assertRaises(VehicleDoesNotExistServiceException):
            self.sut.get(id=self.test_vehicle.id)


class VehicleServiceListTestCase(TestCase):
    def setUp(self):
        self.test_vehicle_1 = VehicleFactory(id=1)
        self.test_vehicle_2 = VehicleFactory(id=2)
        self.test_vehicle_3 = VehicleFactory(id=3)
        self.test_vehicle_4 = VehicleFactory(id=4)

        self.test_vehicles = [
            self.test_vehicle_1,
            self.test_vehicle_2,
            self.test_vehicle_3,
            self.test_vehicle_4,
        ]
        self.test_vehicle_entities = [
            entity.as_entity() for entity in self.test_vehicles
        ]

        self.vehicle_repository = mock.create_autospec(VehicleRepository)
        self.vehicle_repository.list.return_value = self.test_vehicle_entities

        self.sut = VehicleService(vehicle_repository=self.vehicle_repository)

    def test_default_args_success(self):
        actual_result = self.sut.list()

        self.assertEquals(actual_result, self.test_vehicle_entities)

    def test_defined_args_success(self):
        expected_result = [
            self.test_vehicle_2.as_entity(),
            self.test_vehicle_1.as_entity(),
        ]
        self.vehicle_repository.list.return_value = expected_result

        actual_result = self.sut.list(
            order_by=VehicleListOrderBy.ID, descending=True, page=2, limit=2
        )

        self.assertEquals(actual_result, expected_result)
        self.vehicle_repository.list.assert_called_with(
            order_by=VehicleListOrderBy.ID, descending=True, page=2, limit=2
        )


class VehicleServiceCreateTestCase(TestCase):
    def setUp(self):
        self.test_vehicle = VehicleFactory(
            id=1, average_track=1, cg_height=1, cg_long=1, wheelbase=2
        )
        self.test_vehicle_entity = self.test_vehicle.as_entity()

        self.test_args_dict = self.test_vehicle_entity.as_dict()
        del self.test_args_dict["id"]
        del self.test_args_dict["stability_factor"]
        del self.test_args_dict["weight_distribution"]

        self.test_args = VehicleServiceCreateArgs(**self.test_args_dict)

        self.vehicle_repository = mock.create_autospec(VehicleRepository)
        self.vehicle_repository.create.return_value = self.test_vehicle_entity

        self.sut = VehicleService(vehicle_repository=self.vehicle_repository)

    def test_success(self):
        expected_vehicle_arg = attrs.evolve(
            self.test_vehicle_entity,
            id=None,
            stability_factor=0.5,
            weight_distribution=0.5,
        )

        result = self.sut.create(self.test_args)

        self.assertEquals(result, self.test_vehicle_entity)
        self.vehicle_repository.create.assert_called_with(vehicle=expected_vehicle_arg)
