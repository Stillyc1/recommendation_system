from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recommendation_system.models import Film, UserFilm, Genre, UserGenre, Rating, RecommendationStatistics
from recommendation_system.serializers import FilmSerializer, RatingSerializer, UserFilmSerializer, \
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


class FilmDetailView(LoginRequiredMixin, DetailView):
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


@method_decorator(cache_page(60 * 5), name='dispatch')
class RecommendationView(LoginRequiredMixin, ListView):
    model = Film
    template_name = "recommendation_system/recommendation_film.html"
    context_object_name = "film"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        recommendation_system = RecommendationSystem

        graph = recommendation_system.build_preference_graph()
        get_recommendations = recommendation_system.get_recommendations(graph, self.request.user.id)
        _, sorted_pagerank = recommendation_system.calculate_pagerank(graph)

        RecommendationStatistics.objects.create(
            user=self.request.user,
            film_count=len(get_recommendations["films"]),
            genre_count=len(get_recommendations["genres"])
        )

        context["top_5_films"] = Film.objects.filter(title__in=sorted_pagerank["top_5_films"][:4])
        context["top_5_genres"] = Genre.objects.filter(name__in=sorted_pagerank["top_5_genres"])
        context["genres"] = Genre.objects.filter(name__in=get_recommendations["genres"])
        context["films"] = Film.objects.filter(title__in=get_recommendations["films"])

        return context


class PreferenceView(LoginRequiredMixin, ListView):
    model = Rating
    template_name = "recommendation_system/preference_user.html"
    context_object_name = "ratings"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user_genres"] = UserGenre.objects.filter(user=self.request.user)
        context["user_films"] = UserFilm.objects.filter(user=self.request.user)
        context["ratings"] = Rating.objects.filter(user=self.request.user)

        return context


class StatisticRecommendationView(LoginRequiredMixin, ListView):
    """Представление статистики рекомендаций для пользователя."""
    model = RecommendationStatistics
    template_name = "recommendation_system/statistics.html"
    context_object_name = "statistics"

    def get_queryset(self):
        return RecommendationStatistics.objects.filter(user=self.request.user)


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

        RecommendationStatistics.objects.create(
            user=request.user,
            film_count=len(get_recommendations["films"]),
            genre_count=len(get_recommendations["genres"])
        )

        return Response({"top": sorted_pagerank, "recommendations": get_recommendations})


class RecommendationStatisticsAPIView(APIView):
    """API для получения статистики на основе графов и рекомендаций."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        system = RecommendationSystem
        graph = system.build_preference_graph()

        # Получаем статистику рекомендации для текущего пользователя
        pagerank_scores, _ = system.calculate_pagerank(graph)
        similar_users = system.collaborative_filtering(graph, request.user.id)
        k_neighbors = system.k_nearest_neighbors(graph, request.user.id)

        return Response({
            'pagerank_scores': pagerank_scores,
            'similar_users': similar_users,
            'k_neighbors': k_neighbors
        })
