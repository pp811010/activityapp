from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from booking.models import Student
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    faculty = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18"}
        ),
        choices=Student.FACULTIES
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18",
                   'placeholder': 'Phone'})
    )

    student_ID = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18",
                   'placeholder': 'Student ID'})
    )
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18",
        'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18",
                'placeholder': 'Username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18",
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18",
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18",
                'placeholder': 'Email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18",
                'placeholder': 'Password'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            return user

    def clean(self):
        cleaned_data = super().clean()
        
        email = cleaned_data.get('email')
        if email:
            if not email.endswith('@kmitl.ac.th'):
                self.add_error('email', 'อีเมลต้องใช้โดเมน @kmitl.ac.th')

        phone = cleaned_data.get('phone')
        if len(phone) != 10:
            self.add_error('phone', 'เบอร์โทรศัพท์ต้องมี 10 หลัก')

        student_ID = cleaned_data.get('student_ID')
        if len(student_ID) != 8:
            self.add_error('student_ID', 'หมายเลขนักเรียนต้องมี 8 หลัก')

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if len(password) < 8:
            self.add_error('password', 'รหัสผ่านต้องอย่างน้อย 8 หลัก')


        if len(password2) < 8:
            self.add_error('password2', 'รหัสผ่านต้องอย่างน้อย 8 หลัก')


        if password != password2:
            self.add_error('password2', 'รหัสผ่านไม่ตรงกัน')

        return cleaned_data
