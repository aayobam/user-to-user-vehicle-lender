from decimal import Decimal
from math import ceil
from django.db import models
from django.urls import reverse
from apps.common.base_model import BaseModel
from apps.users.models import CustomUser
from apps.vehicles.models import Vehicle


class Booking(BaseModel):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    renter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    renter_driver_license = models.FileField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_hours = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"{self.vehicle.type} Bookings"

    def get_absolute_url(self):
        return reverse("booking_detail", kwargs={"id": self.id})

    def get_total_hours(self):
        duration_hours = (
            self.end_date - self.start_date).total_seconds() / 3600
        return ceil(duration_hours)

    def get_total_price(self):
        duration_hours = self.get_total_hours()
        total_price = Decimal(duration_hours) * self.vehicle.price_per_hour
        return total_price

    def save(self, *args, **kwargs):
        self.total_hours = self.get_total_hours()
        self.total_price: Decimal = self.get_total_price()
        return super().save(*args, **kwargs)
