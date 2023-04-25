from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=200,
        unique=True,
        verbose_name='Email'
    )
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    subscriptions = models.ManyToManyField(
        User,
        related_name='subscribers',
        symmetrical=False,
        verbose_name='Подписки',
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    favorites = models.ManyToManyField(
        'recipes.Recipe',
        related_name='favorited_by',
        blank=True,
        verbose_name='Избранное'
    )
    shopping_cart = models.ManyToManyField(
        'recipes.Recipe',
        related_name='added_to_cart_by',
        blank=True,
        verbose_name='Корзина'
    )

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"
