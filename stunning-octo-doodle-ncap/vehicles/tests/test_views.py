import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from vehicles.entities import VehicleEntity
from vehicles.models import Vehicle
from vehicles.tests.factories import VehicleFactory


class VehicleListViewGetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("vehicle-list")
        self.test_vehicles = [VehicleFactory(id=i) for i in range(1, 126)]

    def test_success(self):
        response = self.client.get(self.url)
        content = json.loads(response.content)

        expected_result_for_first_page = [
            entity.as_entity().as_dict() for entity in self.test_vehicles[:100]
        ]
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(content), 100)
        self.assertEquals(content, expected_result_for_first_page)

        response = self.client.get(self.url, {"page": "2"})
        content = json.loads(response.content)
        expected_result_for_second_page = [
            entity.as_entity().as_dict() for entity in self.test_vehicles[100:]
        ]
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(content), 25)
        self.assertEquals(content, expected_result_for_second_page)

    def test_descending_success(self):
        response = self.client.get(self.url, {"descending": "true"})
        content = json.loads(response.content)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(content), 100)
        self.assertEquals(content[0]["id"], 125)
        self.assertEquals(content[-1]["id"], 26)


class VehicleListViewPostTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("vehicle-list")
        self.test_vehicle = VehicleFactory.build(id=1)
        self.test_vehicle_entity = self.test_vehicle.as_entity()

    def test_success(self):
        payload = self.test_vehicle_entity.as_dict()
        del payload["id"]
        del payload["stability_factor"]
        del payload["weight_distribution"]

        response = self.client.post(self.url, payload, format="json")

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            VehicleEntity(**json.loads(response.content)), self.test_vehicle_entity
        )

        persisted_vehicle = Vehicle.objects.get(id=self.test_vehicle.id)
        self.assertEquals(self.test_vehicle_entity, persisted_vehicle.as_entity())

    def test_missing_argument(self):
        payload = self.test_vehicle_entity.as_dict()
        del payload["id"]
        del payload["stability_factor"]
        del payload["weight_distribution"]
        del payload["make"]

        response = self.client.post(self.url, payload, format="json")

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class VehicleDetailViewGetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("vehicle-detail", kwargs={"id": "1"})
        self.test_vehicle = VehicleFactory(id=1)
        self.test_vehicle_entity = self.test_vehicle.as_entity()

    def test_success(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            json.loads(response.content), self.test_vehicle_entity.as_dict()
        )

    def test_vehicle_does_not_exist(self):
        url = reverse("vehicle-detail", kwargs={"id": "9999"})
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
