from typing import Any
from .models import Booking
from django import forms


class UpdateBookingForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs=dict(type='datetime-local')))
    end_date = forms.DateField(
        widget=forms.DateInput(attrs=dict(type='datetime-local')))

    class Meta:
        model = Booking
        fields = ['address', 'city', 'state', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super(UpdateBookingForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['city'].widget.attrs.update({"class": "form-control mb-3"})
        self.fields['state'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['start_date'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['end_date'].widget.attrs.update(
            {"class": "form-control mb-3"})


class CreateBookingForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=forms.DateInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(
        widget=forms.DateInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Booking
        fields = ['address', 'city', 'state', 'start_date',
                  'end_date', 'pickup_location', 'dropoff_location']

    def __init__(self, *args, **kwargs):
        super(CreateBookingForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['city'].widget.attrs.update({"class": "form-control mb-3"})
        self.fields['state'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['start_date'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['end_date'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['pickup_location'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['dropoff_location'].widget.attrs.update(
            {"class": "form-control mb-3"})

        self.fields['pickup_location'].disabled = True
        self.fields['dropoff_location'].disabled = True

    # def clean(self) -> dict[str, Any]:
    #     cleaned_data = super().clean()
    #     start_date = cleaned_data.get('start_date')
    #     end_date = cleaned_data.get('end_date')
    #     vehicle = cleaned_data.get("vehicle_id")

    #     if not self.is_booking_available(vehicle, start_date, end_date):
    #         raise forms.ValidationError(
    #             "bookings not available, please select a different date or check other vehicles.")

    #     if not self.cannot_book_own_listing(vehicle):
    #         raise forms.ValidationError("you cannot rent your own vehicle listing(s).")

    #     return super().validate_unique()

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
