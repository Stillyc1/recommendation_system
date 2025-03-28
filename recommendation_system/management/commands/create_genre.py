from django.core.management import BaseCommand

from recommendation_system.models import Genre

genres = [
    "аниме", "биография", "боевик", "детектив", "комедия", "ужасы", "фантастика", "приключения", "мультфильм"
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for genre in genres:
            Genre.objects.create(name=f"{genre}")

        self.stdout.write(self.style.SUCCESS(f"Добавлено {len(genre)} жанров в базу данных!"))
