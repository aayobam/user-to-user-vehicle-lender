# Generated by Django 4.2.7 on 2024-03-30 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vehicles", "0004_remove_vehicle_registration_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicle",
            name="availability_status",
            field=models.CharField(
                choices=[("Available", "Available"), ("Unavailable", "Unavailable")],
                default="Available",
                max_length=50,
            ),
        ),
    ]