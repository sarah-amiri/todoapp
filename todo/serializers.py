from rest_framework.serializers import ModelSerializer

from .models import Todo


class TodoSerializer(ModelSerializer):

    class Meta:
        model = Todo
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def to_internal_value(self, data):
        # add user to data
        # data from input is immutable, so we cannot change it directly
        new_data = data.copy()
        new_data.update({'user': self.context['request'].user.id})

        return super().to_internal_value(new_data)
