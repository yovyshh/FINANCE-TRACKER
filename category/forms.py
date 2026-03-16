from django import forms
from .models import Category
from .models import SubCategory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'description', 'type', 'max_limit']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control medium-description',
                'rows': 5,
                'cols': 40
            }),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'max_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['title']
