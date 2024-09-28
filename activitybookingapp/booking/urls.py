from django.urls import path

from booking import views

urlpatterns = [
    path("mybooking/", views.MyBooking.as_view(), name="mybooking"),
    path("mybooking/<int:booking_id>/", views.MyBooking.as_view(), name="mybooking"),
    path("activity/", views.Activity.as_view(), name="activity"),
    path("placebooking/<int:place_id>/", views. PlaceBooking.as_view(), name="placebooking"),
    path("calender/", views.CalenderView.as_view(), name="calender"),
    path("report-form/", views.ReportView.as_view(), name="report-form"),
    path('get-available-times/', views.get_available_times, name='get_available_times'),
]