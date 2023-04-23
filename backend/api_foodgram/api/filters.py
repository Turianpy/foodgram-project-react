from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Ingredient
from users.models import User


class IngredientFilterSet(FilterSet):
    name = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilterSet(FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    is_favorited = filters.BooleanFilter(
        method='favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(favorited_by=user.profile)
        return queryset

    def in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(added_to_cart_by=user.profile)
        return queryset
