from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import UserSerializer, UserRetrieveSerializer


class UserCreateAPIView(CreateAPIView):
    """Реализация представления регистрации пользователя, через CreateAPIView."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Хэшируем пароль при создании пользователя."""
        user = serializer.save(is_active=True)
        user.set_password(serializer.validated_data['password'])
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    """Реализация представления просмотра пользователя, через RetrieveAPIView."""
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
