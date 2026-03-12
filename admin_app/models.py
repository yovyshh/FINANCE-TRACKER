from django.db import models
from user.models import *

class IncomeCategory(models.Model):
    category_name = models.CharField(max_length=20, default='', null=True)  # Unique ID for the income category
    category_type = models.CharField(max_length=100, null=False)  # E.g., "Salary", "Business", etc.
    category_description = models.TextField(null=True, blank=True)  # Optional description for the income type

    def __str__(self):
        return f"{self.category_type} - {self.category_description or 'No Description'}"


class SubCategory(models.Model):
    category_name = models.CharField(max_length=20, default='', null=True)  # Subcategory name
    parent_category = models.ForeignKey(
        IncomeCategory, 
        on_delete=models.CASCADE,  # Cascade delete: delete subcategories if parent category is deleted
        related_name='subcategories',  # Related name for reverse lookup
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.category_name} (Under: {self.parent_category.category_name if self.parent_category else 'None'})"

