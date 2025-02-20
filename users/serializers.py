from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """Класс сериализатор пользователя."""

    class Meta:
        model = User
        fields = ("username",)
