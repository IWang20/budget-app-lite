from django.contrib import admin
from .models import Transaction

# Register your models here.
# this customize the look of the admin panel 
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'description', 'category', 'amount')

admin.site.register(Transaction, TransactionAdmin)