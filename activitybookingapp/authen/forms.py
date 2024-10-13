from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from booking.models import Student
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    faculty = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64"}
        ),
        choices=Student.FACULTIES
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
                   'placeholder': 'Phone'})
    )

    student_ID = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
                   'placeholder': 'Student ID'})
    )
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
        'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
                'placeholder': 'Username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
                'placeholder': 'Email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': "mb-8 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
                'placeholder': 'Password'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        
        email = cleaned_data.get('email')
        if email:
            username_part = email.split('@')[0]
            if not email.endswith('@kmitl.ac.th') | len(username_part) < 8:
                self.add_error('email', 'อีเมลต้องใช้โดเมน @kmitl.ac.th')

        phone = cleaned_data.get('phone')
        if phone and len(phone) != 10:
            self.add_error('phone', 'เบอร์โทรศัพท์ต้องมี 10 หลัก')

        student_ID = cleaned_data.get('student_ID')
        if student_ID and len(student_ID) != 8:
            self.add_error('student_ID', 'หมายเลขนักเรียนต้องมี 8 หลัก')

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            self.add_error('password2', 'รหัสผ่านไม่ตรงกัน')

        return cleaned_data
