# Generated by Django 5.1.6 on 2025-03-02 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recommendation_system", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="film",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="recommendation_system/photo/",
                verbose_name="Изображение",
            ),
        ),
    ]
