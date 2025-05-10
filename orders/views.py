from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View
from core.utils import format_currency, format_asia_jakarta_datetime, get_datetime_now
from .filters import OrderFilter

from menu.models import MenuItem
from orders.models import Order, OrderItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


class ListOrder(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        orders = Order.objects.all().order_by("-date")
        order_filter = OrderFilter(request.GET, queryset=orders)
        filtered_orders = order_filter.qs

        # Pagination
        page = request.GET.get("page", 1)
        items_per_page = 3  # Adjust number of items per page as needed
        paginator = Paginator(filtered_orders, items_per_page)

        try:
            paginated_orders = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page
            paginated_orders = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results
            paginated_orders = paginator.page(paginator.num_pages)

        for order in paginated_orders:
            # Format the date to Asia/Jakarta timezone (UTC+7)
            order.formatted_date = format_asia_jakarta_datetime(order.date)
            # Format the currency
            order.total_amount = format_currency(order.total_amount)
            # Add formatted date for the date input field (YYYY-MM-DD)
            order.input_date = order.date.strftime('%Y-%m-%d')
        
        # Get the current filter date in the correct format for the date input
        filter_date = request.GET.get('date', '')
        
        return render(request, "orders/page.html", {
            "orders": paginated_orders, 
            "order_filter": order_filter, 
            "is_paginated": paginator.num_pages > 1, 
            "page_obj": paginated_orders,
            "filter_date": filter_date
        })


class CreateOrder(LoginRequiredMixin, View):
    login_url = "/login/"
    breadcrumbs = [
        {"label": "Orders", "href": "/order/", "active": False},
        {"label": "Create Order", "href": "/order/create/", "active": True},
    ]
    breadcrumbs_description = "Add a new order to your collection."
    now = get_datetime_now()
    context = {
        "breadcrumbs": breadcrumbs,
        "breadcrumbs_description": breadcrumbs_description,
        "now": now,
    }

    def get(self, request):
        payment_methods = Order.PaymentMethod.choices
        menu_items = MenuItem.objects.all()

        context = self.context
        context.update({"payment_methods": payment_methods, "menu_items": menu_items})

        return render(request, "orders/create/page.html", context)

    def post(self, request):
        data = request.POST.dict()
        context = self.context
        payment_methods = Order.PaymentMethod.choices
        menu_items = MenuItem.objects.all()

        order_items = []
        for i in range(0, round((len(data)-6)/3)):
            if not data.get(f"id_{i}") or not data.get(f"name_{i}") or not data.get(f"price_{i}") or not data.get(f"quantity_{i}"):
                continue
            order_items.append({
                "id": data.get(f"id_{i}"),
                "name": data.get(f"name_{i}"),
                "price": int(data.get(f"price_{i}")),
                "qty": int(data.get(f"quantity_{i}")),
            })

        if (
            not data.get("customer_name")
            or not data.get("date")
            or not data.get("payment_method")
        ):
            messages.error(request, "Please fill out all required fields.")
            context.update({"payment_methods": payment_methods, "menu_items": menu_items, "order_items": order_items, **data})
            return render(request, "orders/create/page.html", context)

        if not data.get("id_0"):
            messages.error(request, "Please add at least one item to the order list.")
            context.update({"payment_methods": payment_methods, "menu_items": menu_items, "order_items": order_items, **data})
            return render(request, "orders/create/page.html", context)

        # Create the order
        order = Order.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            date=data.get("date"),
            customer_name=data.get("customer_name").capitalize().strip(),
            customer_phone=data.get("customer_phone"),
            payment_method=data.get("payment_method"),
            total_amount=data.get("total_amount"),
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
                    actor=request.user if request.user.is_authenticated else None,
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
                context.update({"payment_methods": payment_methods, "menu_items": menu_items, "form_data": data})
                return render(request, "orders/create/page.html", context)

            index += 1

        messages.success(request, "Order created successfully.")

        return redirect("create-order")

class UpdateOrder(LoginRequiredMixin, View):
    login_url = "/login/"
    model = Order
    template_name = "orders/create/page.html"
    breadcrumbs = [
        {"label": "Orders", "href": "/order/", "active": False},
        {"label": "Edit Order", "href": "/order/update/", "active": True},
    ]
    breadcrumbs_description = "Edit an order in your collection."
    context = {
        "breadcrumbs": breadcrumbs,
        "breadcrumbs_description": breadcrumbs_description,
    }

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("id")
        order = Order.objects.get(id=order_id)
        # Format the date to be used in HTML date input (YYYY-MM-DD)
        order.formatted_date_input = format_asia_jakarta_datetime(order.date)
        data = OrderItem.objects.filter(order=order_id)

        order_items = []
        for item in data:
            order_items.append({
                "order_id": order_id,
                "id": item.id,
                "name": item.menu_item.name,
                "price": int(item.menu_item.price),
                "qty": int(item.quantity),
        })

        payment_methods = Order.PaymentMethod.choices
        menu_items = MenuItem.objects.all()

        context = self.context
        context.update({"payment_methods": payment_methods, "menu_items": menu_items, "order_items": order_items, **order.__dict__})
        print(context)
        return render(request, "orders/create/page.html", context)
    
    def post(self, request, *args, **kwargs):
        order_id = kwargs.get("id")
        order = Order.objects.get(id=order_id)
        data = request.POST.dict()

        order_items = []
        for i in range(0, round((len(data)-6)/3)):
            if not data.get(f"id_{i}") or not data.get(f"name_{i}") or not data.get(f"price_{i}") or not data.get(f"quantity_{i}"):
                continue
            order_items.append({
                "id": data.get(f"id_{i}"),
                "name": data.get(f"name_{i}"),
                "price": int(data.get(f"price_{i}")),
                "qty": int(data.get(f"quantity_{i}")),
            })

        try:
            for key, value in data.items():
                setattr(order, key, value)
            order.customer_name = order.customer_name.capitalize().strip()
            order.save()
        except IntegrityError:
            messages.error(request, "Something wrong, please check again your input")
            context = self.context
            context.update({"payment_methods": payment_methods, "menu_items": menu_items, "order_items": order_items, **order.__dict__})
            return render(request, "orders/create/page.html", context)

        try:
            for item in order_items:
                order_item = OrderItem.objects.get(id=item["id"])
                order_item.quantity = item["qty"]
                order_item.save()
        except OrderItem.DoesNotExist:
            messages.warning(request, f"Order item {item['id']} not found.")
        except Exception as e:
            messages.error(request, f"Error processing item {item['id']}: {e}")
            order.delete()
            context.update({"payment_methods": payment_methods, "menu_items": menu_items, "form_data": data})
            return render(request, "orders/create/page.html", context)
        
        messages.success(request, "Order successfully updated")
        return redirect("list-order")
        
        

class DeleteOrder(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("id")
        order = Order.objects.get(id=order_id)
        order.delete()
        messages.success(request, "Order successfully deleted")
        return redirect("list-order")
