from decimal import Decimal
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

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"{self.vehicle.type} Bookings"

    def get_absolute_url(self):
        return reverse("booking_detail", kwargs={"id": self.id})

    def get_total_price(self):
        total_price: Decimal = (
            self.start_date - self.end_date) / self.vehicle.price_per_hour
        return total_price

    def save(self, *args, **kwargs):
        self.total_price: Decimal = self.get_total_price()
        return super().save(*args, **kwargs)
