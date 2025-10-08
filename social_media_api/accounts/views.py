

# Create your views here.
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    # override to return token on register
    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        user = User.objects.get(pk=resp.data['id'])
        token, _ = Token.objects.get_or_create(user=user)
        data = resp.data
        data['token'] = token.key
        return Response(data, status=201)


# DRF's ObtainAuthToken returns token; we'll extend to return user info
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=resp.data['token'])
        user = token.user
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data})


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # returns the profile for the current authenticated user
    def get_object(self):
        return self.request.user
