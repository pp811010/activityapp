from django.urls import path

from booking import views

urlpatterns = [
    path("mybooking/", views.MyBooking.as_view(), name="mybooking"),
    path("activity/", views.Activity.as_view(), name="activity"),
    path("activitybooking/", views.ActivityBooking.as_view(), name="activity"),
    path("report-form/", views.ReportView.as_view(), name="report_form")
]