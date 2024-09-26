from django.shortcuts import render
from django.views import View
from booking.models import *

# Create your views here.
class MyBooking(View):
    def get(self, request):
        return render(request, 'mybooking.html')
    
class Activity(View):
    def get(self, request):
        return render(request, 'activity.html')
