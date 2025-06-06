from django.contrib import admin
from django.urls import include, path

from .consumer import ChatConsumer, NotificationConsumer

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("orders.urls")),
    path("", include("menu.urls")),
    path("", include("chats.urls")),
    path("", include("my_auth.urls")),
]

websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
    path("ws/chats/", ChatConsumer.as_asgi()),
]
