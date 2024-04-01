from datetime import datetime
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.bookings.models import Booking
from apps.vehicles.models import Vehicle
from apps.common import choices
from django.db import models


class BookVehicleView(LoginRequiredMixin, generic.CreateView):
    model = Booking
    fields = "__all__"
    template_name = 'bookings/book_vehicle.html'
    success_url = reverse_lazy("bookings")

    def post(self, request, *args, **kwargs):

        booking_data = {
            'renter': request.user,
            'vehicle_id': request.POST.get('vehicle_id'),
            'address': request.POST.get('address'),
            'city': request.POST.get('city'),
            'state': request.POST.get('state'),
            'start_date': request.POST.get('pick-up'),
            'end_date': request.POST.get('drop-off'),
            'pickup_location': request.POST.get('pick-up-location'),
            'dropoff_location': request.POST.get('drop-of-location'),
        }

        booking = self.model.objects.create(**booking_data)
        booking.save()
        messages.success(request, "booking successful.")
        return redirect("my_bookings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle_obj = get_object_or_404(Vehicle, id=vehicle_id)
        context['vehicle_id'] = vehicle_id
        context["vehicle"] = vehicle_obj
        return context

        # instance = self.get_object()

        # if not self.is_booking_available(instance.vehicle, instance.start_date, instance.end_date):
        #     messages.info(self.request, "bookings not available, please select a different date or check other vehicles.")
        #     return redirect('available_vehicles')

        # if not self.cannot_book_own_listing(instance):
        #     messages.info(self.request, "you cannot rent your own vehicle listing(s).")
        #     return redirect('available_vehicles')

        # messages.success(self.request, "booking successfull.")

    # def is_booking_available(self, vehicle, start_date, end_date):
    #     bookings = Booking.objects.filter(vehicle=vehicle)
    #     for booking in bookings:
    #         if not (end_date < booking.start_date or start_date > booking.end_date):
    #             return False
    #     return True

    # def cannot_book_own_listing(booking: Booking):
    #     if booking.renter == booking.vehicle.owner:
    #         return False
    #     return True


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
    model = Booking
    fields = "__all__"
    template_name = "bookings/edit_booking.html"
    context_object_name = "booking"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("booking_list")

    def patch_booking(self, instance, booking_data):
        for key, value in booking_data.items():
            setattr(instance, key, value)
        instance.save()

    def post(self, request, *args, **kwargs):
        booking_data = {
            'address': request.POST.get('address'),
            'city': request.POST.get('city'),
            'state': request.POST.get('state'),
        }

        html_start_date = request.POST.get('start-date')
        html_end_date = request.POST.get('end-date')

        start_date = DateTimeFormater.html_to_django(html_start_date)
        end_date = DateTimeFormater.html_to_django(html_end_date)

        print(f"START DATE: {start_date}")
        print(f"END DATE: {end_date}")

        booking_data["start_date"] = start_date
        booking_data["end_date"] = end_date

        instance = self.get_object()
        self.patch_booking(instance, booking_data)
        messages.success(request, "booking updated successfully.")
        return redirect("update_booking", instance.id)


class UpdateOrderView(LoginRequiredMixin, generic.UpdateView):
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
    model = Booking
    context_object_name = "booking"
    pk_url_kwarg = "id"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        messages.success(request, f"booking cancelled successfully")
        return redirect("vehicle_list")


class CancelOrderView(LoginRequiredMixin, generic.DeleteView):
    model = Booking
    context_object_name = "order"
    pk_url_kwarg = "id"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        messages.success(request, f"order canceled successfully.")
        return redirect("order_list")


class DateTimeFormater:

    @staticmethod
    def html_to_django(html_time):
        # Parse HTML time format
        html_format = "%Y-%m-%dT%H:%M:%S"
        html_datetime = datetime.strptime(html_time, html_format)

        # Format to Django DateTime format
        django_format = "%Y-%m-%d %H:%M:%S"
        django_datetime = html_datetime.strftime(django_format)

        return django_datetime

    @staticmethod
    def django_to_html(django_time):
        # Parse Django DateTime format
        django_format = "%Y-%m-%d %H:%M:%S"
        django_datetime = datetime.strptime(django_time, django_format)

        # Format to HTML time format
        html_format = "%Y-%m-%dT%H:%M:%S"
        html_datetime = django_datetime.strftime(html_format)

        return html_datetime

    # # Example usage:
    # html_time = "2024-04-01T08:30:00"
    # django_time = "2024-04-01 08:30:00"
