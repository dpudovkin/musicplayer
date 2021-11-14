from django import forms

from room.models import Song


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('title', 'artist', 'image', 'audio_file','text')