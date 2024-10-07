
from django import forms
from django.forms import ModelForm, ValidationError
from booking.models import *
from django.utils import timezone

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        is_edit = kwargs.get('instance') is not None
        super(ReportForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal'
        if is_edit:
            self.fields['student'].disabled = True
            self.fields['place'].disabled = True
            self.fields['details'].disabled = True

        else:
            self.fields['status'].disabled = True
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
