from rest_framework.serializers import ModelSerializer

from .models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ['last_login', 'is_superuser', 'is_active', 'groups', 'user_permissions']
        extra_kwargs = {
            'password': {'write_only': True}
        }
