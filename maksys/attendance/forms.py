# forms.py

from django import forms
from .models import AttendanceSettings

class AttendanceSettingsForm(forms.ModelForm):
    class Meta:
        model = AttendanceSettings
        fields = ['office_time', 'late_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom attributes to input fields to support 12-hour format
        self.fields['office_time'].widget = forms.TimeInput(format='%I:%M %p', attrs={'placeholder': 'HH:MM AM/PM'})
        self.fields['late_time'].widget = forms.TimeInput(format='%I:%M %p', attrs={'placeholder': 'HH:MM AM/PM'})
        self.fields['end_time'].widget = forms.TimeInput(format='%I:%M %p', attrs={'placeholder': 'HH:MM AM/PM'})

    def clean(self):
        cleaned_data = super().clean()
        # Add any custom validation logic here
        return cleaned_data
