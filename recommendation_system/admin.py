from django.contrib import admin

from .models import Film

# создали админку python manage.py createsuperuser
# создали классы для отображения моделей в админке


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    """Отображает модели получателей рассылки в админке"""

    list_display = (
        "id",
        "title",
        "genre",
        "director",
        'rating',
    )
    list_filter = (
        "title",
        "genre",
    )
    search_fields = ("id", "title", "genre", "director",)
