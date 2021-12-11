from django.contrib import admin

from chat.models import ChatMessage


@admin.register(ChatMessage)
class SongAdmin(admin.ModelAdmin):
    pass