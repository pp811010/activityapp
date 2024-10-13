
import json
from datetime import datetime, time

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views import View
from booking.forms import *
from booking.models import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.

class HomeUser(LoginRequiredMixin, View):
    login_url = '/authen/'
    def get(self, request):
        user = request.user
        student = Student.objects.get(user = user)
        activity = Activity.objects.all()
        return render(request, 'home.html', {"student": student, 'activity' : activity})
        
        
class MyBooking(LoginRequiredMixin, View):
    login_url = '/authen/'
    def get(self, request):
        user = request.user
        student = Student.objects.get(user = user)
        booking = Booking.objects.filter(student = student).order_by('-date')
        return render(request, 'mybooking.html', {"booking": booking, 'student': student})
    
    def delete(self, request, booking_id):
        print(booking_id)
        booking = Booking.objects.get(id=booking_id)
        booking.delete()
        return HttpResponse(booking_id)

class ActivityView(LoginRequiredMixin,  View):
    login_url = '/authen/'
    def get(self, request, act_id):
        act = Activity.objects.get(pk = act_id)
        place = Place.objects.filter(activity_id = act_id)
        return render(request, 'activity.html', {'act': act ,'place': place})
    
class PlaceBooking(LoginRequiredMixin,  View):
    login_url = '/authen/'
    def get(self, request, place_id):
        user = request.user
        place = Place.objects.get(pk=place_id)
        return render(request, 'placebooking.html', {
            'place': place
        })
     
class PlaceBooking2(LoginRequiredMixin, View):
    def get(self, request, place_id):
        date = request.GET.get('selected_date')
        place = Place.objects.get(pk=place_id)

        bookingpending = Booking.objects.filter(place = place,date = date, status = 'PENDING').values() # ทำเป็น dictionary
        for b in bookingpending:
            b['date'] = str(b['date'])
            b['start_time'] = str(b['start_time'])
            b['end_time'] = str(b['end_time'])
            b['created_at'] = str(b['created_at'])
        print(list(bookingpending))
        bookingpending_json = json.dumps(list(bookingpending))

        #ิbooking confirm status booked
        bookingconfirm = Booking.objects.filter(place = place,date = date, status = 'APPROVED').values() 
        for b in bookingconfirm:
            b['date'] = str(b['date'])
            b['start_time'] = str(b['start_time'])
            b['end_time'] = str(b['end_time'])
            b['created_at'] = str(b['created_at'])
        bookingconfirm_json = json.dumps(list(bookingconfirm))


        return render(request, 'placebooking2.html', {
            'date': date,
            'place': place,
            'booking': bookingconfirm_json,
            'pending' : bookingpending_json,
        })
    
    def post(self, request, place_id):
        user = request.user
        stu = Student.objects.get(user=user)

        # เข้าถึงข้อมูล POST
        selected_time = json.loads(request.POST.get('select_time', '[]'))  # ตั้งค่าเริ่มต้นเป็น list ว่าง
        date_booking = request.POST.get('date')
        date_booking = datetime.strptime(date_booking, "%Y-%m-%d").date()

        # ตรวจสอบว่า selected_time ว่างไหม
        if not selected_time:
            return JsonResponse({"status": "error", "message": "โปรดเลือกเวลา"}, status=400)


        selected_time.sort()
        start_time = time(selected_time[0], 0, 0)
        end_time = time(selected_time[-1] + 1, 0, 0)

        place = Place.objects.get(id=place_id)

        # ตรวจสอบ
        image_files = request.FILES.getlist('image')
        if (len(image_files) != place.card):
            return JsonResponse({"status": "error", "message": f"กรุณาอัปโหลดไฟล์ให้ตรงกับจำนวนที่กำหนด (จำนวนบัตรนักเรียนต้องเป็น {place.card} ไฟล์)"}, status=400)

        booking = Booking.objects.create(
            student=stu,
            place=place,
            date=date_booking,
            start_time=start_time,
            end_time=end_time,
            status='PENDING'
        )

        send_mail(
            'การจองสนามสำเร็จ',
            f'คุณ {stu} ได้ทำการจองสนาม {place.name} วันที่ {date_booking} เวลา {start_time} - {end_time} สำเร็จเรียบร้อยแล้ว โปรดมาก่อนเวลา 15 นาที และแสดงใบการจองกับเจ้าหน้าที่',
            settings.EMAIL_HOST_USER, 
            [stu.email],  
            fail_silently=False  
        )

        for file in image_files:
            BookingFile.objects.create(booking=booking, image=file)

        return JsonResponse({"status": "success"})

class BookingView(LoginRequiredMixin,  View):
    login_url = '/authen/'
    def get(self, request, booking_id):
        booking = Booking.objects.get(id = booking_id)
        bookingfile = BookingFile.objects.filter(booking = booking)
        print(bookingfile)
        return render(request, 'booking.html', {'booking': booking, 'bookingfile': bookingfile})

class PlaceView(LoginRequiredMixin,  View):
    login_url = '/authen/'
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
        reports = Report.objects.all().order_by("id")
        return render(request, 'report-list.html', {
            "reports":reports
        })
    
class ReportDetail(View):
    def get(self, request, report_id):
        report = Report.objects.get(pk=report_id)
        form = ReportForm(instance=report)
        return render(request, 'report-detail.html', {
            "form":form,
            # "report":report
        })
    
    def post(self, request, report_id):
        report = Report.objects.get(pk=report_id)
        form = ReportForm(request.POST, instance=report)

        if form.is_valid():
            form.save()
            return redirect('report-list')
        
        return render(request, 'report-form.html', {
            "form":form
        })

# ผู้จัดการสนาม
class HomeAdmin(LoginRequiredMixin,  View):
    login_url = '/authen/'
    def get(self, request):
        user = request.user
        activity = Activity.objects.all()
        return render(request, 'homeadmin.html', {'activity' : activity})

class Addplace(LoginRequiredMixin, View):
    login_url = '/authen/'

    def get(self, request, act_id):
        act = get_object_or_404(Activity, pk=act_id)
        form = PlaceForm(initial={'activity': act})
        return render(request, 'addplace.html', {'form': form, 'act': act})
    
    def post(self, request, act_id):
        act = get_object_or_404(Activity, pk=act_id)
        form = PlaceForm(request.POST, request.FILES)

        if form.is_valid():
            place = form.save(commit=False)
            place.activity = act
            place.save()
            return redirect('activity', act_id)
        else:
            messages.error(request, 'เกิดข้อผิดพลาดในการเพิ่มสถานที่ กรุณาตรวจสอบข้อมูลของคุณ.')
            return render(request, 'addplace.html', {'form': form, 'act': act})



class EditPlace(View):
    login_url = '/authen/'
    def get(self, request, place_id):
        place = Place.objects.get(pk = place_id)
        
        form = PlaceForm(instance=place)
        return render(request, 'editplace.html', {'form': form, 'place': place})
    
    def post(self, request, place_id):
        place = Place.objects.get(pk= place_id)
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('activity', place.activity.id)
        return render(request, 'editplace.html', {'form': form, 'place': place})
    
    def delete(self, request, place_id):
        place = Place.objects.get(pk = place_id)
        place.delete()
        print('sasasa')
        return HttpResponse(status=200)
