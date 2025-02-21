from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Months(models.Model):
    year = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    beginning_balance = models.FloatField()
    ending_balance = models.FloatField()

    