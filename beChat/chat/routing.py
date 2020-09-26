from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path('ws/chat/user=(?P<user_id>\w+)/$', ChatConsumer),
]



"""

command: open => user_id, chat_id=1 or null
command: create chat => user_id, friend_id
commad: 

"""