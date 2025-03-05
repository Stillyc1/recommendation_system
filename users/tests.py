from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class UserCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Тестируем создание нового пользователя."""
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_create_user_without_password(self):
        """Тестируем создание пользователя без пароля."""
        data = {
            'username': 'testuser',
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)


class UserRetrieveAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user(self):
        """Тестируем успешное получение информации о пользователе."""
        response = self.client.get(reverse('users:user', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_retrieve_user_unauthenticated(self):
        """Тестируем попытку получения информации о пользователе без аутентификации."""
        self.client.logout()
        response = self.client.get(reverse('users:user', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileUserDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_view_profile_user(self):
        """Тестируем успешный просмотр профиля пользователя."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users:profile_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_view_profile_user_unauthenticated(self):
        """Тестируем попытку просмотра профиля пользователя без аутентификации."""
        response = self.client.get(reverse('users:profile_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление на страницу входа


class ProfileUserUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_update_profile_user(self):
        """Тестируем успешное обновление профиля пользователя."""
        self.client.login(username='testuser', password='testpassword')
        data = {
            'username': 'newusername',
        }
        response = self.client.post(reverse('users:profile_edit', args=[self.user.id]), data)
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')

    def test_update_profile_user_unauthenticated(self):
        """Тестируем попытку обновления профиля пользователя без аутентификации."""
        data = {
            'username': 'newusername',
        }
        response = self.client.post(reverse('users:profile_edit', args=[self.user.id]), data)
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление на страницу входа


class LoginUserViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_user(self):
        """Тестируем успешный вход пользователя."""
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Ожидаем redirect на главную страницу
