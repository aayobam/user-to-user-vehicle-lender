from typing import Any

from django.shortcuts import get_object_or_404

from apps.vehicles.models import Vehicle
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
