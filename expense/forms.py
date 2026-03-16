from django import forms
from .models import Expense
from budget.models import Budget
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from category.models import Category, SubCategory
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'description', 'amount', 'category', 'subcategory', 'date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(type="Expense")
        else:
            self.fields['category'].queryset = Category.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                self.fields['subcategory'].queryset = SubCategory.objects.none()
        elif self.instance.pk and hasattr(self.instance, 'category') and self.instance.category:
            self.fields['subcategory'].queryset = SubCategory.objects.filter(category=self.instance.category)
        else:
            self.fields['subcategory'].queryset = SubCategory.objects.none()

        self.fields['date'].initial = date.today()

    def clean_date(self):
        selected_date = self.cleaned_data.get('date')
        today = date.today()
        valid_date_range_start = today - timedelta(days=7)
        valid_date_range_end = today

        if not (valid_date_range_start <= selected_date <= valid_date_range_end):
            raise ValidationError(
                f"Please select a date between {valid_date_range_start.strftime('%Y-%m-%d')} and {valid_date_range_end.strftime('%Y-%m-%d')}."
            )
        return selected_date