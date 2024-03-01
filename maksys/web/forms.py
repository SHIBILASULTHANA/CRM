from django import forms
from .models import Department,Employee,Client

from django.contrib.auth import get_user_model
User = get_user_model()

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class EmployeeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        exclude = ['user']  # Exclude the 'user' field
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        
class ClientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Client
        exclude = ['user']
