import attrs

from django.test import TestCase

from vehicles.constants import VehicleListOrderBy
from vehicles.repositories import (
    VehicleRepository,
    VehicleDoesNotExistRepositoryException,
)
from vehicles.tests.factories import VehicleFactory


class VehicleRepositoryGetTestCase(TestCase):
    def setUp(self):
        self.sut = VehicleRepository()
        self.test_vehicle = VehicleFactory(id=1)

    def test_success(self):
        vehicle = self.sut.get(id=self.test_vehicle.id)
        self.assertEquals(vehicle, self.test_vehicle.as_entity())

    def test_raises_does_not_exist_repository_exception(self):
        with self.assertRaises(VehicleDoesNotExistRepositoryException):
            self.sut.get(id=9999)


class VehicleRepositoryListTestCase(TestCase):
    def setUp(self):
        self.sut = VehicleRepository()

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

    def test_default_args_success(self):
        expected_result = [entity.as_entity() for entity in self.test_vehicles]

        actual_result = self.sut.list()
        self.assertEquals(actual_result, expected_result)

    def test_defined_args_success(self):
        expected_result = [
            self.test_vehicle_2.as_entity(),
            self.test_vehicle_1.as_entity(),
        ]

        actual_result = self.sut.list(
            order_by=VehicleListOrderBy.ID,
            descending=True,
            page=2,
            limit=2,
        )
        self.assertEquals(actual_result, expected_result)


class VehicleRepositoryCreateTestCase(TestCase):
    def setUp(self):
        self.sut = VehicleRepository()
        self.reference_vehicle_entity = VehicleFactory(id=1)

    def test_success(self):
        vehicle_payload = self.reference_vehicle_entity.as_entity()
        vehicle_payload.id = None
        expected_result = attrs.evolve(vehicle_payload, id=2)

        result = self.sut.create(vehicle=vehicle_payload)

        self.assertEquals(result, expected_result)
