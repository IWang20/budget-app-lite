from django.db import models

# Create your models here.

class Transaction(models.Model):
    date = models.DateField()
    type = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    amount = models.FloatField()

    def _str_(self):
        return self.category

