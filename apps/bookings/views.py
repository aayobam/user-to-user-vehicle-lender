from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.bookings.mixins import BookingMixing
from apps.bookings.models import Booking


class BookVehicleView(LoginRequiredMixin, generic.CreateView):
    model = Booking
    fields = "__all__"
    template_name = 'bookings/book_vehicle.html'
    success_url = reverse_lazy("bookings")

    def post(self, request, *args, **kwargs):
        instance = self.get_object()

        if not self.is_booking_available(instance.vehicle, instance.start_date, instance.end_date):
            messages.info(
                self.request, "bookings not available, please select a different date or check other vehicles.")
            return redirect('available_vehicles')

        if not self.cannot_book_own_listing(instance):
            messages.info(
                self.request, "you cannot rent your own vehicle listing(s).")
            return redirect('available_vehicles')

        messages.success(self.request, "booking successfull.")

    def is_booking_available(self, vehicle, start_date, end_date):
        bookings = Booking.objects.filter(vehicle=vehicle)
        for booking in bookings:
            if not (end_date < booking.start_date or start_date > booking.end_date):
                return False
        return True

    def cannot_book_own_listing(booking: Booking):
        if booking.renter == booking.vehicle.owner:
            return False
        return True


class CustomerBookingListView(LoginRequiredMixin, generic.ListView):
    model = Booking
    fields = "__all__"
    template_name = "bookings/orders.html"
    context_object_name = "bookings"


class OwnerBookingListView(LoginRequiredMixin, generic.ListView):
    model = Booking
    fields = "__all__"
    template_name = "bookings/my-bookings.html"
    context_object_name = "bookings"
