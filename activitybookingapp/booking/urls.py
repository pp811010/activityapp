from django.urls import path

from booking import views

urlpatterns = [
    path("home/", views.HomeUser.as_view(), name="homeuser"),
    path("mybooking/", views.MyBooking.as_view(), name="mybooking"),
    path("mybooking/<int:booking_id>/", views.MyBooking.as_view(), name="mybooking"),
    path("booking/<int:booking_id>/", views.BookingView.as_view(), name="booking"),
    path("activity/<int:act_id>/", views.ActivityView.as_view(), name="activity"),
    path("place/<int:place_id>/", views.PlaceView.as_view(), name="place"),
    path("placebooking/<int:place_id>/", views.PlaceBooking.as_view(), name="placebooking1"),
    path('placebooking2/<int:place_id>/', views.PlaceBooking2.as_view(), name='placebooking2'),

    # report
    path("place/<int:place_id>/report-list/", views.PlaceReport.as_view(), name="place-report-list"),
    path("place/<int:place_id>/report-list/report-form/<int:user_id>/", views.ReportView.as_view(), name="place-report-form"),
    path("myreport/<int:student_id>/", views.MyReportsView.as_view(), name="my-report-list"),

    # profile
    path("profile/<int:student_id>/", views.ProfileView.as_view(), name="my-profile"),
    path("profile/<int:student_id>/manage/", views.ManageProfileView.as_view(), name="manage-profile"),


    #staff
    path("report-list/", views.ReportList.as_view(), name="report-list"),
    path("report/<int:report_id>/", views.ReportDetail.as_view(), name="report-detail"),
    path('place-list/', views.PlaceList.as_view(), name='place-list'),
    path('booking-list/<int:place_id>/', views.BookingList.as_view(), name='booking-list'),
    path('change-booking-status/<int:booking_id>/', views.ChangeBookingStatus.as_view(), name='change-booking-status'),

    # ผู้จัดการสนาม
    path("homeadmin/", views.HomeAdmin.as_view(), name="homeadmin"),
    path("homeadmin/<int:act_id>/", views.ManageActivity.as_view(), name="deleteactivity"),
    path("addplace/<int:act_id>/", views.Addplace.as_view(), name = 'addplace'),
    path("editplace/<int:place_id>/", views.EditPlace.as_view(), name='editplace'),
    path("staff-list/", views.StaffView.as_view(), name = 'staff-list'),
    path("staff-list/add/", views.AddStaffView.as_view(), name = 'add-staff'),
    path("staff-list/delete/<int:staff_id>", views.DeleteStaffView.as_view(), name = 'delete-staff'),
]
