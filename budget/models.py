from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from expense.models import Expense


class Budget(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    expiry_date = models.DateField()
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Add this line
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    # def remaining_balance(self):
    #     total_expenses = Expense.objects.filter(
    #         user=self.user,
    #         date__range=[self.start_date, self.expiry_date]
    #     ).aggregate(Sum('amount'))['amount__sum'] or 0
    #     return self.initial_amount - total_expenses

    @property
    def is_active(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.expiry_date

    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.expiry_date})"
    
    def __str__(self):
        return f"{self.name}"
    
    # def save(self, *args, **kwargs):
    #     # Calculate the remaining amount dynamically if it's not set
    #     if self.remaining_amount is None:
    #         self.remaining_amount = self.remaining_balance()  # Set remaining amount as the calculated balance
    #     super().save(*args, **kwargs)


