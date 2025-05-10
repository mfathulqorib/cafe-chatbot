from django.urls import path

from .views import CreateOrder, ListOrder, DeleteOrder, UpdateOrder

urlpatterns = [
    path("order/create/", CreateOrder.as_view(), name="create-order"),
    path("order/", ListOrder.as_view(), name="list-order"),
    path("order/<str:id>/", UpdateOrder.as_view(), name="update-order"),
    path("order/delete/<str:id>", DeleteOrder.as_view(), name="delete-order"),
]
