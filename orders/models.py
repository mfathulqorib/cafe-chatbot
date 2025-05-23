from django.db import models

from core.models import BaseModel
from menu.models import MenuItem


class Order(BaseModel):
    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Cash"
        DEBIT = "debit", "Debit"
        CREDIT = "credit", "Credit"
        QRIS = "qris", "QRIS"

    date = models.DateTimeField()
    customer_name = models.CharField(max_length=50)
    customer_phone = models.CharField(max_length=15, blank=True, null=True)
    items = models.ManyToManyField(MenuItem, through="OrderItem")
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)
    total_amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Order {self.customer_name} on {self.date.strftime('%Y-%m-%d %H:%M')}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return f"{self.order}: {self.quantity} x {self.menu_item.name}"
