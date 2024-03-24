from django.db import models


class VehicleManager(models.Manager):

    def total_vehicles_available_for_rent(self):
        return self.get_queryset().filter(availability_status=True).count()

    def total_vehicles_added_by_user(self, user_id):
        return self.get_queryset().filter(owner_id=user_id).count()
