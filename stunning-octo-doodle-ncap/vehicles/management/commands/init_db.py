import csv

from django.core.management.base import BaseCommand

from vehicles.models import Vehicle


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open("vehicles/management/data/2004_ncap_ssf.csv") as f:
            reader = csv.reader(f)
            next(reader)

            vehicles = [
                Vehicle(
                    ncap_year=row[0],
                    model_year=row[1],
                    make=row[2],
                    model=row[3],
                    drivetrain=row[4],
                    body_style=row[5],
                    engine_type=row[6],
                    transmission_type=row[7],
                    front_track=row[8],
                    rear_track=row[9],
                    average_track=row[10],
                    wheelbase=row[11],
                    test_weight=row[12],
                    cg_long=row[13],
                    cg_lat=row[14],
                    cg_height=row[15],
                    stability_factor=row[16],
                    weight_distribution=row[17],
                )
                for row in reader
            ]
        Vehicle.objects.bulk_create(vehicles)
