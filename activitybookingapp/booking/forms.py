
from django import forms
from django.forms import ModelForm, ValidationError
from booking.models import *
from django.utils import timezone

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        is_edit = kwargs.get('instance') is not None
        super(ReportForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight font-normal'
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

    def clean(self):
        cleaned_data = super().clean()
        card = cleaned_data.get("card")
        location = cleaned_data.get("location")
        description = cleaned_data.get("description")
    
        if card is not None:
            if card < 0 and card > 4:
                self.add_error('card', 'The number of cards must be between 1 and 4.')
        
        if location and len(location) < 10:
            self.add_error('location', 'Location must be at least 10 characters long.')
        
        if description and len(description) < 20:
            self.add_error('description', 'Description must be at least 20 characters long.')
        
        return cleaned_data