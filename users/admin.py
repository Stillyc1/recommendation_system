from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображает модели пользователей в админке"""

    list_display = (
        "id",
        "username",
    )
    list_filter = (
        "username",
    )
    search_fields = ("id", "username",)
