from django.urls import path

from booking import views

urlpatterns = [
    path("mybooking/", views.MyBooking.as_view(), name="mybooking"),
    path("mybooking/<int:booking_id>/", views.MyBooking.as_view(), name="mybooking"),
    path("booking/<int:booking_id>/", views.BookingView.as_view(), name="booking"),
    path("activity/", views.Activity.as_view(), name="activity"),
    path("place/<int:place_id>/", views.PlaceView.as_view(), name="place"),
    path("placebooking/<int:place_id>/", views.PlaceBooking.as_view(), name="placebooking1"),
    path('placebooking2/<int:place_id>/', views.PlaceBooking2.as_view(), name='placebooking2'),

    # report
    path("place/<int:place_id>/report-list/", views.PlaceReport.as_view(), name="place-report-list"),
    path("place/<int:place_id>/report-list/report-form/<int:user_id>/", views.ReportView.as_view(), name="place-report-form"),
    #report management
    path("report-list/", views.ReportList.as_view(), name="report-list"),
    path("report/<int:report_id>/", views.ReportDetail.as_view(), name="report-detail"),


    # ผู้จัดการสนาม
    path("addplace/", views.Addplace.as_view(), name = 'addplace'),
]
