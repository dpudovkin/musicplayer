from django.contrib.auth.models import User
from django.db import models


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=3000)
    message_html = models.TextField(max_length=3000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message


class Message(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    text = models.CharField(max_length=255)
