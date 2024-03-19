from django.contrib import admin

from .models import Vehicle, VehicleImage


@admin.register(Vehicle)
class AdminVehicle(admin.ModelAdmin):
    list_display = ('id', 'owner', 'type', 'make', 'model', 'year', 'location', 'longitude', 'latitude',
                    'registration_number', 'price_per_hour', 'availability_status')
    readonly_fields = ('id', 'longitude', 'latitude')


@admin.register(VehicleImage)
class AdminVehicleImage(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'image')
    readonly_fields = ('id',)
