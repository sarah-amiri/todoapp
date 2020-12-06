from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from .serializers import UserSerializer

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
