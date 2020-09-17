from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from chat.api.serializers import UserSerializer
from django.contrib.auth.models import User
from chat.models import Chat, Message


class ProfileAPI(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = IsAuthenticated

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListRoomChatAPI(GenericAPIView):
    
    def get(self, request, user_id):
        rooms_chat_data = []
        my_user = User.objects.get(pk=user_id)
        for chat in Chat.objects.all():
            if my_user in chat.participants:
                name = chat.id
                if chat.name:
                    name = chat.name
                number_associates = len(chat.participants.all())
                name_asociates = []
                for user in chat.participants.all():
                    name_asociates.append(user.username)
                
                messages = []
                for message in chat.messages.all():
                    messages.append({
                        'user': message.user.username,
                        'message': message.message
                    })
                
                rooms_chat_data.append({
                    'name': name,
                    'number_asociate': number_associates,
                    'name_asociates': name_asociates,
                    'messages': messages

                })

        return Response(rooms_chat_data, status=status.HTTP_200_OK)


