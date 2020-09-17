from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user.username}"


class Chat(models.Model):
    name = models.CharField(max_length=500, null=True)
    participants = models.ManyToManyField(User, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return f"Room {self.pk}."

