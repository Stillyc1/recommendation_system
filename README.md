# recommendation_system

Система рекомендаций на основе графов. Система будет рекомендовать пользователям элементы (например, фильмы, книги, продукты и т.д.) на основе их предпочтений и поведения других пользователей с похожими интересами. Система должна использовать алгоритмы графов для нахождения связей и рекомендаций.

## Содержание

- [Установка](#установка)
- [Использование](#использование)
- [Тестирование](#тестирование)
- [Функциональность](#функциональность)
- [Технологии](#технологии)
- [Лицензия](#лицензия)

## Установка

1. Убедитесь, что у вас установлен [Poetry](https://python-poetry.org/docs/#installation). Если нет, вы можете установить его, следуя официальной документации.
2. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/stillyc1/recommendation_system.git
    ```
3. Перейдите в директорию проекта:
    ```bash
    cd recommendation_system
    ```
4. Установите зависимости:
    ```bash
    poetry install
    ```
   
## Использование

1. Чтобы запустить проект, используйте следующую команду:
    ```bash
    python manage.py runserver
    ```
   
    После запуска приложения вы сможете получить доступ к нему по адресу http://127.0.0.1:8000/.

## Тестирование

1. Для запуска тестов используйте следующую команду:
    ```bash
    python manage.py test
    ```
   
## Функциональность

### Пользовательский интерфейс
1. Регистрация пользователя
2. Вход и выход пользователя
3. Просмотр и редактирование профиля пользователя
4. Просмотр фильмов и жанров
5. Оценка фильмов
6. Рекомендации фильмов на основе предпочтений пользователя

### API
1. Регистрация пользователя через UserCreateAPIView
2. Получение информации о пользователе через UserRetrieveAPIView
3. Работа с профилем пользователя через ProfileUserDetailView и ProfileUserUpdateView
4. Аутентификация через LoginUserView и LogoutUserView
5. Создание рейтингов и жанров через соответствующие представления

## Технологии
- Python 3.12
- Django 5.1.6
- Django REST Framework
- PostgreSQL
- Другие библиотеки, указанные в pyproject.toml:
    flake8 = "^7.1.2"
    mypy = "^1.15.0"
    black = "^25.1.0"
    isort = "^6.0.0"
    python-dotenv = "^1.0.1"
    psycopg2 = "^2.9.10"
    requests = "^2.32.3"
    pillow = "^11.1.0"
    ipython = "^8.32.0"
    redis = "^5.2.1"
    djangorestframework-simplejwt = "^5.4.0"
    coverage = "^7.6.12"
    drf-yasg = "^1.21.8"
    django-cors-headers = "^4.7.0"
    schedule = "^1.2.2"
    gunicorn = "^23.0.0"
    networkx = "^3.4.2"
    numpy = "^2.2.3"
    scipy = "^1.15.2"
    pytest-cov = "^6.0.0"

## Лицензия
Лицензии нет.
