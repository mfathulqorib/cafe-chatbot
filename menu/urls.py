from django.urls import path
from .views import CreateMenu

urlpatterns = [
    path('menu/create/', CreateMenu.as_view(), name="create-menu"),
]