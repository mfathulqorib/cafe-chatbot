from django.db import models
from core.models import BaseModel

# Create your models here.

class MenuItem(BaseModel):
    class Category(models.TextChoices):
        DESSERT = 'dessert', 'Dessert'
        COFFEE = 'coffee', 'Coffee'
        TEA = 'tea', 'Tea'
        MAIN_COURSE = 'main_course', 'Main Course'
        SNACK = 'snack', 'Snack'
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )

    def __str__(self):
        return f"{self.name} - {self.category.title()} ({self.formatted_price()})"

    def formatted_price(self):
        return f"Rp {int(self.price):,}".replace(",", ".")

