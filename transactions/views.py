from django.shortcuts import render
from django.views.generic import View
from menu.models import MenuItem
from transactions.models import Transaction, TransactionItem
from django.contrib import messages
from decimal import Decimal
from rich import print

class CreateTransaction(View):
    context = {}

    def get(self, request):
        payment_methods = Transaction.PaymentMethod.choices
        menu_items = MenuItem.objects.all()

        self.context["menu_items"] = menu_items
        self.context["payment_methods"] = payment_methods
        
        return render(request, 'transactions/create/page.html', self.context)
    
    def post(self, request):
        data = request.POST.dict()
        context = self.context
        context["form_data"] = data

        if not data.get('customer_name') or not data.get('date') or not data.get('payment_method'):
            messages.error(request, "Please fill out all required fields.")
            return render(request, 'transactions/create/page.html', context)
        
        # Create the transaction
        transaction = Transaction.objects.create(
            actor=request.user if request.user.is_authenticated else None,
            date=data.get('date'),
            customer_name=data.get('customer_name'),
            customer_phone=data.get('customer_phone'),
            payment_method=data.get('payment_method'),
        )

        # Extract dynamic items from form
        index = 0
        while f"id_{index}" in data:
            print(f"processing index: {index}")
            try:
                menu_id = data.get(f"id_{index}")
                quantity = int(data.get(f"quantity_{index}", "1"))
                price = Decimal(data.get(f"price_{index}", "0"))

                menu_item = MenuItem.objects.get(id=menu_id)

                TransactionItem.objects.create(
                    transaction=transaction,
                    menu_item=menu_item,
                    quantity=quantity,
                    total_amount=price * quantity
                )
            except MenuItem.DoesNotExist:
                messages.warning(request, f"Menu item {menu_id} not found.")
            except Exception as e:
                messages.error(request, f"Error processing item {index}: {e}")
                return render(request, 'menu/create/page.html', context)
            
            index += 1

        messages.success(request, "Transaction created successfully.")
        
        context["form_data"] = {}
        return render(request, 'transactions/create/page.html', context)
