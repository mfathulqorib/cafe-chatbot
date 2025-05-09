from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View
from rich import print

from menu.models import MenuItem
from orders.models import Order, OrderItem


class ListOrder(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        orders = Order.objects.all()
        return render(request, "orders/page.html", {"orders": orders})


class CreateOrder(LoginRequiredMixin, View):
    login_url = "/login/"
    context = {}

    def get(self, request):
        payment_methods = Order.PaymentMethod.choices
        menu_items = MenuItem.objects.all()

        self.context["menu_items"] = menu_items
        self.context["payment_methods"] = payment_methods

        return render(request, "orders/create/page.html", self.context)

    def post(self, request):
        data = request.POST.dict()
        context = self.context

        if (
            not data.get("customer_name")
            or not data.get("date")
            or not data.get("payment_method")
        ):
            messages.error(request, "Please fill out all required fields.")
            return render(request, "orders/create/page.html", dict(context, **data))

        if not data.get("id_0"):
            messages.error(request, "Please add at least one item to the order list.")
            return render(request, "orders/create/page.html", dict(context, **data))

        # Create the order
        order = Order.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            date=data.get("date"),
            customer_name=data.get("customer_name"),
            customer_phone=data.get("customer_phone"),
            payment_method=data.get("payment_method"),
        )

        # Extract dynamic items from form
        index = 0
        while f"id_{index}" in data:
            try:
                menu_id = data.get(f"id_{index}")
                quantity = int(data.get(f"quantity_{index}", "1"))
                price = Decimal(data.get(f"price_{index}", "0"))

                menu_item = MenuItem.objects.get(id=menu_id)

                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity,
                    total_amount=price * quantity,
                )
            except MenuItem.DoesNotExist:
                messages.warning(request, f"Menu item {menu_id} not found.")
            except Exception as e:
                messages.error(request, f"Error processing item {index}: {e}")
                order.delete()
                return render(request, "orders/create/page.html", context)

            index += 1

        messages.success(request, "Order created successfully.")

        context["form_data"] = {}
        return render(request, "orders/create/page.html", context)
