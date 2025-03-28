from django.core.exceptions import PermissionDenied
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверка на владельца, чтобы только владелец мог смотреть атрибуты пользователя"""

    def has_object_permission(self, request, view, obj):
        """Метод проверки для Api"""
        if obj.id == request.user.id:
            return True
        return False

    @staticmethod
    def get_object_only_owner(self, user_id):
        """Метод проверки для веб-сервера, возврат объекта владельца."""
        if self.id == user_id:
            return self
        else:
            raise PermissionDenied
