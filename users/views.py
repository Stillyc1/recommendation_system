from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.forms import CustomUserCreationForm, LoginUserForm, ProfileForm
from users.models import User
from users.permissions import IsOwner
from users.serializers import UserSerializer, UserRetrieveSerializer
from users.services import UserIsNotAuthenticated


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
    # IsOwner добавлен permissions.py для просмотра пользователя только самим пользователем
    permission_classes = [IsAuthenticated, IsOwner]


class ProfileUserDetailView(LoginRequiredMixin, DetailView):
    """Представление просмотра профиля пользователя на веб-сервере"""
    model = User
    template_name = 'users/profile_user.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        """Проверяем что пользователь может смотреть только свой профиль"""
        self.object = super().get_object(queryset)
        user_id = self.request.user.id
        return IsOwner.get_object_only_owner(self=self.object, user_id=user_id)


class ProfileUserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/register.html'
    form_class = ProfileForm

    context_object_name = "profile_edit"

    def get_success_url(self):
        return reverse("users:profile_user", args=[self.kwargs.get("pk")])

    def get_object(self, queryset=None):
        """Проверяем что пользователь может смотреть только свой профиль"""
        self.object = super().get_object(queryset)
        user_id = self.request.user.id
        return IsOwner.get_object_only_owner(self=self.object, user_id=user_id)


class LoginUserView(UserIsNotAuthenticated, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'


class LogoutUserView(LoginRequiredMixin, LogoutView):
    success_url = reverse_lazy('recommendation_system:home')
    next_page = 'recommendation_system:home'


class RegisterView(UserIsNotAuthenticated, CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('recommendation_system:home')
