# chat/consumers.py
import json
import random
import syslog

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import time


class RoomConsumer(WebsocketConsumer):


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.scope["session"]["seed"] = random.randint(1, 1000)

        # Join room group

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.sync_time()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json['action'] == "SYNC":
            self.finish_sync(text_data_json)
            return

        if text_data_json['action'] == "START_SYNC":
            self.sync_time()
            return

        message = text_data_json['message']
        time = text_data_json['time']
        action = text_data_json['action']
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'room_message',
                'message': message,
                'seed': self.scope["session"]["seed"],
                #'delta': event['delta'],
                'delta': self.scope["session"]["delta"],
                'time': time,
                'action': action
            })

    # Receive message from room group
    def room_message(self, event):
        message = event['message']
        seed = event['seed']
        self.send(text_data=json.dumps({
            'message': message,
            'time': event['time'],
            #'delta': event['delta'],
            'delta': self.scope["session"]["delta"],
            'seed': seed,
            'action': event['action']
        }))


    def finish_sync(self, text_data):
        start_time = int(text_data['src_time'])
        js_time = int(text_data['js_time'])
        finish_time = int((time.time()*1000000)//1000)
        #print("Finish sync", start_time, js_time, finish_time)
        print("Delta js start", js_time-start_time, "delta finish js", finish_time-js_time)
        print("Delta finish start", finish_time-start_time)
        # if "delta" in self.scope["session"]:
        #     self.scope["session"]["delta"] = self.scope["session"]["delta"]//2+((js_time-start_time)+(finish_time-js_time))//4
        # else:
        #     self.scope["session"]["delta"] = ((js_time-start_time)+(finish_time-js_time))//2

        if "delta" in self.scope["session"]:
            self.scope["session"]["delta"] = (self.scope["session"]["delta"] + (finish_time-start_time))//2
        else:
            self.scope["session"]["delta"] = (finish_time-start_time)

        print(self.scope["session"]["delta"])

    def sync_time(self):
        self.send(text_data=json.dumps({
                'action': "SYNC",
                'src_time': str(int((time.time()*1000000)//1000))
    }))





