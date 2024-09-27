from django.urls import path

from booking import views

urlpatterns = [
    path("mybooking/", views.MyBooking.as_view(), name="mybooking"),
    path("activity/", views.Activity.as_view(), name="activity"),
    path("placebooking/<int:place_id> ", views.ActivityBooking.as_view(), name="placebooking"),
    path("calender/", views.CalenderView.as_view(), name="calender"),
    path("report-form/", views.ReportView.as_view(), name="report_form")
]