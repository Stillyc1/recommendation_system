from django.db import models

from users.models import User


class Genre(models.Model):
    """Модель жанр фильма. Используется для получения предпочтений пользователя"""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Film(models.Model):
    """Модель фильма"""
    title = models.CharField(max_length=255, unique=True, verbose_name="Название фильма")
    description = models.TextField(blank=True, verbose_name="Описание", default="Не указано")
    release_date = models.DateField(verbose_name="Дата выхода")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='films')
    director = models.CharField(max_length=100, verbose_name="Режиссер")
    rating = models.FloatField(null=True, blank=True, verbose_name="Рейтинг фильма (от 1 до 10)")
    image = models.ImageField(upload_to="recommendation_system/photo/", verbose_name="Изображение",
                              blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class UserFilm(models.Model):
    """Модель связи: фильма и пользователя (предпочтение)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences', verbose_name="Пользователь")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='preferences', verbose_name="Фильм")
    created_at = models.DateTimeField(auto_now_add=True)  # Время взаимодействия

    class Meta:
        verbose_name = "Просмотр фильма пользователем"
        verbose_name_plural = "Просмотры фильма пользователя"
        unique_together = ('user', 'film')  # Обеспечить уникальность предпочтения для каждого пользователя и фильма

    def __str__(self):
        return f"{self.user.username} - посмотрел - {self.film.title}"


class Rating(models.Model):
    """Модель оценки пользователем фильма."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='ratings')
    rating = models.FloatField(verbose_name="Оценка фильма")  # Оценка, например, от 1 до 10
    created_at = models.DateTimeField(auto_now_add=True)  # Время, когда была оставлена оценка

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        unique_together = ('user', 'film')  # Пользователь может оценить фильм только один раз

    def __str__(self):
        return f"{self.user.username} оценил {self.film.title} на {self.rating}"


class UserGenre(models.Model):
    """Модель связи пользователя и жанра фильмов"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='liked_by_users')

    class Meta:
        unique_together = ('user', 'genre')
        verbose_name = "Жанр пользователя"
        verbose_name_plural = "Жанры пользователя"

    def __str__(self):
        return f"{self.user.username} предпочитает {self.genre.name}"
