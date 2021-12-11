from django.contrib.auth.models import User
from django.db import models
import datetime


# Create your models here.

class SongManager(models.Manager):

    def recently_added(self):
        return self.all().order_by('-created')[:10]

    def applied_recently_added(self, verified=True):
        return self.all().order_by('-created').filter(verified=verified)[:10]


class Song(models.Model):
    objects = SongManager()
    title = models.CharField(max_length=90, null=False, verbose_name='Наименование трека')
    artist = models.CharField(max_length=90, null=False, verbose_name='Исполнитель')
    image = models.ImageField(verbose_name='Обложка трека')
    audio_file = models.FileField(blank=True, null=True, verbose_name="Аудио файл")
    text = models.TextField(max_length=50000, null=True, verbose_name='Текст песни')
    textHTML = models.TextField(max_length=10000, null=True, verbose_name='Текст песни с HTML тэгами')
    created = models.TimeField(auto_now_add=True, verbose_name="Дата создания")
    verified = models.BooleanField(default=False, verbose_name="Верицирован")
    uploader = models.ForeignKey(to=User, verbose_name="Загружающее лицо", null=True, on_delete=models.SET_NULL)
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
    song = models.ForeignKey(to=Song, verbose_name="Аудиотрек", null=True, on_delete=models.SET_NULL)
