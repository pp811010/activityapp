from django.db import models
from django.contrib.auth.models import User

class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)  # Changed to EmailField for better validation
    phone = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Student(models.Model):
    DEPARTMENTS = [
        ('CS', 'Computer Science'),
        ('ENG', 'Engineering'),
        ('BUS', 'Business'),
        ('MED', 'Medicine'),
        ('LAW', 'Law'),
        ('ART', 'Arts'),
        ('EDU', 'Education'),
        ('BIO', 'Biology'),
        ('CHE', 'Chemistry'),
        ('PHY', 'Physics'),
        ('MATH', 'Mathematics'),
        ('SOC', 'Social Sciences'),
        ('HIST', 'History'),
        ('PHIL', 'Philosophy'),
        ('ENV', 'Environmental Science'),
    ]

    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    stu_card = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)  # Changed to EmailField for better validation
    phone = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Activity(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Place(models.Model):
    staff = models.ManyToManyField(Staff)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.TextField()
    description = models.TextField(blank=True, null=True)
    photo = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=50,
        choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')]
    )
    def __str__(self):
        return f"Booking by {self.student} for {self.place}"

class Report(models.Model):
    STATUS_CHOICES = [
        ('REPORTED', 'Reported'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    details = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Report by {self.student} for {self.place}"

class BookingFile(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    card = models.CharField(max_length=256)

    def __str__(self):
        return f"Fine for Booking {self.booking}"
