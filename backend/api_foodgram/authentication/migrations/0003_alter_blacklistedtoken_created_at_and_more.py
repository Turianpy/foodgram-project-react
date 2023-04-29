# Generated by Django 4.2 on 2023-04-29 02:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacklistedtoken',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='blacklistedtoken',
            name='token',
            field=models.CharField(max_length=255, verbose_name='Токен авторизации'),
        ),
        migrations.AlterField(
            model_name='blacklistedtoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blacklisted_tokens', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]