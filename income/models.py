from django.db import models
from category.models import Category, SubCategory  
from user_app.models import users  # Ensure correct import path

class Income(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='incomes', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name='incomes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # New field for creation timestamp
    

    def __str__(self):
        return self.title
