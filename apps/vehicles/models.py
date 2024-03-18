from django.db import models
from django.urls import reverse
from apps.common.base_model import BaseModel
from apps.common.choices import VEHICLE_MAKES, VEHICLE_TYPES
from apps.users.models import CustomUser


class Vehicle(BaseModel):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(choices=VEHICLE_TYPES, max_length=100)
    make = models.CharField(choices=VEHICLE_MAKES, max_length=100)
    model = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    availability_status = models.BooleanField(default=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['type', 'location']),
            # models.Index(fields=['type']),
            # models.Index(fields=['location']),
            # models.Index(fields=['model']),
        ]
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse("vehicle_detail", kwargs={"id": self.id})


class VehicleImage(BaseModel):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,related_name="vehicle_images", blank=True, null=True)
    image = models.ImageField(upload_to="vehicle images/", blank=True, null=True)

    class Meta:
        verbose_name = "Vehicle Image"
        verbose_name_plural = "Vehicle Images"

    def __str__(self):
        return self.image.url
