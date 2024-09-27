from datetime import date
from django import forms
from django.forms import ModelForm, ValidationError
from booking.models import *

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = "__all__"

class BookingForm(ModelForm):
    from django import forms
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
        widgets = {
            "booking_date": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get("booking_date")
        if booking_date and booking_date < timezone.now():
            raise forms.ValidationError("Booking date cannot be in the past.")
        return booking_date

