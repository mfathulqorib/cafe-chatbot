from django.urls import path

from .views import CreateOrder, ListOrder

urlpatterns = [
    path("order/create/", CreateOrder.as_view(), name="create-order"),
    path("order/", ListOrder.as_view(), name="list-order"),
]
