import json
import random
import sys

from django.core.management import BaseCommand
from api.factories import (IngredientFactory, RandomIngredentFactory,
                           RecipeFactory, RecipeIngredientFactory, TagFactory,
                           UserFactory)
from recipes.models import Recipe


class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser) -> None:
        parser.add_argument('file_path', type=str, help='Path to file with data')

    def handle(self, *args, **options):
        file_path = options['file_path']

        with open(file_path, 'r') as f:
            ingredients = json.load(f)
            for ingredient in ingredients:
                IngredientFactory(
                    name=ingredient['name'],
                    measurement_unit=ingredient['measurement_unit']
                )

        users = UserFactory.create_batch(10)
        for u in users:
            RecipeFactory.create_batch(random.randint(1, 6), author=u)
        tags = TagFactory.create_batch(10)
        recipes = Recipe.objects.all()
        for recipe in recipes:
            ingredients = RandomIngredentFactory.create_batch(random.randint(1, 10))
            for ingredient in ingredients:
                RecipeIngredientFactory(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=random.randint(1, 100)
                )
            recipe.tags.set(random.sample(tags, random.randint(1, 3)))
        sys.stdout.write(self.style.SUCCESS('Successfully filled database'))
