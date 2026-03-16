from django.db import models
from django.conf import settings
from category.models import Category, SubCategory

class Recurring(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=20,
        choices=[('Income', 'Income'), ('Expense', 'Expense')]
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.amount} - {self.date}"   
