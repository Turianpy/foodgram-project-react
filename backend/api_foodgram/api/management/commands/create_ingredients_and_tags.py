import json
import sys

from django.core.management import BaseCommand
from tests.factories import IngredientFactory, TagFactory


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to file with data')

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(f'{file_path}/ingredients.json', 'r') as f:
            ingredients = json.load(f)
            for ingredient in ingredients:
                IngredientFactory(
                    name=ingredient['name'],
                    measurement_unit=ingredient['measurement_unit']
                )

        with open(f'{file_path}/tags.json', 'r') as f:
            tags = json.load(f)
            for tag in tags:
                TagFactory(
                    name=tag['name'],
                    color=tag['color'],
                    slug=tag['slug'])

        sys.stdout.write(self.style.SUCCESS('Successfully filled database'))
