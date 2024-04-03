from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.bookings.forms import CreateBookingForm, UpdateBookingForm
from apps.bookings.models import Booking
from apps.vehicles.models import Vehicle
from apps.common import choices


class BookVehicleView(LoginRequiredMixin, generic.CreateView):

    """
    Enables users to book for vehicle available for leasing.
    """
    form_class = CreateBookingForm
    template_name = 'bookings/book_vehicle.html'
    success_url = reverse_lazy("booking_list")

    # This prefills the form with initial data.
    def get_initial(self):
        initial = super().get_initial()
        vehicle = get_object_or_404(Vehicle, id=self.kwargs['vehicle_id'])
        initial['pickup_location'] = vehicle.pickup_location
        initial['dropoff_location'] = vehicle.pickup_location
        return initial

    # gets vehicle data through the vehicle id suppled on the path and returns to the final booking template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle_obj = get_object_or_404(Vehicle, id=vehicle_id)
        context["vehicle"] = vehicle_obj
        return context

    def form_valid(self, form):
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        start_date = form.instance.start_date
        end_date = form.instance.end_date

        if not self.is_booking_available(vehicle, start_date, end_date):
            messages.error(self.request, "bookings not available, please select a different date or check other vehicles.")
            self.form_invalid(form)

        if vehicle.owner == self.request.user:
            messages.error(self.request, "you cannot book your own vehicle listing(s).")
            self.form.invalid(form)

        instance = form.save(commit=False)
        instance.vehicle = vehicle
        instance.renter = self.request.user
        instance.save()
        messages.success(self.request, 'Booking successful.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "could not process booking, please try again")
        return super().form_invalid(form)

    def is_booking_available(self, vehicle, start_date, end_date):
        bookings = Booking.objects.filter(vehicle=vehicle)
        for booking in bookings:
            if not (end_date < booking.start_date or start_date > booking.end_date):
                return False
        return True


class OrdersListView(LoginRequiredMixin, generic.ListView):
    """
    This returns a list of vehicle a user has leased.
    """
    model = Booking
    fields = "__all__"
    template_name = "bookings/orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return super().get_queryset().filter(vehicle__owner=self.request.user)


class BookingListView(LoginRequiredMixin, generic.ListView):
    """
    Returns list of all vehicle a user has rented.
    """
    model = Booking
    fields = "__all__"
    template_name = "bookings/my_bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return super().get_queryset().filter(renter=self.request.user)


class UpdateBookingView(LoginRequiredMixin, generic.UpdateView):
    """
    Enables users who already booked a vehicle to update their bookings.
    """
    queryset = Booking.objects.all()
    form_class = UpdateBookingForm
    template_name = "bookings/edit_booking.html"
    context_object_name = "booking"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("booking_list")

    def form_valid(self, form):
        messages.success(self.request, "booking  updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "update failed, please try again.")
        return super().form_invalid(form)


class UpdateOrderView(LoginRequiredMixin, generic.UpdateView):
    """
    Enables vehicle owners to update their existing orders.
    """
    model = Booking
    fields = "__all__"
    template_name = "bookings/edit_order.html"
    context_object_name = "order"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("order_list")

    def patch_order(self, instance, booking_data):
        for key, value in booking_data.items():
            setattr(instance, key, value)
        instance.save()

    def post(self, request, *args, **kwargs):
        booking_data = {
            "status": request.POST.get("order-status")
        }

        instance = self.get_object()
        self.patch_order(instance, booking_data)
        messages.success(request, "Order updated successfully.")
        return redirect("update_order", instance.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ORDER_STATUS"] = choices.BOOKING_APPROVAL
        return context


class CancelBookingView(LoginRequiredMixin, generic.DeleteView):
    """
    Enables all users be able to cancel their bookings.
    """
    model = Booking
    context_object_name = "booking"
    pk_url_kwarg = "id"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        messages.success(request, f"booking cancelled successfully")
        return redirect("booking_list")


class CancelOrderView(LoginRequiredMixin, generic.DeleteView):
    """
    Enables all users be able to cancel their orders.
    """
    model = Booking
    context_object_name = "order"
    pk_url_kwarg = "id"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        messages.success(request, f"order canceled successfully.")
        return redirect("order_list")
