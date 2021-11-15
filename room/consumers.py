# chat/consumers.py
import json
import random
import time

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer

from chat.models import ChatMessage
from room.models import Like
from room.service import RedisService, RepositoryService


class RoomConsumer(WebsocketConsumer):
    actionNewSong = 'new_song'
    actionUserConnect = 'user_connect'
    actionUserDisconnect = 'user_disconnect'
    actionVoteUpdate = 'vote_update'
    actionNewMessage = 'new_msg'
    actionLike = 'like'
    actionUnlike = 'unlike'

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'v2_%s' % self.room_name
        self.username = self.scope["user"].username

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        # connect user
        RedisService.get_instance().connect_user(self.room_group_name, self.username)

        # update song
        songId = RedisService.get_instance().current_song_id(self.room_group_name)
        if songId is None:
            # songId = RepositoryService.get_instance().next_song_id()
            self.room_start_new_song()
        else:
            self.audio_update(songId)

        # room connect user
        self.room_connect_user(self.username)
        self.room_vote_update()

    def disconnect(self, close_code):
        # Leave room group

        # send disconnect messages to room
        RedisService.get_instance().disconnect_user(self.room_group_name, self.username)

        self.room_disconnect_user(self.username)

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        message = text_data_json.get('message')
        action = text_data_json.get('action')

        if action == RoomConsumer.actionLike:
            song_id = RedisService.get_instance().current_song_id(self.room_group_name)
            toLike = Like.objects.like(user_id=self.scope["user"].id, song_id=song_id)
            if toLike:
                self.send(text_data=json.dumps({
                    'action': RoomConsumer.actionLike,
                }))
            else:
                self.send(text_data=json.dumps({
                    'action': RoomConsumer.actionUnlike,
                }))
            return

        if action == 'vote':
            if not RedisService.get_instance().is_voted(self.room_group_name, self.username):
                RedisService.get_instance().vote_next_song(self.room_group_name, self.username)

            if RedisService.get_instance().turn_next(self.room_group_name):
                self.room_start_new_song()

            self.room_vote_update()
            return

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'room_message',
                'message': message,
                'action': action
            })

    def audio_update(self, songId):
        song = RepositoryService.get_instance().song(songId)
        text = song.text
        self.like_sync(songId)
        if len(str(song.textHTML)) != 0:
            text = song.textHTML
        self.send(text_data=json.dumps({
            'message': '',
            'action': 'audio_update',
            'src': song.audio_file.url,
            'text': text,
            'img': song.image.url,
            'title': song.title,
            'artist': song.artist,
        }))

    def like_sync(self, songId):
        liked = Like.objects.is_liked(user_id=self.scope["user"].id, song_id=songId)
        if liked:
            self.send(text_data=json.dumps({
                'action': RoomConsumer.actionLike,
            }))
        else:
            self.send(text_data=json.dumps({
                'action': RoomConsumer.actionUnlike,
            }))

    # Receive message from room group
    def room_message(self, event):
        message = event.get('message')
        action = event.get('action')

        # new song action
        if action == RoomConsumer.actionNewSong:
            RedisService.get_instance().reset_vote(self.room_group_name, self.username)
            songId = RedisService.get_instance().current_song_id(self.room_group_name)

            self.audio_update(songId)
        elif action == RoomConsumer.actionUserConnect or action == RoomConsumer.actionUserDisconnect:
            username = event.get('username')

            self.send(text_data=json.dumps({
                'message': message,
                'action': action,
                'username': username,
                'users': RedisService.get_instance().all_users(self.room_group_name)
            }))
        elif action == RoomConsumer.actionVoteUpdate:
            self.send(text_data=json.dumps({
                'message': message,
                'action': action,
                'vote_count': RedisService.get_instance().vote_count(self.room_group_name)
            }))
        else:
            self.send(text_data=json.dumps({
                'message': message,
                'action': action
            }))

    def room_start_new_song(self):
        RedisService.get_instance().clear_voted(self.room_group_name)
        newSongId = RepositoryService.get_instance().next_song_id()
        RedisService.get_instance().update_current_src_id(self.room_group_name, newSongId)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'room_message',
                'message': '',
                'action': RoomConsumer.actionNewSong
            })

    def room_connect_user(self, username):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'room_message',
                'message': '',
                'action': RoomConsumer.actionUserConnect,
                'username': username
            })

    def room_disconnect_user(self, username):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'room_message',
                'message': '',
                'action': RoomConsumer.actionUserConnect,
                'username': username
            })

    def room_vote_update(self):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'room_message',
                'message': '',
                'action': RoomConsumer.actionVoteUpdate,
            })
