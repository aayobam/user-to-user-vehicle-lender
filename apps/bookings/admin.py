from django.contrib import admin
from .models import Booking



@admin.register(Booking)
class AdminBooking(admin.ModelAdmin):
    list_display = ('id', 'renter', 'vehicle', 'start_date', 'end_date', 'total_price')
    search_fields = ('vehicle__type', 'renter__get_full_name')