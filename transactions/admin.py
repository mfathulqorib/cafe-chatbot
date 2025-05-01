from django.contrib import admin
from .models import Transaction, TransactionItem

# Register your models here.

admin.site.register([Transaction, TransactionItem])