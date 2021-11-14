from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser


def get_anonymus_user(self):
    return User.objects.get_or_create(username='Anonymus',
                                      email='mail@mail.ru',
                                      password='password')[0]


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=False, default='user.png')
    bio = models.CharField(max_length=300, null=True, blank=True, default='no info')
