import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Chat, User
from .utilitys import ( get_all_user, get_all_chat, 
                        add_message, new_chat)


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
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

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        user_id = text_data_json['user_id']
        user = User.objects.get(pk=user_id)

        messages = []

        if command == 'message':
            chat_id = text_data_json['chat_id']
            message = text_data_json['message']
            print(text_data_json)
            add_message(chat_id, user_id, message)

        idChat = -1
        if command == 'newChat':
            friend_id = text_data_json['friend_id']
            idChat = new_chat(user_id, friend_id)

        messages = {
            'idNewChat': idChat,
            'users': get_all_user(),
            'rooms': get_all_chat(text_data_json['user_id']),
        }
            

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': messages
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        messages = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': messages
        }))

