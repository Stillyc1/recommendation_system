from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserRetrieveAPIView, RegisterView, LoginUserView, LogoutUserView, \
    ProfileUserDetailView, ProfileUserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('register_web/', RegisterView.as_view(), name='register_web'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileUserDetailView.as_view(), name='profile_user'),
    path('<int:pk>/profile_edit/', ProfileUserUpdateView.as_view(), name='profile_edit'),


    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user'),
    path('token/', TokenObtainPairView.as_view(permission_classes=[AllowAny]), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=[AllowAny]), name='token_refresh'),
]
