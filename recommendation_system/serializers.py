from rest_framework.serializers import ModelSerializer
from .models import Film, Genre, Rating, UserFilm, UserGenre


class GenreSerializer(ModelSerializer):
    """Сериализатор модели жанра."""
    class Meta:
        model = Genre
        fields = '__all__'


class FilmSerializer(ModelSerializer):
    """Сериализатор модели фильма."""
    genre = GenreSerializer()

    class Meta:
        model = Film
        fields = '__all__'


class UserFilmSerializer(ModelSerializer):
    """Сериализатор модели взаимодействия пользователя и фильма."""

    class Meta:
        model = UserFilm
        fields = '__all__'


class UserGenreSerializer(ModelSerializer):
    """Сериализатор модели взаимодействия пользователя и жанра."""

    class Meta:
        model = UserGenre
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    """Сериализатор модели рейтинга."""
    class Meta:
        model = Rating
        fields = '__all__'
