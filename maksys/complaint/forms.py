from django import forms
from .models import Complaint
from web.models import Employee

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['complaint_name', 'start_date', 'category', 'brand', 'serial_no', 'client', 'summary']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AssignComplaintForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), empty_label="Select Employee")
    remarks = forms.CharField(widget=forms.Textarea)