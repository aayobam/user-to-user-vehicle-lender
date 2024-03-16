class BookingMixing:
    def get_queryset(self, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.filter(renter=self.request.user):
            return queryset
        return queryset.filter(vehicle__owner=self.request.user)
