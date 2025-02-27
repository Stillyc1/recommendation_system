from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверка на владельца, чтобы только владелец мог смотреть атрибуты пользователя"""

    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
        return False
