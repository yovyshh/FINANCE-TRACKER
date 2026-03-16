from django import forms
from django.forms.widgets import DateInput
from .models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'start_date', 'expiry_date', 'initial_amount', 'description']

    start_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    expiry_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
