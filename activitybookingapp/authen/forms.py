from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from booking.models import Student

class RegisterForm(forms.ModelForm):
    faculty = forms.CharField(widget=forms.Select(
        attrs={'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64"},
        choices=Student.FACULTIES
    ))
    
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
               'placeholder': 'Phone'}))
    
    student_ID = forms.CharField(widget=forms.TextInput(
        attrs={'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
               'placeholder': 'Student ID'}))


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64", 
                'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={
                'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64", 
                'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={
                'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64", 
                'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={
                'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
                'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={
                'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
                'placeholder': 'Password'}),

        }

    def save(self):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        user.save()
        return user
