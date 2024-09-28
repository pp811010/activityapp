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
        booking = Booking.objects.all()
        return render(request, 'mybooking.html', {"booking": booking})
    
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
        place = Place.objects.get(pk=place_id)
        form = BookingForm()
        return render(request, 'placebooking.html', {
            "form": form,
            'place': place
        })

    def post(self, request, place_id):
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mybooking')
        else:
            print(form.errors)  # แสดงผลข้อผิดพลาดที่เกิดขึ้นกับฟอร์ม

        return render(request, "placebooking.html", {
            "form": form,
            'place': Place.objects.get(pk=place_id)  # คืนค่า place เพื่อแสดงในฟอร์ม
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