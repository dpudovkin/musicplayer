from django.db import models

# Create your models here.


class Song(models.Model):
    title = models.CharField(max_length=90, null=False, verbose_name='Наименование трека')
    artist = models.TextField(max_length=90, null=False, verbose_name='Исполнитель')
    image = models.ImageField(verbose_name='Обложка трека')
    audio_file = models.FileField(blank=True, null=True)
    audio_link = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=20)
    paginate_by = 2

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Song, self).save()
        # TBD create audio and img directory for saving
        # name = self.audio_file.name
        # new_path = settings.MEDIA_ROOT + '/mp3/'+name
        # initial_path = self.audio_file.path
        # os.rename(initial_path, new_path)

    class Meta:
        ordering = ('title',)
