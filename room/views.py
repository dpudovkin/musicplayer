# Create your views here.
# imported our models
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse

from chat.models import ChatMessage
from chat.service import ChatMessageRepository
from .models import Song


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
