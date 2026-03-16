from django.db import models

class TaxSlab(models.Model):
    min_limit = models.DecimalField(max_digits=10, decimal_places=2)
    max_limit = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Tax Slab: {self.min_limit} - {self.max_limit} at {self.tax_percentage}%"
