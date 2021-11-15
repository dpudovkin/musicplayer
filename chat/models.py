from django.db import models

from user.models import User


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=3000, null=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания сообщения')
    room_name = models.CharField(max_length=100, null=False, default='no room',
                                 blank=False, verbose_name='Наменование команты чата')

    def __str__(self):
        return self.message
