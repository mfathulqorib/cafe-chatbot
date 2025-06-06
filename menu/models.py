from django.db import models

from core.models import BaseModel


class MenuItem(BaseModel):
    class Category(models.TextChoices):
        DESSERT = "dessert", "Dessert"
        COFFEE = "coffee", "Coffee"
        TEA = "tea", "Tea"
        MAIN_COURSE = "main_course", "Main Course"
        SNACK = "snack", "Snack"

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=20, choices=Category.choices)

    def __str__(self):
        return f"{self.name} - {self.get_category_display()} ({self.formatted_price()})"

    def formatted_price(self):
        return f"Rp {int(self.price):,}".replace(",", ".")
    
    def get_category_display(self):
        return self.Category(self.category).label
    
