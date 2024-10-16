
from django import forms
from django.forms import ModelForm, ValidationError
from booking.models import *
from django.utils import timezone

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student 
        fields = ['first_name', 'last_name', 'faculty', 'stu_card', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18",
                'placeholder': 'First Name'  # Changed to First Name
            }),
            'last_name': forms.TextInput(attrs={
                'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18",
                'placeholder': 'Last Name'  # Changed to Last Name
            }),
            'faculty': forms.Select(
                attrs={
                    'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18"
                },
                choices=Student.FACULTIES
            ),
            'stu_card': forms.TextInput(attrs={
                'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18",
                'placeholder': 'Student Card'  # Changed to Student Card
            }),
            'email': forms.EmailInput(attrs={
                'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18",
                'placeholder': 'Email'  # Changed to Email
            }),
            'phone': forms.TextInput(attrs={
                'class': "text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-18",
                'placeholder': 'Phone Number'  # Changed to Phone Number
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email:
            username_part = email.split('@')[0]
            if not email.endswith('@kmitl.ac.th') or len(username_part) != 8:
                self.add_error('email', 'อีเมลต้องใช้โดเมน @kmitl.ac.th')

        phone = cleaned_data.get('phone')
        if len(phone) != 10:
            self.add_error('phone', 'เบอร์โทรศัพท์ต้องมี 10 หลัก')

        student_ID = cleaned_data.get('stu_card')
        if len(student_ID) != 8:
            self.add_error('stu_card', 'หมายเลขนักเรียนต้องมี 8 หลัก')
        
        return cleaned_data


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = "__all__"
        widgets = {
            'image': forms.ClearableFileInput(
                attrs={
                    'class':"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal",
                    'accept':'image/*',
                }
            ),
            "place": forms.Select(
                attrs={
                    'class':"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal"
                }
            ),
            "student": forms.Select(
                attrs={
                    'class':"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal"
                }
            ),
            "details": forms.Textarea(
                attrs={
                    'class':"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal"
                }
            ),
            "created_at": forms.TextInput(
                attrs={
                    'class':"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal"
                }
            ),
            "status":forms.Select(
                attrs={
                    'class':"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal"
                }
            )
        }
    
    def __init__(self, *args, **kwargs):
        is_edit = kwargs.get('instance') is not None
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['created_at'].disabled = True

        if is_edit:
            self.fields['student'].disabled = True
            self.fields['place'].disabled = True
            self.fields['details'].disabled = True

        else:
            self.fields['status'].disabled = True

    
    def clean_details(self):
        details = self.cleaned_data.get('details')
        if details and len(details) < 10:
            raise forms.ValidationError('Location must be at least 10 characters long.')
        return details

    
class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-[300px]", 
                'placeholder': 'ชื่อสนาม'}),
            'activity': forms.Select(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-[300px]"}),
            'location': forms.TextInput(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-[300px]", 
                'placeholder': 'ที่ตั้งสนาม'}),
            'description': forms.Textarea(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-[400px]", 
                'placeholder': 'รายละเอียดของสนาม',
                'style': 'resize: none;'}),
            'card': forms.NumberInput(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-[300px]",
                'placeholder': 'จำนวนบัตรที่ต้องใช้จอง'}),
            'staff': forms.CheckboxSelectMultiple(attrs={
                'class': "mt-2 mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 px-20"}),
            'photo': forms.ClearableFileInput(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
                'accept': 'image/*',
                'style': 'padding: 10px;',
                'id': 'photo-input'}),
        }

    def clean_card(self):
            card = self.cleaned_data.get('card')
            if card is not None and (card < 1 or card > 4):
                raise forms.ValidationError('The number of cards must be between 1 and 4.')
            return card

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if location and len(location) < 10:
            raise forms.ValidationError('Location must be at least 10 characters long.')
        return location

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) < 15:
            raise forms.ValidationError('Description must be at least 20 characters long.')
        return description