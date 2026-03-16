from django import forms
from .models import Income, Category, SubCategory
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['title', 'description', 'amount', 'category', 'subcategory']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'cols': 40,
                'placeholder': 'Add a brief description...',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a title...',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the amount...',
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Extract the user argument
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter categories to include only those with type="Income" for the user
        if user:
            self.fields['category'].queryset = Category.objects.filter(type="Income")
        else:
            self.fields['category'].queryset = Category.objects.none()

        # Dynamically filter subcategories based on the selected category
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                self.fields['subcategory'].queryset = SubCategory.objects.none()
        elif self.instance and hasattr(self.instance, 'category') and self.instance.category:
            # Safely check if instance has a category before accessing it
            self.fields['subcategory'].queryset = SubCategory.objects.filter(category=self.instance.category)
        else:
            self.fields['subcategory'].queryset = SubCategory.objects.none()
