from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from authen.forms import *


class LoginView(View):
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('mybooking')

        return render(request,'login.html', {"form":form})


class LogoutView(View):
    
    def get(self, request):
        logout(request)
        return redirect('login')
    
class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save form but don't commit to DB yet
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()

            # Assuming you're saving extra data (like department, phone) from your form
            student = Student.objects.create(
                user = user,
                first_name = user.first_name,
                last_name = user.last_name,
                email = user.email,
                stu_card=form.cleaned_data['student_ID'],
                department=form.cleaned_data['department'],  # Save department
                phone=form.cleaned_data['phone'],  # Save phone number
            )
            student.save()

            # login(request, user)  # Log the user in immediately
            return redirect('login')

        return render(request, 'register.html', {'form': form})
