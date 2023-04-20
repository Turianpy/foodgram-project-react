from django.urls import include, path
from rest_framework import routers
from recipes import views
from users.views import UserViewSet
from recipes.views import (IngredientViewSet, RecipeViewSet, TagViewSet)

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('recipes', RecipeViewSet, basename='recipes')
v1_router.register('ingredients', IngredientViewSet, basename='ingredients')
v1_router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include('authentication.urls', namespace='auth')),
]