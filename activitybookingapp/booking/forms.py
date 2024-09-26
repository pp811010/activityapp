from django.forms import ModelForm
from booking.models import *

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = "__all__"