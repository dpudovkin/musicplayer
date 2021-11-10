import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

from chat.models import ChatMessage


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'd2_%s' % self.room_name
        self.username = self.scope["user"].username

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # @database_sync_to_async
    def new_message(self, message):
        msg = ChatMessage(message=message, room_name=self.room_name)
        msg.user = self.scope['user']
        msg.save()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message_text = text_data_json.get('text')

        self.new_message(message=message_text)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_room',
                'message': message_text,
                'username': self.username,
            })

    def chat_room(self, event):
        message_text = event.get('message')
        username = event.get('username')

        self.send(text_data=json.dumps({
            'text': message_text,
            'username': username,
        }, ensure_ascii=False))
