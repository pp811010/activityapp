from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150) 
    phone = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Student(models.Model):
    FACULTIES = [
        ('It', 'Information Technology'),
        ('ENG', 'Engineering'),
        ('BUS', 'Business'),
        ('MED', 'Medicine'),
        ('LAW', 'Law'),
        ('ART', 'Arts'),
        ('EDU', 'Education'),
        ('SC', 'Sciences')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    faculty = models.CharField(max_length=50, choices=FACULTIES)
    stu_card = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Activity(models.Model):
    name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to = 'activity/')

    def __str__(self):
        return f"{self.name}"

class Place(models.Model):
    staff = models.ManyToManyField(Staff)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.TextField()
    description = models.TextField()
    card = models.IntegerField()
    photo = models.ImageField(upload_to = 'place/')

    def __str__(self):
        return self.name


class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=50,
        choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')]
    )
    def __str__(self):
        return f"Booking by {self.student} for {self.place}"

class Report(models.Model):
    REPORTED = 'REPORTED'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'

    STATUS_CHOICES = [
        (REPORTED, 'Reported'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    details = models.TextField()
    image = models.ImageField(upload_to = 'report/', blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

class BookingFile(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'studentcard/') 

