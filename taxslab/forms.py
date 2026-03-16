from django import forms
from .models import TaxSlab

class TaxSlabForm(forms.ModelForm):
    class Meta:
        model = TaxSlab
        fields = ['min_limit', 'max_limit', 'tax_percentage']
