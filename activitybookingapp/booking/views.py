import re
import json
from datetime import datetime, time

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views import View
from booking.forms import *
from booking.models import *
from authen.forms import RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.core.validators import validate_email


# Create your views here.
# LoginRequiredMixin, PermissionRequiredMixin,
class HomeUser(View):

    def get(self, request):
        user = request.user
        activity = Activity.objects.annotate(place_count=Count('place')).order_by('-place_count')
        if not user.is_anonymous:
            student = Student.objects.get(user=user)
            return render(request, 'home.html', {"student": student, 'activity': activity})
        
        return render(request, 'home.html', {'activity': activity})
        
        
class MyBooking(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = "booking.add_booking"
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

class ActivityView(View):
    def get(self, request, act_id):
        act = Activity.objects.get(pk = act_id)
        place = Place.objects.filter(activity_id = act_id)
        return render(request, 'activity.html', {'act': act ,'place': place})
    

class PlaceView(View):
    def get(self, request, place_id) :
        place = Place.objects.get(pk=place_id)
        report = Report.objects.filter(place = place)
        return render(request, 'placedetail.html', {
            'place': place,
            'report' : report
        }) 

    
class PlaceBooking(LoginRequiredMixin, PermissionRequiredMixin,  View):
    login_url = '/authen/'
    permission_required = "booking.add_booking"
    def get(self, request, place_id):
        user = request.user
        place = Place.objects.get(pk=place_id)
        return render(request, 'placebooking.html', {
            'place': place
        })
     
class PlaceBooking2(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = "booking.add_booking"
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

        selected_time = json.loads(request.POST.get('select_time', '[]'))  # ตั้งค่าเริ่มต้นเป็น list ว่าง
        date_booking = request.POST.get('date')
        date_booking = datetime.strptime(date_booking, "%Y-%m-%d").date()

 
        if not selected_time:
            return JsonResponse({"status": 'error',"message": "โปรดเลือกเวลา"}, status=400)


        selected_time.sort()
        start_time = time(selected_time[0], 0, 0)
        end_time = time(selected_time[-1] + 1, 0, 0)

        place = Place.objects.get(id=place_id)

        # ตรวจสอบ
        image_files = request.FILES.getlist('image')
        if (len(image_files) != place.card):
            return JsonResponse({"status": 'error', "message": f"กรุณาอัปโหลดไฟล์ให้ตรงกับจำนวนที่กำหนด (จำนวนบัตรนักเรียนต้องเป็น {place.card} ไฟล์)"}, status=400)

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

class BookingView(LoginRequiredMixin, PermissionRequiredMixin,  View):
    login_url = '/authen/'
    permission_required = "booking.add_booking"
    def get(self, request, booking_id):
        booking = Booking.objects.get(id = booking_id)
        bookingfile = BookingFile.objects.filter(booking = booking)
        print(bookingfile)
        return render(request, 'booking.html', {'booking': booking, 'bookingfile': bookingfile})


# get form
class ReportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    def get(self, request, place_id, user_id):
        form = ReportForm()
        student = Student.objects.get(pk=user_id )
        form.fields['student'].initial = student
        place = Place.objects.get(pk=place_id)
        form.fields['place'].initial = place
        return render(request, 'report-form.html',{
            "form": form,
            "place":place,
            "user_id":user_id,
        })


# get list of report in this place and save form
class PlaceReport(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    def get(self, request, place_id):
        place = Place.objects.get(pk=place_id)
        reports = Report.objects.filter(place=place).order_by('-created_at')
        return render(request, 'report-list.html', {
            "reports":reports,
            "place":place
        })
    
    def post(self, request, place_id):
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('place-report-list' , place_id=place_id)
        place = Place.objects.get(pk=place_id)
        reports = Report.objects.filter(place=place)
        return render(request, 'report-list.html', {
            "reports":reports,
            "place":place,
        })


class MyReportsView(View):
    def get(self, request, student_id):
        reports = Report.objects.filter(student__id=student_id)
        return render(request, 'myreport.html',{"reports":reports})


class ProfileView(View):
    def get(self, request, student_id):
        user = User.objects.get(pk=student_id)
        student = Student.objects.get(pk=student_id)
        
        return render(request, 'profile.html',{
            "student":student,
        })
    
class ManageProfileView(View):
    def get(self, request, student_id):
        user = User.objects.get(pk=student_id)
        form = RegisterForm(instance=user)
        return render(request, 'manage-profile.html',{
            "user":user,
            "form":form,
        })

class ReportList(LoginRequiredMixin, PermissionRequiredMixin,View):
    login_url = '/authen/'
    def get(self, request):
        reports = Report.objects.all().order_by("id")
        return render(request, 'report-list-staff.html', {
            "reports":reports
        })

  
class ReportDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    def get(self, request, report_id):
        report = Report.objects.get(pk=report_id)
        form = ReportForm(instance=report)
        return render(request, 'report-detail.html', {
            "form":form,
            "report":report
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


class PlaceList(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    def get(self, request):
        activities = Activity.objects.all()
        return render(request, 'activity-place.html', {
            'activities':activities
        })


class BookingList(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    def get(self, request, place_id):
        place=Place.objects.get(pk=place_id)
        bookings = Booking.objects.filter(place__id=place_id)
        return render(request, 'approve-booking.html',{
            'bookings':bookings,
            "place":place,
        })

class ChangeBookingStatus(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        action = request.POST.get('action')

        if action == 'approve':
            booking.status = 'APPROVED'
        elif action == 'reject':
            booking.status = 'REJECTED'
        
        booking.save()
        return redirect('booking-list', place_id=booking.place.pk)




# ผู้จัดการสนาม
class HomeAdmin(LoginRequiredMixin,  View):
    login_url = '/authen/'
    
    def get(self, request):
        user = request.user
        print(user.get_all_permissions())
        activity = Activity.objects.all()
        return render(request, 'homeadmin.html', {'activity' : activity})

    def post(self, request):
        name = request.POST.get('activity-name')
        name = name.capitalize()
        print(name)
        photo  = request.FILES.get('photo')
        act = Activity.objects.create(name=name,  photo = photo )        
        if act:  
            return redirect('homeadmin') 
        else:
            return HttpResponse({'error': 'Failed create activity'})
            
class ManageActivity(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ["booking.delete_activity", "booking.edit.activity"]
    def  delete(self, request, act_id):
        act = Activity.objects.get(pk= act_id)
        act.delete()
        return HttpResponse(act_id)
    
    def post(self, request, act_id):
        name = request.POST.get('activity-name')
        name = name.capitalize()
        photo  = request.FILES.get('photo')
        act = Activity.objects.get(pk = act_id)
         
        if act: 
            act.name= name
            act.photo = photo
            act.save()
            return redirect('homeadmin') 
        else:
            return HttpResponse({'error': 'Failed edit activity'})
    
class Addplace(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = "booking.add_place"
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
            messages.error(request, 'เกิดข้อผิดพลาดในการเพิ่มสถานที่ กรุณาตรวจสอบข้อมูลของคุณ')
            return render(request, 'addplace.html', {'form': form, 'act': act})



class EditPlace(LoginRequiredMixin, PermissionRequiredMixin,View):
    login_url = '/authen/'
    permission_required = "booking.change_place"
    def get(self, request, place_id):
        place = Place.objects.get(pk = place_id)
        
        form = PlaceForm(instance=place)
        return render(request, 'editplace.html', {'form': form, 'place': place})
    
    #save edit
    def post(self, request, place_id):
        place = Place.objects.get(pk= place_id)
        form = PlaceForm(request.POST, request.FILES, instance=place )
        if form.is_valid():
            form.save()
            return redirect('activity', place.activity.id)
        return render(request, 'editplace.html', {'form': form, 'place': place})
    
    def delete(self, request, place_id):
    
        place = Place.objects.get(pk = place_id)
        act = place.activity.id
        if place:
            place.delete()
            return JsonResponse({'act': act}, status=200)
    

class StaffView(LoginRequiredMixin, View):
    login_url = '/authen/'
    permission_required = "booking.views_staff"
    def get(self, request):
        staffs = Staff.objects.all()
        num_staff = staffs.count()
        return render(request, 'staff-list.html', {
            "staffs":staffs
            ,'num_staff':num_staff
        })
    
class StaffProfile(View):
    def get(self, request, staff_id):
        staff = Staff.objects.get(pk = staff_id)
        return render(request, 'staff-profile.html', {'staff': staff})

class AddStaffView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = "booking.add_staff"
    def get(self, request):
        return render(request, 'add-staff.html')
    
    def post(self, request):
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        errors = {}

        if not fname:
            errors['first_name'] = "First name is required."
        if not lname:
            errors['last_name'] = "Last name is required."

        if not email:
            errors['email'] = "Email is required."
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors['email'] = "Enter a valid email address."

        phone_pattern = r'^\d{3}-\d{3}-\d{4}$'
        if not phone:
            errors['phone'] = "Phone number is required."
        elif not re.match(phone_pattern, phone):
            errors['phone'] = "Phone number must be in the format XXX-XXX-XXXX."

        if errors:
            return render(request, 'add-staff.html', {
                'errors': errors,
                'first_name': fname,
                'last_name': lname,
                'email': email,
                'phone': phone
            })

        Staff.objects.create(
            first_name = fname,
            last_name = lname,
            email = email,
            phone = phone
        )
        return redirect('staff-list')
    
class DeleteStaffView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = "booking.delete_staff"
    def post(self, request, staff_id):
        staff = get_object_or_404(Staff, pk=staff_id)
        staff.delete()
        return redirect('staff-list')