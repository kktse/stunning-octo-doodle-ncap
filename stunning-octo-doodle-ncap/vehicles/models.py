from django.db import models

from vehicles.constants import VehicleDrivetrainTypes, VehicleBodyStyles
from vehicles.entities import VehicleEntity


class VehicleBase(models.Model):
    class Meta:
        abstract = True

    id = models.AutoField(primary_key=True)


class Vehicle(VehicleBase):
    ncap_year = models.IntegerField()
    model_year = models.IntegerField()
    make = models.CharField(max_length=128)
    model = models.CharField(max_length=256)

    drivetrain = models.CharField(
        max_length=32,
        choices=VehicleDrivetrainTypes.CHOICES,
        default=VehicleDrivetrainTypes.UNKNOWN,
    )
    body_style = models.CharField(
        max_length=32,
        choices=VehicleBodyStyles.CHOICES,
        default=VehicleBodyStyles.UNKNOWN,
    )
    engine_type = models.TextField(max_length=128)
    transmission_type = models.TextField(max_length=128)

    front_track = models.FloatField()
    rear_track = models.FloatField()
    average_track = models.FloatField()
    wheelbase = models.FloatField()

    test_weight = models.FloatField()

    cg_long = models.FloatField()
    cg_lat = models.FloatField()
    cg_height = models.FloatField()

    stability_factor = models.FloatField()
    weight_distribution = models.FloatField()

    def as_entity(self) -> VehicleEntity:
        return VehicleEntity(
            id=self.id,
            ncap_year=self.ncap_year,
            model_year=self.model_year,
            make=self.make,
            model=self.model,
            drivetrain=self.drivetrain,
            body_style=self.body_style,
            engine_type=self.engine_type,
            transmission_type=self.transmission_type,
            front_track=self.front_track,
            rear_track=self.rear_track,
            average_track=self.average_track,
            wheelbase=self.wheelbase,
            test_weight=self.test_weight,
            cg_long=self.cg_long,
            cg_lat=self.cg_lat,
            cg_height=self.cg_height,
            stability_factor=self.stability_factor,
            weight_distribution=self.weight_distribution,
        )
