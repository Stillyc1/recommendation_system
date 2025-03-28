from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class UserIsNotAuthenticated(UserPassesTestMixin):
    """Миксин для запрета повторной регистрации пользователя"""
    def test_func(self):
        if self.request.user.is_authenticated:
            messages.info(self.request, 'Вы уже авторизованы. Вы не можете посетить эту страницу.')
            raise PermissionDenied
        return True

    def handle_no_permission(self):
        return redirect('recommendation_system:home')


class FormClean:
    def clean(self):
        """Валидация данных сообщения (не должны иметь запрещенные слова)"""
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        name = cleaned_data.get("name")
        country = cleaned_data.get("name")
        city = cleaned_data.get("name")

        banned_words = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]

        for word in banned_words:
            if username and word in username.lower():
                self.add_error(
                    "username",
                    f'Нельзя использовать слово "{word.title()}" в поле username.',
                )
            if name and word in name.lower():
                self.add_error(
                    "name",
                    f'Нельзя использовать слово "{word.title()}" в name.',
                )
            if country and word in country.lower():
                self.add_error(
                    "country",
                    f'Нельзя использовать слово "{word.title()}" в country.',
                )
            if city and word in city.lower():
                self.add_error(
                    "city",
                    f'Нельзя использовать слово "{word.title()}" в city.',
                )
