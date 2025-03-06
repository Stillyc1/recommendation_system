import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from dotenv import load_dotenv

load_dotenv(override=True)


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            username='admin'
        )

        user.set_password(os.getenv("PASSWORD_CSU"))

        user.is_staff = True
        user.is_superuser = True

        user.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully created admin user with email {user.username}!"))
