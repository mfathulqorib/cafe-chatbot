from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class CreateTransaction(View):
    def get(self, request):
        return render(request, 'transactions/create.html')