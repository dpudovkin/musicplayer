# Create your views here.
# imported our models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from chat.models import ChatMessage
from chat.service import ChatMessageRepository
from .forms import SongForm
from .models import Song, Like


@login_required(login_url=('/accounts/login'))
def room(request, room_name):
    # load songs
    paginator = Paginator(Song.objects.all(), 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # load chat messages
    chat_queryset = ChatMessageRepository.get_instance().messages_by_room(room_name).order_by("-created")[:20]
    chat_message_count = len(chat_queryset)

    if chat_message_count > 0:
        first_message_id = chat_queryset[len(chat_queryset) - 1].id
    else:
        first_message_id = -1
    previous_id = -1
    if first_message_id != -1:
        try:
            previous_id = ChatMessage.objects.filter(pk__lt=first_message_id).order_by("-pk")[:1][0].id
        except IndexError:
            previous_id = -1
    chat_messages = reversed(chat_queryset)

    context = {"page_obj": page_obj,
               'room_name': room_name,
               'chat_messages': chat_messages,
               'first_message_id': previous_id
               }

    return render(request, 'room.html', context)


@login_required(login_url='/accounts/login')
def index(request):
    context = {}
    return render(request, 'index.html', context)


def to_room(request):
    return redirect(f"/rooms/{request.POST.get('room_name')}")


@login_required(login_url='/accounts/login')
def add_song(request):
    if request.method == "POST":
        song_form = SongForm(request.POST, request.FILES)
        if song_form.is_valid():
            song = song_form.save()
            song.uploader = request.user
            song.save()
            messages.success(request, 'Your song was successfully added!')
            return HttpResponseRedirect(
                reverse('room:add_song_success')
            )
        else:
            messages.error(request, 'Error saving form')
    songs = Song.objects.applied_recently_added(verified=True)
    return render(request=request, template_name="songs.html", context={'songs': songs, 'success': False})


@login_required(login_url='/accounts/login')
def add_song_success(request):
    songs = Song.objects.applied_recently_added(verified=True)
    return render(request=request, template_name="songs.html", context={'songs': songs, 'success': True})


@login_required(login_url='/accounts/login')
def liked_song(request):
    likes = Like.objects.liked_by_user(request.user.id)
    songs = []
    for like in likes:
        songs.append(like.song)
    return render(request=request, template_name='liked_songs.html', context={'liked_songs': songs})
