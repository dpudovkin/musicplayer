# Create your views here.
# imported our models
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Song


def room(request, room_name):
    paginator = Paginator(Song.objects.all(), 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, 'room_name': room_name}
    return render(request, 'room.html', context)
