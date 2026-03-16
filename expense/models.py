from django.db import models
from django.conf import settings
from decimal import Decimal
from user_app.models import*
from category.models import SubCategory  
from category.models import Category
from budget.models import *


  

# Create your models here.

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='expenses', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name='expenses', on_delete=models.CASCADE)
    budget = models.ForeignKey('budget.Budget', on_delete=models.CASCADE)
    date = models.DateField(null=True)


    def __str__(self):
        return self.title
    
  

    
class BudgetHistory(models.Model):
    budget = models.ForeignKey('budget.Budget', related_name='history', on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, related_name='history', on_delete=models.CASCADE)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"History for {self.budget.name} on {self.date}"
