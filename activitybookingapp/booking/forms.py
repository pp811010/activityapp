
from django import forms
from django.forms import ModelForm, ValidationError
from booking.models import *
from django.utils import timezone

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal'
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_booking', 'end_booking']
        widgets = {
            "start_booking": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_booking": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_booking = cleaned_data.get("start_booking")
        end_booking = cleaned_data.get("end_booking")

        if start_booking and end_booking:
            if start_booking.date() != end_booking.date():
                raise forms.ValidationError("Start and End bookings must be on the same day.")
            if end_booking <= start_booking:
                raise forms.ValidationError("End booking time must be after Start booking time.")

        return cleaned_data
