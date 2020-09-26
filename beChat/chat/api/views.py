from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from chat.models import User

class RegisterView(GenericAPIView):

    serializer_class = RegisterSerializer
   
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(request.data)
        user = User.objects.get(email=request.data['email'])
        
        return Response({'user_id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=request.data['email'])
        
        if not user:
            return Response({'user_id':'null'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'user_id': user.id, 'username': user.username}, status=status.HTTP_200_OK)
