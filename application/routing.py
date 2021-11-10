# chat/routing.py
from django.urls import re_path

import room
from chat.consumers import ChatConsumer
from room.consumers import RoomConsumer

# routing for websockets
websocket_urlpatterns = [
    re_path(r'ws/app/(?P<room_name>\w+)/$', RoomConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]
