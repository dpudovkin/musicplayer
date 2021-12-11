
from django.urls import path

from . import views

app_name = "room"

urlpatterns = [
    path("", views.index, name="index"),
    path("to/room/", views.to_room, name='to_room'),
    path('<str:room_name>/', views.room, name='room'),
    path("add/song/", views.add_song, name='add_song'),
    path("add/song/success", views.add_song_success, name='add_song_success'),
    path("liked/song/", views.liked_song, name='liked_song')
]
