# Generated by Django 5.1.6 on 2025-03-02 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_city_user_country_user_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=255, unique=True, verbose_name="Никнейм"),
        ),
    ]
