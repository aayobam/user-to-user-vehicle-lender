from django.contrib import admin

from .models import Vehicle


@admin.register(Vehicle)
class AdminVehicle(admin.ModelAdmin):
    list_display = ('id', 'owner', 'type', 'make', 'model', 'year', 'location', 'registration_number', 'price_per_hour', 'availability_status')
    readonly_fields = ('id',)
