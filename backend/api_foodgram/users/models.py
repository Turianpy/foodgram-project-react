from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    subscriptions = models.ManyToManyField('self', related_name='subscribers', symmetrical=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    favorites = models.ManyToManyField('recipes.Recipe', related_name='favorited_by', blank=True)
    shopping_cart = models.ManyToManyField('recipes.Recipe', related_name='added_to_cart_by', blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"
