from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recommendation_system.models import Film, UserFilm, Genre, UserGenre, Rating
from recommendation_system.serializers import FilmSerializer, RatingSerializer, GenreSerializer, UserFilmSerializer, \
    UserGenreSerializer
from recommendation_system.services import RecommendationSystem


class HomePageView(View):
    """Класс представление главной страницы веб-приложения."""
    model = Film
    template_name = "recommendation_system/home.html"
    context_object_name = "films"

    def get(self, request):
        genres = Genre.objects.all()  # Получаем все жанры
        films = Film.objects.all()  # Получаем все фильмы
        # Получаем сообщение об успехе
        success_message = request.session.pop('success_message', None)
        return render(request, self.template_name, {
            'genres': genres,
            'films': films,
            'success_message': success_message,
        })

    def post(self, request):
        if 'genre' in request.POST:
            genre_id = request.POST.get('genre')
            user = request.user

            # Проверяем, существует ли уже этот жанр для пользователя
            if not UserGenre.objects.filter(user=user, genre_id=genre_id).exists():
                UserGenre.objects.create(user=user, genre_id=genre_id)  # Создаем объект UserGenre
                request.session['success_message'] = 'Жанр успешно добавлен!'  # Устанавливаем сообщение об успехе

        elif 'film' in request.POST:
            film_id = request.POST.get('film')
            rating_value = request.POST.get('rating')
            user = request.user

            # Создаем или обновляем оценку для фильма
            Rating.objects.update_or_create(
                user=user,
                film_id=film_id,
                defaults={'rating': rating_value}
            )
            request.session['success_message'] = 'Оценка успешно добавлена!'  # Устанавливаем сообщение об успехе

        return redirect('recommendation_system:home')  # Перенаправление на главную страницу


class FilmDetailView(DetailView):
    model = Film
    template_name = "recommendation_system/film.html"
    context_object_name = "film"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user

        if not UserFilm.objects.filter(user=user, film=self.object):
            UserFilm.objects.create(
                user=user,
                film=self.object
            )
        return self.object


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
        return Response(self.get_serializer(instance).data)


# class GenreRetrieveAPIView(RetrieveAPIView):
#     """Класс представления жанра фильма через RetrieveAPIView"""
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#
#         UserGenre.objects.create(
#             user=request.user,
#             genre=instance,
#         )
#
#         return Response(self.get_serializer(instance).data)


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
            return Response({
                "error": "Укажите предпочтения: 'rating', 'film' или 'genre' или 'film'."
                },
                status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            self.perform_create(serializer)  # Вызываем perform_create
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationAPIView(APIView):
    """API для получения рекомендаций на основе графов"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recommendation_system = RecommendationSystem

        graph = recommendation_system.build_preference_graph()
        get_recommendations = recommendation_system.get_recommendations(graph, request.user.id)
        _, sorted_pagerank = recommendation_system.calculate_pagerank(graph)

        return Response({"top": sorted_pagerank, "recommendations": get_recommendations})


class RecommendationStatisticsAPIView(APIView):
    """API для получения статистики на основе графов и рекомендаций."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        system = RecommendationSystem
        graph = system.build_preference_graph()

        # Получаем рекомендации для текущего пользователя
        pagerank_scores, _ = system.calculate_pagerank(graph)
        similar_users = system.collaborative_filtering(graph, request.user.id)
        k_neighbors = system.k_nearest_neighbors(graph, request.user.id)

        return Response({
            'pagerank_scores': pagerank_scores,
            'similar_users': similar_users,
            'k_neighbors': k_neighbors
        })
