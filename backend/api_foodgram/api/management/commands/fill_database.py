import json
import random
import sys

from django.core.management import BaseCommand

from recipes.models import Recipe
from tests.factories import (IngredientFactory, RandomIngredentFactory,
                             RecipeFactory, RecipeIngredientFactory,
                             TagFactory, UserProfileFactory)


class Command(BaseCommand):
    help = 'Fill database with test data'

    DB_SIZE = 10
    MAX_AMOUNT = 32000

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to file with data')

    def handle(self, *args, **options):
        file_path = options['file_path']

        with open(file_path, 'r') as f:
            ingredients = json.load(f)
            for ingredient in ingredients:
                IngredientFactory(
                    name=ingredient['name'],
                    measurement_unit=ingredient['measurement_unit']
                )
        profiles = UserProfileFactory.create_batch(self.DB_SIZE)
        users = [profile.user for profile in profiles]
        for u in users:
            RecipeFactory.create_batch(
                random.randint(1, self.DB_SIZE),
                author=u
            )
        tags = TagFactory.create_batch(self.DB_SIZE)
        recipes = Recipe.objects.all()
        for recipe in recipes:
            ingredients = RandomIngredentFactory.create_batch(
                random.randint(1, self.DB_SIZE))
            for ingredient in ingredients:
                RecipeIngredientFactory(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=random.randint(1, self.MAX_AMOUNT)
                )
            recipe.tags.set(random.sample(tags, random.randint(1, 3)))
        sys.stdout.write(self.style.SUCCESS('Successfully filled database'))
