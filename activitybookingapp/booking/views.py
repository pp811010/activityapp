from django.shortcuts import redirect, render
from django.views import View
from booking.forms import *
from booking.models import *

# Create your views here.
class MyBooking(View):
    def get(self, request):
        booking = Booking.objects.all()
        return render(request, 'mybooking.html', {"booking": booking})
    
class Activity(View):
    def get(self, request):
        place = Place.objects.all()
        return render(request, 'activity.html', {'place': place})
    
class ActivityBooking(View):

    def get(self, request, place_id):
        place = Place.objects.get(pk = place_id)
        form = BookingForm()
        return render(request, 'placebooking.html',{
            "form": form,
            'place': place
        })

    def post(self, request):
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mybooking')
        else:
            print(form.errors)  # แสดงผลข้อผิดพลาดที่เกิดขึ้นกับฟอร์ม

        return render(request, "activitybooking.html", {
            "form": form
        })


class ReportView(View):

    def get(self, request):
        form = ReportForm()
        return render(request, 'report-form.html',{
            "form": form
        })
