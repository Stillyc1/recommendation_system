from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Film, Genre, UserGenre, Rating, RecommendationStatistics, UserFilm


class RecommendationSystemTestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Создаем тестовые данные
        self.genre = Genre.objects.create(name='Action')
        self.film = Film.objects.create(title='Test Film', description='Test Description',
                                        release_date="2024-05-20", genre=self.genre, director="test_director",
                                        rating=8)
        self.rating = Rating.objects.create(user=self.user, film=self.film, rating=5)
        # Создаем статистику рекомендаций для пользователя
        self.statistic = RecommendationStatistics.objects.create(user=self.user, film_count=5, genre_count=2)

    def test_home_page_get(self):
        """Тестируем GET запрос на главную страницу."""
        response = self.client.get(reverse('recommendation_system:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recommendation_system/home.html')
        self.assertIn('genres', response.context)
        self.assertIn('films', response.context)

    def test_add_genre_post(self):
        """Тестируем POST запрос для добавления жанра."""
        response = self.client.post(reverse('recommendation_system:home'), {'genre': self.genre.id})
        self.assertEqual(response.status_code, 302)  # Проверяем, что происходит перенаправление
        self.assertTrue(UserGenre.objects.filter(user=self.user, genre=self.genre).exists())
        self.assertEqual(self.client.session['success_message'], 'Жанр успешно добавлен!')

    def test_add_rating_post(self):
        """Тестируем POST запрос для добавления оценки к фильму."""
        response = self.client.post(reverse('recommendation_system:home'), {'film': self.film.id, 'rating': 5})
        self.assertEqual(response.status_code, 302)  # Проверяем, что происходит перенаправление
        self.assertTrue(Rating.objects.filter(user=self.user, film=self.film, rating=5).exists())
        self.assertEqual(self.client.session['success_message'], 'Оценка успешно добавлена!')

    def test_add_genre_already_exists(self):
        """Тестируем попытку добавить жанр, который уже существует для пользователя."""
        UserGenre.objects.create(user=self.user, genre=self.genre)
        response = self.client.post(reverse('recommendation_system:home'), {'genre': self.genre.id})
        self.assertEqual(response.status_code, 302)  # Проверяем, что происходит перенаправление
        self.assertEqual(UserGenre.objects.filter(user=self.user, genre=self.genre).count(),
                         1)  # Количество не должно измениться

    def test_film_detail_view(self):
        """Тестируем доступ к детали фильма."""
        response = self.client.get(reverse('recommendation_system:film_detail', args=[self.film.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recommendation_system/film.html')
        self.assertEqual(response.context['film'], self.film)
        self.assertTrue(UserFilm.objects.filter(user=self.user, film=self.film).exists())

    def test_recommendation_view(self):
        """Тестируем представление рекомендаций."""
        response = self.client.get(reverse('recommendation_system:recommendation_film'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recommendation_system/recommendation_film.html')
        self.assertIn('top_5_films', response.context)
        self.assertIn('top_5_genres', response.context)
        self.assertIn('genres', response.context)
        self.assertIn('films', response.context)

    def test_preference_view(self):
        """Тестируем представление предпочтений пользователя."""
        response = self.client.get(reverse('recommendation_system:preference'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recommendation_system/preference_user.html')
        self.assertIn('user_genres', response.context)
        self.assertIn('user_films', response.context)
        self.assertIn('ratings', response.context)
        self.assertEqual(response.context['ratings'].count(), 1)

    def test_statistic_view(self):
        """Тестируем представление статистики рекомендаций."""
        response = self.client.get(reverse('recommendation_system:statistics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recommendation_system/statistics.html')
        self.assertIn('statistics', response.context)
        self.assertEqual(response.context['statistics'].count(), 1)


class FilmRetrieveAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)

        self.genre = Genre.objects.create(name='Action')
        self.film = Film.objects.create(title='Test Film', description='Test Description',
                                        release_date="2024-05-20", genre=self.genre, director="test_director",
                                        rating=8)

    def test_film_retrieve(self):
        """Тестируем успешное получение фильма."""
        response = self.client.get(reverse('recommendation_system:film', args=[self.film.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.film.title)
        self.assertTrue(UserFilm.objects.filter(user=self.user, film=self.film).exists())


class PreferenceCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        self.genre = Genre.objects.create(name='Action')
        self.film = Film.objects.create(title='Test Film', description='Test Description',
                                        release_date="2024-05-20", genre=self.genre, director="test_director",
                                        rating=8)

    def test_create_rating(self):
        """Тестируем создание оценки для фильма."""
        data = {'rating': 5, 'film': self.film.id}
        response = self.client.post(reverse('recommendation_system:add-preference'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Rating.objects.filter(user=self.user, film=self.film, rating=5).exists())

    def test_create_user_genre(self):
        """Тестируем создание жанра для пользователя."""
        data = {'genre': self.genre.id}
        response = self.client.post(reverse('recommendation_system:add-preference'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserGenre.objects.filter(user=self.user, genre=self.genre).exists())

    def test_create_invalid_preference(self):
        """Тестируем попытку создания предпочтения с невалидными данными."""
        data = {'invalid_field': 'value'}
        response = self.client.post(reverse('recommendation_system:add-preference'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


class RecommendationAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        self.genre = Genre.objects.create(name='Action')
        self.film = Film.objects.create(title='Test Film', description='Test Description',
                                        release_date="2024-05-20", genre=self.genre, director="test_director",
                                        rating=8)

    def test_get_recommendations(self):
        """Тестируем получение рекомендаций."""
        response = self.client.get(reverse('recommendation_system:recommendation'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('top', response.data)
        self.assertIn('recommendations', response.data)


class RecommendationStatisticsAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_get_recommendation_statistics(self):
        """Тестируем получение статистики рекомендаций."""
        response = self.client.get(reverse('recommendation_system:recommendation_statistics'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('pagerank_scores', response.data)
        self.assertIn('similar_users', response.data)
        self.assertIn('k_neighbors', response.data)
