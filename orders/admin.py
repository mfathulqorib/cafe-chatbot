from django.contrib import admin

from .models import Order, OrderItem

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order", "menu_item", "quantity", "total_amount")

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)