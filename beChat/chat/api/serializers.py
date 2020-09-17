from rest_framework import serializers
from chat.models import Chat, Contact

class ChatSerializer(serializers.ModelSerializer):
    