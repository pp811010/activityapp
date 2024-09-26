from django.shortcuts import redirect, render
from django.views import View
from booking.forms import ReportForm
from booking.models import *

# Create your views here.
class MyBooking(View):
    def get(self, request):
        return render(request, 'mybooking.html')
    
class Activity(View):
    def get(self, request):
        return render(request, 'activity.html')
    
class ActivityBooking(View):
    def get(self, request):
        return render(request, 'calender.html')

class ReportView(View):
    def get(self, request):
        form = ReportForm()
        return render(request, 'report-form.html',{
            "form": form
        })
    def post(self, request):
        form = ReportForm(request.POST)

        if form.is_valid():
            student = form.cleaned_data.get('student')
            print(f"Student: {student}")
            form.save()
            return redirect('report-form')
        
        return render(request, 'report-form.html', {
            "form":form
        })