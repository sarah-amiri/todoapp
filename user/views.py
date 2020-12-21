from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        """
        Return the object that view is going to display.
        It is GenericAPIView function that override here.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # get object based on user id (identified by token)
        filter_kwargs = {self.lookup_field: self.request.user.id}

        obj = get_object_or_404(queryset, **filter_kwargs)

        # check permissions for user
        # here permission is IsAuthenticated but there may be other permissions
        self.check_object_permissions(self.request, obj)

        return obj
