from django.urls import path
from .views import ProfileAPI, ListRoomChatAPI

urlpatterns = [
    path('profile/<int:pk>', ProfileAPI.as_view(), name='profile'),
    path('room/<int:user_id>', ListRoomChatAPI.as_view(), name = 'room')
]