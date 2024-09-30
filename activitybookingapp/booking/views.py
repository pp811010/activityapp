import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from booking.forms import *
from booking.models import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.
class MyBooking(LoginRequiredMixin, View):
    login_url = '/authen/'
    def get(self, request):
        user = request.user
        student = Student.objects.get(user = user)
        booking = Booking.objects.filter(student = student)
        return render(request, 'mybooking.html', {"booking": booking, 'student': student})
    
    def delete(self, request, booking_id):
        booking = Booking.objects.get(pk=booking_id)
        booking.delete()
        return HttpResponse(booking_id)

class Activity(View):
    def get(self, request):
        place = Place.objects.all()
        return render(request, 'activity.html', {'place': place})
    
class PlaceBooking(View):

    def get(self, request, place_id):
        user = request.user
        place = Place.objects.get(pk=place_id)
        form = BookingForm()
        return render(request, 'placebooking.html', {
            "form": form,
            'place': place
        })

    def post(self, request, place_id):
        user = request.user
        place = Place.objects.get(pk=place_id)
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = user.student
            booking.place = place
            booking.status = 'PENDING'
            booking.save()
            return redirect('mybooking')

        return render(request, "placebooking.html", {
            "form": form,
            'place': place
        })

class CalenderView(View):

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