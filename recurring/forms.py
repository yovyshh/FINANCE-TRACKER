from django import forms
from .models import Recurring

class RecurringTransactionForm(forms.ModelForm):
    class Meta:
        model = Recurring
        fields = ['title', 'amount', 'date', 'type', 'category', 'subcategory']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
