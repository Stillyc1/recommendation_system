from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView

from recommendation_system.models import Film, Rating
from recommendation_system.serializers import FilmSerializer, RatingSerializer


class FilmListAPIView(RetrieveAPIView):
    """Класс представления фильма через RetrieveAPIView"""
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


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