from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render
from django.views.generic import View

from .models import MenuItem


# Create your views here.
class CreateMenu(LoginRequiredMixin, View):
    login_url = "/login/"
    categories = MenuItem.Category.choices
    context = {"categories": categories}

    def get(self, request):
        return render(request, "menu/create/page.html", self.context)

    def post(self, request):
        data = request.POST.dict()
        template_page = "menu/create/page.html"

        menu_data = {
            "name": data.get("name"),
            "price": data.get("price").replace(".", ""),
            "description": data.get("description"),
            "category": data.get("category"),
        }

        if not menu_data["name"] or not menu_data["price"] or not menu_data["category"]:
            messages.error(request, "Please fill out all required fields.")
            return render(request, template_page, dict(self.context, **menu_data))

        if MenuItem.objects.filter(name=menu_data["name"]).exists():
            messages.error(request, "Menu is already registered")
            return render(request, template_page, dict(self.context, **menu_data))

        try:
            MenuItem.objects.create(**menu_data)
        except IntegrityError:
            messages.error(request, "Something wrong, please cek again your input")
            return render(request, template_page, dict(self.context, **menu_data))

        messages.success(request, "Menu successfully created")
        return render(request, template_page, self.context)
