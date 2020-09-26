from chat.models import Chat, Message
from django.shortcuts import get_object_or_404
from .models import User
from datetime import datetime


def add_message(chat_id, user_id, message):
    user = User.objects.get(pk=user_id)
    chat = Chat.objects.get(pk=chat_id)
    message = Message(user=user, message=message)
    message.save()
    chat.messages.add(message)
    chat.save()


def new_chat(user_id, friend_id):
    user = User.objects.get(pk=user_id)
    friend = User.objects.get(pk=friend_id)
    name = user.username + '&' + friend.username
    chat = Chat(name=name)
    chat.save()
    chat.participants.add(user)
    chat.participants.add(friend)
    chat.save()
    return chat.id


def get_all_user():
    users = []
    for user in User.objects.all():
        objects = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        users.append(objects)
    return users
    

def get_all_chat(user_id):

    user = User.objects.get(pk=user_id)
    rooms = []
    
    if Chat.objects.all():
        for chat in Chat.objects.all():
            if chat.participants.all():
                if user in chat.participants.all():
                    paticipants = [user.id for user in chat.participants.all()]
                    print(paticipants)

                    messages = []
                    for mess in chat.messages.all():
                        objects = {
                           'username': mess.user.username,
                           'id': mess.user.id,
                           'message': mess.message,
                           'time':str(mess.timestamp)
                        }
                        messages.append(objects)
                    if messages:
                        message = messages[len(messages)-1]
                    else:
                        message = {
                            'time': str(datetime.now())
                        }
                    names = chat.name.split('&')
                    objects = {
                        'id': chat.id,
                        'paticipants': paticipants,
                        'name': names[0] if user.username != names[0] else names[1],
                        'messages':messages,
                        'update_time': message['time']
                    }
                    rooms.append(objects)

    return rooms
