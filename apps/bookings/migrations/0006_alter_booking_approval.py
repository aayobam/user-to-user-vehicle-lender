# Generated by Django 4.2.7 on 2024-04-01 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0005_booking_approval"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="approval",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Declined", "Declined"),
                ],
                default="Pending",
                max_length=100,
            ),
        ),
    ]
