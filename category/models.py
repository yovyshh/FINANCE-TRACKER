from django.db import models
from django.conf import settings  # Import settings to access AUTH_USER_MODEL

class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(
        max_length=20,
        choices=[('Income', 'Income'), ('Expense', 'Expense')]
    )
    max_limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title  # Displaying the title of the category


class SubCategory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    category = models.ForeignKey(
        'Category', 
        related_name='subcategories', 
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
