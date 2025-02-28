from rest_framework import viewsets, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recommendation_system.models import Film, Rating, UserFilm, Genre, UserGenre
from recommendation_system.serializers import FilmSerializer, RatingSerializer, GenreSerializer, UserFilmSerializer, \
    UserGenreSerializer
from recommendation_system.services import build_preference_graph, calculate_pagerank, collaborative_filtering, \
    k_nearest_neighbors


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

        UserGenre.objects.create(
            user=request.user,
            genre=instance,
        )

        return Response(self.get_serializer(instance).data)


class PreferenceCreateAPIView(CreateAPIView):
    """Класс представления для добавления предпочтений пользователю"""
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя перед сохранением
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        data = request.data

        # Проверяем тип данных и создаем соответствующий объект
        if 'rating' in data and 'film' in data:
            serializer = RatingSerializer(data=data)
        elif 'genre' in data:
            serializer = UserGenreSerializer(data=data)
        elif 'film' in data:
            serializer = UserFilmSerializer(data=data)
        else:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            self.perform_create(serializer)  # Вызываем perform_create
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        graph = build_preference_graph()

        # Получаем рекомендации для текущего пользователя
        pagerank_scores = calculate_pagerank(graph)
        similar_users = collaborative_filtering(graph, request.user.id)
        k_neighbors = k_nearest_neighbors(graph, request.user.id)

        return Response({
            'pagerank_scores': pagerank_scores,
            'similar_users': similar_users,
            'k_neighbors': k_neighbors
        })
