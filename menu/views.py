from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.generic import View

from core.utils import format_currency

from .filters import MenuItemFilter
from .models import MenuItem


class ListMenu(LoginRequiredMixin, View):
    login_url = "/login/"
    categories = MenuItem.Category.choices

    def get(self, request):
        menu_items = MenuItem.objects.all()
        menu_filter = MenuItemFilter(request.GET, queryset=menu_items)
        filtered_items = menu_filter.qs

        # Pagination
        page = request.GET.get("page", 1)
        items_per_page = 5  # Adjust number of items per page as needed
        paginator = Paginator(filtered_items, items_per_page)

        try:
            paginated_items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page
            paginated_items = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results
            paginated_items = paginator.page(paginator.num_pages)

        # Format the price and category display names
        for menu in paginated_items:
            menu.price = format_currency(menu.price)
            for key, value in self.categories:
                if menu.category == key:
                    menu.category = value

        return render(
            request,
            "menu/page.html",
            {
                "menu_items": paginated_items,
                "menu_filter": menu_filter,
                "categories": self.categories,
                "is_paginated": paginator.num_pages > 1,
                "page_obj": paginated_items,
            },
        )


class CreateMenu(LoginRequiredMixin, View):
    login_url = "/login/"
    categories = MenuItem.Category.choices
    breadcrumbs = [
        {"label": "Menus", "href": "/menu/", "active": False},
        {"label": "Create Menu", "href": "/menu/create/", "active": True},
    ]
    breadcrumbs_description = "Add a new menu item to your collection."
    context = {
        "categories": categories,
        "breadcrumbs": breadcrumbs,
        "breadcrumbs_description": breadcrumbs_description,
    }

    def get(self, request):
        context = {}
        context.update(self.context)
        return render(request, "menu/create/page.html", context)

    def post(self, request):
        data = request.POST.dict()
        template_page = "menu/create/page.html"
        context = {}
        context.update(self.context)

        menu_data = {
            "name": data.get("name"),
            "price": data.get("price").replace(".", ""),
            "description": data.get("description"),
            "category": data.get("category"),
        }

        if not menu_data["name"] or not menu_data["price"] or not menu_data["category"]:
            messages.error(request, "Please fill out all required fields.")
            context.update(menu_data)
            return render(request, template_page, context)

        if MenuItem.objects.filter(name=menu_data["name"]).exists():
            messages.error(request, "Menu is already registered")
            context.update(menu_data)
            return render(request, template_page, context)

        try:
            MenuItem.objects.create(**menu_data)
        except IntegrityError:
            messages.error(request, "Something wrong, please cek again your input")
            return render(request, template_page, dict(self.context, **menu_data))

        messages.success(request, "Menu successfully created")
        return render(request, template_page, context)


class UpdateMenu(LoginRequiredMixin, View):
    login_url = "/login/"
    model = MenuItem
    template_name = "menu/create/page.html"
    breadcrumbs = [
        {"label": "Menus", "href": "/menu/", "active": False},
        {"label": "Edit Menu", "href": "/menu/update/", "active": True},
    ]
    breadcrumbs_description = "Edit a menu item in your collection."

    context = {
        "breadcrumbs": breadcrumbs,
        "breadcrumbs_description": breadcrumbs_description,
    }

    def get(self, request, *args, **kwargs):
        menu_id = kwargs.get("id")
        menu = MenuItem.objects.get(id=menu_id)
        categories = MenuItem.Category.choices

        context = self.context
        context.update(
            {
                "categories": categories,
                "name": menu.name,
                "price": int(menu.price),
                "description": menu.description,
                "category": menu.category,
                "menu_id": menu_id,
            }
        )

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Get the menu item ID from URL parameters
        menu_id = kwargs.get("id")
        # Fetch the menu item using the ID
        menu = MenuItem.objects.get(id=menu_id)

        data = request.POST.dict()
        categories = MenuItem.Category.choices

        menu_data = {
            "name": data.get("name"),
            "price": data.get("price").replace(".", ""),
            "description": data.get("description"),
            "category": data.get("category"),
        }

        if not menu_data["name"] or not menu_data["price"] or not menu_data["category"]:
            messages.error(request, "Please fill out all required fields.")
            context = self.context
            context.update({"categories": categories, **menu_data})
            return render(request, self.template_name, context)

        try:
            # Update the menu item with the new data
            for key, value in menu_data.items():
                setattr(menu, key, value)
            menu.save()
        except IntegrityError:
            messages.error(request, "Something wrong, please check again your input")
            context = self.context
            context.update({"categories": categories, **menu_data})
            return render(request, self.template_name, context)

        messages.success(request, "Menu successfully updated")
        return redirect("list-menu")


class DeleteMenu(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        menu_id = kwargs.get("id")
        menu = MenuItem.objects.get(id=menu_id)
        menu.delete()
        messages.success(request, "Menu successfully deleted")
        return redirect("list-menu")
