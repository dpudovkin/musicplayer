from django.db import models

# Create your models here.


class Song(models.Model):
    title = models.CharField(max_length=90, null=False, verbose_name='Наименование трека')
    artist = models.CharField(max_length=90, null=False, verbose_name='Исполнитель')
    image = models.ImageField(verbose_name='Обложка трека')
    audio_file = models.FileField(blank=True, null=True)
    text = models.TextField(max_length=50000, null=True, verbose_name='Текст песни')
    textHTML = models.TextField(max_length=10000, null=True, verbose_name='Текст песни с HTML тэгами')
    paginate_by = 2

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Song, self).save()

    class Meta:
        ordering = ('title',)


