import io
from wsgiref.util import FileWrapper

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, Recipe, Tag
from recipes.utils import calculate_shopping_cart
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from users.models import User

from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, SetPasswordSerializer,
                          ShortRecipeSerializer, TagSerializer,
                          UserCreateSerializer, UserSerializer,
                          UserSerializerWithRecipes)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return RecipeCreateSerializer
        return RecipeSerializer

    def update(self, request, *args, **kwargs):
        recipe = self.get_object()
        if request.user != recipe.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = ShortRecipeSerializer(recipe)
        user = request.user
        if request.method == 'POST':
            user.profile.favorites.add(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user.profile.favorites.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = ShortRecipeSerializer(recipe)
        user = request.user
        if request.method == 'POST':
            user.profile.shopping_cart.add(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user.profile.shopping_cart.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        """
        Download shopping cart as a text file.
        """
        cart = calculate_shopping_cart(request.user)
        if not cart:
            return Response(status=status.HTTP_204_NO_CONTENT)

        buffer = io.BytesIO()
        for ingredient, amount_data in cart.items():
            buffer.write((
                f'{ingredient} - {amount_data["amount"]}'
                f'{amount_data["measurement_unit"]} \n'.encode()))
        buffer.seek(0)

        file_name = 'shopping_cart.txt'

        response = HttpResponse(FileWrapper(buffer), content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        buffer.close()

        return response


class IngredientViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


class TagViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post', 'get', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            validate_password(serializer.validated_data['password'])
        except ValidationError as e:
            return Response(
                {'password': e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        if self.action != 'subscribe':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.IsAuthenticated],
        url_path='me')
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated],
        url_path='set_password'
    )
    def set_password(self, request):
        data = request.data
        data['user'] = request.user
        serializer = SetPasswordSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, pk):
        user = get_object_or_404(User, id=pk)
        serializer = UserSerializer(user)
        if request.method == 'POST':
            request.user.profile.subscriptions.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            request.user.profile.subscriptions.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscriptions(self, request):
        queryset = request.user.profile.subscriptions.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializerWithRecipes(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializerWithRecipes(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
