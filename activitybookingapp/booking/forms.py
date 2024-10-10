
from django import forms
from django.forms import ModelForm, ValidationError
from booking.models import *
from django.utils import timezone

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = "__all__"
        # widgets = {
        #     "place": forms.Select(
        #         attrs={
        #             'class':"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal"
        #         }
        #     ),
        #     "student": forms.TextInput(
        #         attrs={
        #             'class':"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal"
        #         }
        #     ),
        #     "details": forms.Textarea(
        #         attrs={
        #             'class':"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal"
        #         }
        #     ),
        #     "created_at": forms.DateTimeField(
        #         attrs={
        #             'class':"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal"
        #         }
        #     ),
        #     "status":forms.Select(
        #         attrs={
        #             'class':"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal"
        #         }
        #     )
        # }
    
    def __init__(self, *args, **kwargs):
        is_edit = kwargs.get('instance') is not None
        super(ReportForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal'
        
        self.fields['student'].disabled = True
        # self.fields['place'].disabled = True
        self.fields['created_at'].disabled = True

        if is_edit:
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
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64", 
                'placeholder': 'Place Name'}),
            'activity': forms.Select(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64"
            }),
            'location': forms.TextInput(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64", 
                'placeholder': 'Location'}),
            'description': forms.Textarea(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64", 
                'placeholder': 'Description'}),
            'card': forms.NumberInput(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
                'placeholder': 'จำนวนบัตรที่ต้องใช้จอง'
            }),
            'staff': forms.CheckboxSelectMultiple(attrs={
                'class': "mt-2 mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200"
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': "mb-3 text-xs rounded-lg p-2.5 border-solid border-2 border-gray-200 w-64",
                'accept': 'image/*',
                'style': 'padding: 10px;',
                'placeholder': 'อัปโหลดรูปภาพ',
            }),
        }

        
        

