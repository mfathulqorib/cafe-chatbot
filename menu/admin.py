from django.contrib import admin

from .models import MenuItem


# Register your models here.
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "description",
        "category",
    )


admin.site.register(MenuItem, MenuItemAdmin)
