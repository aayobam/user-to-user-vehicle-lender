from django.contrib import admin

from .models import Vehicle, VehicleImage


@admin.register(Vehicle)
class AdminVehicle(admin.ModelAdmin):
    list_display = ('id', 'owner', 'type', 'make', 'model', 'year', 'location', 'longitude', 'latitude',
                    'registration_number', 'price_per_hour', 'availability_status')


@admin.register(VehicleImage)
class AdminVehicle(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'image')
