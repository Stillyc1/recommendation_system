from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from recommendation_system.models import Film, Rating, UserFilm, Genre
from recommendation_system.serializers import FilmSerializer, RatingSerializer, GenreSerializer


class FilmRetrieveAPIView(RetrieveAPIView):
    """Класс представления фильма через RetrieveAPIView"""
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if not UserFilm.objects.filter(user=user, film=instance):
            UserFilm.objects.create(
                user=user,
                film=instance
            )

        if request.accepted_renderer.format == 'html':  # проверка, какой формат данных нужен пользователю (html/json)
            return None
        else:
            return Response(self.get_serializer(instance).data)


class GenreRetrieveAPIView(RetrieveAPIView):
    """Класс представления жанра фильма через RetrieveAPIView"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        UserFilm.objects.create(
            user=request.user,
            film=instance,
        )

        return Response(self.get_serializer(instance).data)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class PreferenceViewSet(viewsets.ViewSet):
    def create(self, request):
        user = request.user  # Получение текущего пользователя
        film_id = request.data.get('film_id')
        interaction_type = request.data.get('interaction_type')

        # Создание предпочтения
        preference = Preference.objects.create(user=user, film_id=film_id, interaction_type=interaction_type)
        return response.Response({"message": "Preference created"}, status=status.HTTP_201_CREATED)


class RecommendationViewSet(viewsets.ViewSet):
    def list(self, request):
        user = request.user  # Получение текущего пользователя
        # Логика для генерации рекомендаций, здесь мы просто вернем случайные фильмы как пример
        recommended_films = Film.objects.all()[:5]  # Например, берем 5 случайных фильмов
        serializer = FilmSerializer(recommended_films, many=True)
        return response.Response(serializer.data)


class StatisticsViewSet(viewsets.ViewSet):
    def list(self, request):
        total_films = Film.objects.count()
        total_ratings = Rating.objects.count()
        total_preferences = Preference.objects.count()
        statistics = {
            "total_films": total_films,
            "total_ratings": total_ratings,
            "total_preferences": total_preferences,
        }
        return response.Response(statistics)