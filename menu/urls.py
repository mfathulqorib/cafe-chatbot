from django.urls import path

from .views import CreateMenu, DeleteMenu, ListMenu, UpdateMenu

urlpatterns = [
    path("menu/create/", CreateMenu.as_view(), name="create-menu"),
    path("menu/", ListMenu.as_view(), name="list-menu"),
    path("menu/<str:id>/", UpdateMenu.as_view(), name="update-menu"),
    path("menu/<str:id>/delete/", DeleteMenu.as_view(), name="delete-menu"),
]
