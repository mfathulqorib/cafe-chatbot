from django.urls import path

from .views import CreateTransaction, ListTransaction

urlpatterns = [
    path("transaction/create/", CreateTransaction.as_view(), name="create-transaction"),
    path("transaction/", ListTransaction.as_view(), name="list-transaction"),
]
