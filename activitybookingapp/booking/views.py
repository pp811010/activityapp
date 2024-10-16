import re
import json
from datetime import datetime, time
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views import View
from django.db.models import Case, When
from booking.forms import *
from booking.models import *
from authen.forms import RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.core.validators import validate_email
from django.core.exceptions import PermissionDenied 

# user
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
    permission_required = "booking.view_booking"
    def get(self, request):
        user = request.user
        status_order = Case(
            When(status='PENDING', then=1),
            When(status='APPROVED', then=2),
            When(status='REJECTED', then=3),
            When(status='CANCELED', then=4),
        )
        student = Student.objects.get(user = user)
        booking = Booking.objects.filter(student = student).order_by(status_order,'-created_at')
        return render(request, 'mybooking.html', {"booking": booking, 'student': student})
    
    def delete(self, request, booking_id):
        print(booking_id)
        booking = Booking.objects.get(id=booking_id)
        booking.status = "CANCELED"
        booking.save()
        return HttpResponse(booking_id)

class BookingView(LoginRequiredMixin, PermissionRequiredMixin,  View):
    login_url = '/authen/'
    permission_required = "booking.view_booking"
    def get(self, request, booking_id):
        booking = Booking.objects.get(id = booking_id)
        bookingfile = BookingFile.objects.filter(booking = booking)
        print(bookingfile)
        return render(request, 'booking.html', {'booking': booking, 'bookingfile': bookingfile})

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

        #ิbooking pending status
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

        for file in image_files:
            BookingFile.objects.create(booking=booking, image=file)

        return JsonResponse({"status": "success"})


class ReportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = "booking.view_report"
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

class MyReportsView(View):
    permission_required = "booking.view_report"
    def get(self, request, student_id):
        reports = Report.objects.filter(student__id=student_id).order_by('-id')
        return render(request, 'myreport.html',{"reports":reports})


# get list of report in this place and save form
class PlaceReport(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = 'booking.add_report'
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



# profile
class ProfileView(LoginRequiredMixin, View):
    login_url = '/authen/'
    def get(self, request):
        user = request.user
        student = Student.objects.get(user = user)
        return render(request, 'profile.html',{
            "student":student,
        })
    

class ManageProfileView(LoginRequiredMixin, View):
    login_url = '/authen/'
    def get(self, request):
        user = request.user
       
        student = Student.objects.get(user=user)
        form = StudentForm(instance=student)
        return render(request, 'manage-profile.html', {
            "user": user,
            "form": form,
            "student": student
        })
    
    def post(self, request):
        user = request.user
        student = Student.objects.get(user=user)
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            stu = form.save()
            user.first_name = stu.first_name
            user.last_name = stu.last_name
            user.email  = stu.email
            user.save()
            return redirect('my-profile')
        return render(request, 'manage-profile.html', {
            "user": user,
            "form": form,
            "student": student
        })
            

class ReportList(LoginRequiredMixin, PermissionRequiredMixin,View):
    login_url = '/authen/'
    def post(self, request):
        user = User.objects.get(pk=request.user.id)  # Retrieve the user instance
        form = RegisterForm(request.POST, instance=user)  # Use request.POST and pass the instance

        if form.is_valid():
            user = form.save()  # Save user instance

            # Get the associated student instance
            student = Student.objects.get(user=user)
            student.first_name = form.cleaned_data['first_name']  # Update fields
            student.last_name = form.cleaned_data['last_name']
            student.email = user.email  # Update the email
            student.stu_card = form.cleaned_data['student_ID']
            student.faculty = form.cleaned_data['faculty']
            student.phone = form.cleaned_data['phone']
            print(student)
            student.save()  # Save the student instance

            return redirect('my-profile')
        
        print(form.errors)
        student = Student.objects.get(user=user)  # Retrieve the student again
        return render(request, 'manage-profile.html', {
            "user": user,
            "form": form,
            "student": student
        })


class ChangePasswordView(View):
    def get(self, request ):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'change-password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('my-profile')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'change-password.html', {'form': form})


# for staff
class ReportList(View):
    def get(self, request):
        reports = Report.objects.all().order_by("-id")
        return render(request, 'report-list-staff.html', {
            "reports":reports
        })

  
class ReportDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = 'booking.change_report'
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

# menu Activity
# เเสดง Activity เเละ เพิ่ม activity
class HomeAdmin(LoginRequiredMixin,  View):
    login_url = '/authen/'

    def get(self, request):
        user = request.user
        activity = Activity.objects.all()
        if user.has_perm('booking.view_booking'):
            if user.is_staff:
                return render(request, 'homeadmin.html', {'activity': activity})
            else:
                raise PermissionDenied 
        else:
            raise PermissionDenied


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

# ลบ เเละ edit activity
class ManageActivity(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ['booking.delete_activity', 'booking.change_activity']
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
    
# เพิ่ม place
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
            return render(request, 'addplace.html', {'form': form, 'act': act})

# เเก้ไข place
class EditPlace(LoginRequiredMixin, PermissionRequiredMixin,View):
    login_url = '/authen/'
    permission_required = "booking.change_place"
    def get(self, request, place_id):
        place = Place.objects.get(pk = place_id)
        
        form = PlaceForm(instance=place)
        return render(request, 'editplace.html', {'form': form, 'place': place})
    
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
    

# menu confirm
# เเสดงสนามทั้งหมด
# เเก้ให้เป็น conformView
class PlaceList(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = "booking.change_booking"
    def get(self, request):
        user = request.user
        activities = Activity.objects.all()
        return render(request, 'activity-place.html', {
            'activities':activities
        })

# เเสดงรายละเอียดที่ booking
class BookingList(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = "booking.change_booking"
    def get(self, request, place_id):
        place=Place.objects.get(pk=place_id)
        bookings = Booking.objects.filter(place__id=place_id).order_by('-id')
        return render(request, 'approve-booking.html',{
            'bookings':bookings,
            "place":place,
        })
    
class ChangeBookingStatus(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = "booking.change_booking"
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        action = request.POST.get('action')

        if action == 'approve':
            booking.status = 'APPROVED'           
            send_mail(
                'การจองสนามสำเร็จ',
                f'คุณ {booking.student} ทำการจองสนาม {booking.place} วันที่ {booking.date} เวลา {booking.start_time} - {booking.end_time} สำเร็จ โปรดมาก่อนเวลา 15 นาที และแสดงใบการจองกับเจ้าหน้าที่',
                settings.EMAIL_HOST_USER, 
                [booking.student.email],  
                fail_silently=False  
            )
        elif action == 'reject':
            booking.status = 'REJECTED'  
            send_mail(
                'การจองสนามสำเร็จ',
                f'คุณ {booking.student} ทำการจองสนาม {booking.place} วันที่ {booking.date} เวลา {booking.start_time} - {booking.end_time} ไม่สำเร็จ โปรดจองใหม่อีกครั้ง',
                settings.EMAIL_HOST_USER, 
                [booking.student.email],  
                fail_silently=False  
            )
        
        booking.save()
        return redirect('booking-list', place_id=booking.place.pk)

class StaffView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = "booking.view_staff"
    def get(self, request):
        user = request.user
        staffs = Staff.objects.all()
        num_staff = staffs.count()
        if user.has_perm('booking.view_staff'):
            if user.is_staff:
                return render(request, 'staff-list.html', {
                    "staffs":staffs
                    ,'num_staff':num_staff
                })
            else:
                raise PermissionDenied 
        else:
            raise PermissionDenied
    
class StaffProfile(View, PermissionRequiredMixin):
    def get(self, request, staff_id):
        staff = Staff.objects.get(pk = staff_id)
        return render(request, 'staff-profile.html', {'staff': staff})

class StaffEdit(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = "booking.change_staff"
    def get(self, request, staff_id):
        staff = Staff.objects.get(pk = staff_id)
        form = StaffForm(instance=staff)
        return render(request, 'edit-staff.html', {'form': form, 'staff' : staff})
    
    def post(self, request, staff_id):
        staff = Staff.objects.get(pk = staff_id)
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff-list')
        return render(request, 'edit-staff.html', {'form': form, 'staff' : staff})

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