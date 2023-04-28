import pytest
from fixtures.user_fixtures import *  # noqa
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import UserProfile


@pytest.mark.django_db(transaction=True)
class TestFactories:

    def test_recipe_create(self, recipe_factory):
        recipe = recipe_factory.create()
        assert isinstance(recipe, Recipe), (
            'Проверьте, что создается объект Recipe'
        )
        assert recipe == Recipe.objects.last(), (
            'Проверьте, что создается объект Recipe'
        )

    def test_ingredient_create(self, ingredient_factory):
        ingredient = ingredient_factory.create()
        assert isinstance(ingredient, Ingredient), (
            'Проверьте, что создается объект Ingredient'
        )
        assert ingredient == Ingredient.objects.last(), (
            'Проверьте, что создается объект Ingredient'
        )

    def test_recipe_ingredient_create(self, recipe_ingredient_factory):
        recipe_ingredient = recipe_ingredient_factory.create()
        assert isinstance(recipe_ingredient, RecipeIngredient), (
            'Проверьте, что создается объект RecipeIngredient'
        )
        assert recipe_ingredient == RecipeIngredient.objects.last(), (
            'Проверьте, что создается объект RecipeIngredient'
        )

    def test_tag_create(self, tag_factory):
        tag = tag_factory.create()
        assert isinstance(tag, Tag), (
            'Проверьте, что создается объект Tag'
        )
        assert tag == Tag.objects.last(), (
            'Проверьте, что создается объект Tag'
        )

    def test_profile_create(self, user_profile_factory):
        profile = user_profile_factory.create()
        assert isinstance(profile, UserProfile), (
            'Проверьте, что создается объект UserProfile'
        )
        assert profile == UserProfile.objects.last(), (
            'Проверьте, что создается объект User'
        )
