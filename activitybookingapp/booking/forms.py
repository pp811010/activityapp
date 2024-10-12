
from django import forms
from django.forms import ModelForm, ValidationError
from booking.models import *
from django.utils import timezone

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

    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


    
class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-[300px]", 
                'placeholder': 'ชื่อสนาม'}),
            'activity': forms.Select(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-[300px]"
            }),
            'location': forms.TextInput(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-[300px]", 
                'placeholder': 'ที่ตั้งสนาม'}),
            'description': forms.Textarea(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-[400px]", 
                'placeholder': 'รายละเอียดของสนาม',
                'style': 'resize: none;'
            }),
            'card': forms.NumberInput(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-[300px]",
                'placeholder': 'จำนวนบัตรที่ต้องใช้จอง'
            }),
            'staff': forms.CheckboxSelectMultiple(attrs={
                'class': "mt-2 mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 px-20" 
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
                'accept': 'image/*',
                'style': 'padding: 10px;',
                'placeholder': 'อัปโหลดรูปภาพสถานที่',
                'id': 'photo-input'
            }),
        }

        
        

