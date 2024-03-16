from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.bookings.mixins import BookingMixing
from apps.bookings.models import Booking


class BookVehicleView(LoginRequiredMixin, generic.CreateView):
    model = Booking
    fields = ['vehicle', 'start_date', 'end_date']
    template_name = 'bookings/book_vehicle.html'
    queryset = Booking.objects.select_related("vehicle", "renter").all()
    success_url = reverse_lazy("bookings")

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.renter = self.reuqest.user
        form.instance.driver_licence = self.request.user.document.url
        if not self.is_booking_available(form.instance.vehicle, form.instance.start_date, form.instance.end_date):
            messages.info(self.request, "bookings not available, please select a different date or check other vehicles.")
            return redirect('available_vehicles')
        messages.success(self.request, "booking successfull.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "booking unsuccessful, please try again or book another vehicle.")
        return super().form_invalid(form)

    def is_booking_available(self, vehicle, start_date, end_date):
        bookings = Booking.objects.filter(vehicle=vehicle)
        for booking in bookings:
            if not (end_date < booking.start_date or start_date > booking.end_date):
                return False
        return True


class UserBookingsListView(LoginRequiredMixin, BookingMixing, generic.ListView):
    queryset = Booking.objects.select_related("vehicle", "renter").all()
    template_name = "bookings/user_bookings.html"
    context_object_name = "bookings"
    permission_denied_message = "you do not have permission to view this page."
