# Generated by Django 4.2.7 on 2024-03-17 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="latitude",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="longitude",
        ),
    ]