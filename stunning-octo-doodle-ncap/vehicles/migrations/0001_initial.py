# Generated by Django 4.0.1 on 2022-01-22 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Vehicle",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("ncap_year", models.IntegerField()),
                ("model_year", models.IntegerField()),
                ("make", models.CharField(max_length=128)),
                ("model", models.CharField(max_length=256)),
                (
                    "drivetrain",
                    models.CharField(
                        choices=[
                            ("UNKNOWN", "UNKNOWN"),
                            ("AWD", "AWD"),
                            ("FWD", "FWD"),
                            ("RWD", "RWD"),
                            ("4WD", "4WD"),
                        ],
                        default="UNKNOWN",
                        max_length=32,
                    ),
                ),
                (
                    "body_style",
                    models.CharField(
                        choices=[
                            ("UNKNOWN", "UNKNOWN"),
                            ("Convertible", "Convertible"),
                            ("Hatchback", "Hatchback"),
                            ("Pickup", "Pickup"),
                            ("Sedan", "Sedan"),
                            ("SUV", "SUV"),
                            ("Van", "Van"),
                            ("Wagon", "Wagon"),
                        ],
                        default="UNKNOWN",
                        max_length=32,
                    ),
                ),
                ("engine_type", models.TextField(max_length=128)),
                ("transmission_type", models.TextField(max_length=128)),
                ("front_track", models.FloatField()),
                ("rear_track", models.FloatField()),
                ("average_track", models.FloatField()),
                ("wheelbase", models.FloatField()),
                ("test_weight", models.FloatField()),
                ("cg_long", models.FloatField()),
                ("cg_lat", models.FloatField()),
                ("cg_height", models.FloatField()),
                ("stability_factor", models.FloatField()),
                ("weight_distribution", models.FloatField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]