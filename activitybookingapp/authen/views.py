from django.contrib.auth.models import Group
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
        if form.is_valid():
            user = form.get_user()
            login(request,user)

            if user.is_staff:
                return redirect('homeadmin')
            else:
                return redirect('homeuser')
    
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
            user = form.save()
            usergroup = Group.objects.get(name='User')
            user.groups.add(usergroup)

            student = Student.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                stu_card=form.cleaned_data['student_ID'],
                faculty=form.cleaned_data['faculty'],
                phone=form.cleaned_data['phone'],
            )
            student.save()

            return redirect('login')

        return render(request, 'register.html', {'form': form})