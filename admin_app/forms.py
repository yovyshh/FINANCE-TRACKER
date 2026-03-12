from .models import *
from django import forms

CATEGORY_CHOICES = [
    ('income', 'Income'),
    ('expense', 'Expense')
]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = IncomeCategory
        fields = ['category_name', 'category_type', 'category_description']
        widgets = {
            'category_name': forms.TextInput(attrs={
                'name': 'category_name', 
                'required': True, 
                'class': 'input', 
                'placeholder': 'Enter category name'
            }),
            'category_type': forms.Select(choices=CATEGORY_CHOICES, attrs={
                'name': 'category_type', 
                'required': True, 
                'class': 'input', 
                'placeholder': 'Select category type'
            }),
            'category_description': forms.TextInput(attrs={
                'name': 'category_description', 
                'required': True, 
                'class': 'input', 
                'placeholder': 'Enter category description'
            })
        }
        labels = {
            'category_name': '',  # No label for cleaner UI
        }
        help_texts = {
            'category_name': None,  # No help text
        }



# class ExpenseForm(forms.ModelForm):
#     class Meta:
#         model = Expense
#         fields = ['user', 'category', 'amount', 'date_incurred']
#         widgets = {
#             'user': forms.Select(attrs={
#                 'id': 'user', 
#                 'required': True, 
#                 'class': 'input'
#             }),
#             'category': forms.Select(attrs={
#                 'id': 'category', 
#                 'required': True, 
#                 'class': 'input'
#             }),
#             'amount': forms.NumberInput(attrs={
#                 'id': 'amount', 
#                 'required': True, 
#                 'class': 'input', 
#                 'placeholder': 'Enter expense amount'
#             }),
#             'date_incurred': forms.DateInput(attrs={
#                 'id': 'date_incurred', 
#                 'required': True, 
#                 'class': 'input', 
#                 'type': 'date'
#             }),
#         }
#         labels = {
#             'user': 'User',
#             'category': 'Category',
#             'amount': 'Amount',
#             'date_incurred': 'Date Incurred',
#         }
#         help_texts = {
#             'user': None,
#             'category': None,
#             'amount': None,
#             'date_incurred': None,
#         }

# class BudgetForm(forms.ModelForm):
#     class Meta:
#         model = Budget
#         fields = ['user', 'total_budget', 'start_date', 'end_date']
#         widgets = {
#             'user': forms.Select(attrs={
#                 'id': 'user', 
#                 'required': True, 
#                 'class': 'input'
#             }),
#             'total_budget': forms.NumberInput(attrs={
#                 'id': 'total_budget', 
#                 'required': True, 
#                 'class': 'input', 
#                 'placeholder': 'Enter total budget'
#             }),
#             'start_date': forms.DateInput(attrs={
#                 'id': 'start_date', 
#                 'required': True, 
#                 'class': 'input', 
#                 'type': 'date'
#             }),
#             'end_date': forms.DateInput(attrs={
#                 'id': 'end_date', 
#                 'required': True, 
#                 'class': 'input', 
#                 'type': 'date'
#             }),
#         }
#         labels = {
#             'user': 'User',
#             'total_budget': 'Total Budget',
#             'start_date': 'Start Date',
#             'end_date': 'End Date',
#         }
#         help_texts = {
#             'user': None,
#             'total_budget': None,
#             'start_date': None,
#             'end_date': None,
#         }