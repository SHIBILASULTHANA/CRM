# forms.py

from django import forms
from .models import Board

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name']

class ListForm(forms.Form):
    list_name = forms.CharField(max_length=100)