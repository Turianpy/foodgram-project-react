# Generated by Django 4.2 on 2023-04-20 20:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blacklistedtoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blacklisted_tokens', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='blacklistedtoken',
            unique_together={('token', 'user')},
        ),
    ]
