from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """Класс сериализатор создания пользователя."""

    class Meta:
        model = User
        fields = ("username", "password",)


class UserRetrieveSerializer(ModelSerializer):
    """Класс сериализатор просмотра пользователя."""

    class Meta:
        model = User
        fields = ("username", "name", "country", "city",)
