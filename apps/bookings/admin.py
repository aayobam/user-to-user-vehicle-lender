from decimal import Decimal
from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class AdminBooking(admin.ModelAdmin):
    list_display = ('id', 'renter', 'vehicle', 'start_date',
                    'end_date', 'get_total_price', 'total_hours', 'status')
    search_fields = ('vehicle__type', 'renter__get_full_name')
    readonly_fields = ('id', 'total_price', 'total_hours',
                       'renter_driver_license', 'pickup_location', 'dropoff_location')

    def get_total_price(self, obj):
        duration_hours = obj.get_total_hours()
        total_price = Decimal(duration_hours) * obj.vehicle.price_per_hour
        return f"${total_price}"
    get_total_price.short_description = "total price"
