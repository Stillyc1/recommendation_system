from django.contrib import admin

from .models import Film, RecommendationStatistics, UserGenre, Rating, UserFilm, Genre


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


@admin.register(RecommendationStatistics)
class RecommendationStatisticsAdmin(admin.ModelAdmin):
    """Отображает модели получателей рассылки в админке"""

    list_display = (
        "id",
        "user",
        "film_count",
        "genre_count",
        'timestamp',
    )
    list_filter = (
        "user",
        "timestamp",
    )
    search_fields = ("id", "user", "film_count", "timestamp",)


@admin.register(UserGenre)
class UserGenreAdmin(admin.ModelAdmin):
    """Отображает модели получателей рассылки в админке"""

    list_display = (
        "id",
        "user",
        "genre",
    )
    list_filter = (
        "user",
        "genre",
    )
    search_fields = ("id", "user", "genre",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Отображает модели получателей рассылки в админке"""

    list_display = (
        "id",
        "user",
        "film",
        "rating",
    )
    list_filter = (
        "user",
        "film",
        "rating"
    )
    search_fields = ("id", "user", "film", "rating",)


@admin.register(UserFilm)
class UserFilmAdmin(admin.ModelAdmin):
    """Отображает модели получателей рассылки в админке"""

    list_display = (
        "id",
        "user",
        "film",
        "created_at",
    )
    list_filter = (
        "user",
        "film",
        "created_at"
    )
    search_fields = ("id", "user", "film", "created_at",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Отображает модели получателей рассылки в админке"""

    list_display = (
        "id",
        "name",
    )
    list_filter = (
        "name",
    )
    search_fields = ("id", "name",)
