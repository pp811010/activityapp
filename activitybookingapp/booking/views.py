
import json
from datetime import datetime, time

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
        booking = Booking.objects.filter(student = student).order_by('-id')
        return render(request, 'mybooking.html', {"booking": booking, 'student': student})
    
    def delete(self, request, booking_id):
        print(booking_id)
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
        return render(request, 'placebooking.html', {
            'place': place
        })
    
class PlaceBooking2(View):
    def get(self, request, place_id):
        date = request.GET.get('selected_date')
        place = Place.objects.get(pk=place_id)
        booking = Booking.objects.filter(date = date).values()
        for b in booking:
            b['date'] = str(b['date'])
            b['start_time'] = str(b['start_time'])
            b['end_time'] = str(b['end_time'])
        booking_json = json.dumps(list(booking))


        return render(request, 'placebooking2.html', {
            'date': date,
            'place': place,
            'booking': booking_json
        })
    
    def post(self, request, place_id):
        user = request.user
        stu = Student.objects.get(user=user)
        
        # โหลดข้อมูลจาก body ของ request
        data = json.loads(request.body)
        selected_time = data['select_time']  # เช่น [13, 14, 15]
        date_booking = data['date']
        date_booking = datetime.strptime(date_booking, "%Y-%m-%d").date()

        selected_time.sort()
        start_time = time(selected_time[0], 0, 0)
        end_time = time(selected_time[-1]+1, 0, 0)

        place = Place.objects.get(id=place_id)
    
        # สร้างรายการจอง (Booking)
        booking = Booking.objects.create(
            student=stu,
            place=place,
            date=date_booking,  # ต้องตรวจสอบว่า date เป็นรูปแบบวันที่ (เช่น '2024-10-02')
            start_time=start_time,
            end_time=end_time,
            status = 'PENDING'
        )

        if booking:
            print('dsada')
        else:
            print('ควย')
        
        return JsonResponse({"status": "success"})
    

class BookingView(View):
    def get(self, request, booking_id):
        booking = Booking.objects.get(id = booking_id)
        return render(request, 'booking.html', {'booking': booking})

class PlaceView(View):
    def get(self, request, place_id) :
        place = Place.objects.get(pk=place_id)
        report = Report.objects.filter(place = place)
        return render(request, 'placedetail.html', {
            'place': place,
            'report' : report
        }) 
        


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
    
class ReportList(View):
    def get(self, request):
        reports = Report.objects.all()
        return render(request, 'report-list.html', {
            "reports":reports
        })