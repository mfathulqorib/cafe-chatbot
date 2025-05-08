from django.urls import path

from .views import CreateTransaction

urlpatterns = [
    path("transaction/create/", CreateTransaction.as_view(), name="create-transaction"),
]
