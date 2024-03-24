# Generated by Django 4.2.7 on 2024-03-23 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Vehicle",
            fields=[
                (
                    "id",
                    models.CharField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        max_length=64,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "vehicle_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", "Select Type"),
                            ("Sedan", "Sedan"),
                            ("Suv", "Suv"),
                            ("Truck", "Truck"),
                            ("Hatchback", "Hatchback"),
                            ("Coupe", "Coupe"),
                            ("Convertible", "Convertible"),
                            ("Mini Van", "Mini Van"),
                            ("Pickup", "Pickup"),
                            ("Van", "Van"),
                            ("Crossover", "Crossover"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "vehicle_make",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", "Select Make"),
                            ("Toyota", "Toyota"),
                            ("Honda", "Honda"),
                            ("Ford", "Ford"),
                            ("Chevrolet", "Chevrolet"),
                            ("Bmw", "Bmw"),
                            ("Mercedes Benz", "Mercedes Benz"),
                            ("Audi", "Audi"),
                            ("Nissan", "Nissan"),
                            ("Volkswagen", "Volkswagen"),
                            ("Tesla", "Tesla"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                ("model", models.CharField(blank=True, max_length=100, null=True)),
                ("year", models.CharField(blank=True, max_length=50, null=True)),
                ("max_speed", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "total_doors",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("1", "1"),
                            ("2", "2"),
                            ("3", "3"),
                            ("4", "4"),
                            ("5", "5"),
                            ("6", "6"),
                            ("7", "7"),
                            ("8", "8"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "transmission_type",
                    models.CharField(
                        blank=True,
                        choices=[("Manual", "Manual"), ("Auto", "Auto")],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "total_passengers",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("2", "2"),
                            ("3", "3"),
                            ("4", "4"),
                            ("5", "5"),
                            ("6", "6"),
                            ("7", "7"),
                            ("8", "8"),
                            ("10", "10"),
                            ("15", "15"),
                            ("24", "24"),
                            ("40", "40"),
                            ("50", "50"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "registration_number",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "fuel_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Gasoline", "Gasoline"),
                            ("Petrol", "Petrol"),
                            ("Diesel", "Diesel"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("aircondition", models.BooleanField(default=True)),
                (
                    "engine_capacity",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("availability_status", models.BooleanField(default=True)),
                (
                    "price_per_hour",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "pickup_location",
                    models.CharField(blank=True, max_length=150, null=True),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="vehicle images/"
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Vehicle",
                "verbose_name_plural": "Vehicles",
                "indexes": [
                    models.Index(
                        fields=["vehicle_type"], name="vehicles_ve_vehicle_76fbe4_idx"
                    ),
                    models.Index(
                        fields=["vehicle_make"], name="vehicles_ve_vehicle_27c4df_idx"
                    ),
                ],
            },
        ),
    ]
