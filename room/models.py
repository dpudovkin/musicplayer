from django.contrib.auth.models import User
from django.db import models
import datetime


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


class LikeManager(models.Manager):

    def like(self, user_id, song_id):
        try:
            likeInstance = self.all().get(user_id=user_id, song_id=song_id)
        except Like.DoesNotExist:
            likeInstance = Like(user_id=user_id, song_id=song_id, created_at=datetime.datetime.now())
            likeInstance.save()
            return True
        else:
            likeInstance.delete()
            return False

    def is_liked(self, user_id, song_id):
        try:
            likeInstance = self.all().get(user_id=user_id, song_id=song_id)
        except Like.DoesNotExist:
            return False
        else:
            return True

    def liked_by_user(self, user_id):
        return self.all().filter(user_id=user_id)


class Like(models.Model):
    objects = LikeManager()
    user = models.ForeignKey(to=User, verbose_name="Пользователь", null="False", on_delete=models.SET_NULL)
    created_at = models.TimeField(verbose_name="Дата создания", null=True)
    song = models.ForeignKey(to=Song, verbose_name="Аудитрек", null=True, on_delete=models.SET_NULL)
