class VehicleOwnerMixing:
    def get_queryset(self, *args, **kwargs):
        return self.get_queryset().filter(owner=self.request.user)
