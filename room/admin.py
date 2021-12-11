from django.contrib import admin

from .models import Song

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_filter = ("verified",)
