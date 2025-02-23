from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, verbose_name='Имя пользователя')
    name = models.CharField(max_length=128, null=True, blank=True, default="Не указано",
                            verbose_name="Имя пользователя")
    country = models.CharField(max_length=128, null=True, blank=True, default="Не указано",
                               verbose_name="Страна")
    city = models.CharField(max_length=128, null=True, blank=True, default="Не указано",
                            verbose_name="Город")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
