from django.db import models
from admin_app import*
from django.contrib.auth.models import AbstractUser

class Register(AbstractUser):
    usertype=models.IntegerField(default=1,null=True)
    contact=models.IntegerField(default=1,null=True)
    place=models.IntegerField(default=1,null=True)
    image=models.IntegerField(null=True)



class Income(models.Model):
    income_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, null=False)
    category = models.CharField(max_length=50, null=False)
    amount_of_income = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    date_received = models.DateField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.user_name} - {self.category} - {self.amount_of_income}"
    


class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)  # Links to the Register model (custom user model)
    # category = models.ForeignKey('ExpenseCategory', on_delete=models.CASCADE)  # Links to the corresponding expense category
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    date_incurred = models.DateField(null=False)

    def __str__(self):
        return f"Expense {self.expense_id} - Amount: {self.amount}"

class Budget(models.Model):
    budget_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)  # Links to the Register model (custom user model)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

    def __str__(self):
        return f"Budget {self.budget_id} - Total: {self.total_budget}"

class BudgetSource(models.Model):
    SOURCE_TYPES = [
        ('salary', 'Salary'),
        ('investment', 'Investment'),
        ('loan', 'Loan'),
        ('other', 'Other'),
    ]
    
    source_id = models.AutoField(primary_key=True)
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE)  # Links to the Budget model
    source_name = models.CharField(max_length=255, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES, null=False)

    def __str__(self):
        return f"{self.source_name} - {self.source_type} - Amount: {self.amount}"
    
class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    date_submitted = models.DateField(auto_now_add=True)  # Automatically set to the current date
    rating = models.IntegerField(null=False)  # Rating given by the user
    user = models.ForeignKey(Register, on_delete=models.CASCADE, null=False)  # Links to the Register model (custom user model)
    message = models.CharField(max_length=255, null=False)

    

    def __str__(self):
        return f"Feedback {self.feedback_id} - Rating: {self.rating}"

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name