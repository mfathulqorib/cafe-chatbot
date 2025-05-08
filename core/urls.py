from django.contrib import admin
from django.urls import path, include
from .consumer import NotificationConsumer, ChatConsumer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('transactions.urls')),
    path('', include('menu.urls')),
    path('', include('chats.urls')),
    path('', include('my_auth.urls')),
]

websocket_urlpatterns = [  
    path('ws/notifications/', NotificationConsumer.as_asgi()),  
    path('ws/chats/', ChatConsumer.as_asgi()),  
]
