
from django.urls import path

from . import views

app_name = "room"

urlpatterns = [
    path("", views.index, name="index"),
    path("to/room/", views.to_room, name='to_room'),
    path('<str:room_name>/', views.room, name='room'),
    path("add/song/", views.add_song, name='add_song')
]
