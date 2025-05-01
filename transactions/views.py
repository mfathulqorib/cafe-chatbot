from django.shortcuts import render
from django.views.generic import View
from menu.models import MenuItem
from transactions.models import Transaction

# Create your views here.
class CreateTransaction(View):
    menu_items = MenuItem.objects.all()
    payment_methods = Transaction.PaymentMethod.choices
    context = {"menu_items": menu_items, "payment_methods": payment_methods}

    def get(self, request):
        return render(request, 'transactions/create.html', self.context)
    
    def post(self, request):
        data = request.POST.dict()
        context = self.context
        context["form_data"] = data

        if not data.get('payment_method'):
            return render(request, 'transactions/create.html', context)
        
        context["form_data"] = {}

        return render(request, 'transactions/create.html', context)
