import random

import factory
from faker import Faker
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import User, UserProfile

fake = Faker('ru_RU')

UNIT_CHOICES = [
    'г', 'кг', 'мл', 'л', 'ст. л.', 'ч. л.', 'стакан', 'шт'
]


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: fake.user_name())
    email = factory.LazyAttribute(lambda _: fake.email())
    password = factory.LazyAttribute(lambda _: fake.password())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.LazyAttribute(lambda _: fake.word())
    color = factory.LazyAttribute(lambda _: fake.color())
    slug = factory.LazyAttribute(lambda _: Faker().slug())


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    name = factory.LazyAttribute(lambda _: fake.word())
    measurement_unit = factory.LazyAttribute(
        lambda _: fake.random_element(elements=UNIT_CHOICES)
    )


class RandomIngredentFactory(factory.django.DjangoModelFactory):
    """
    Takes a random ingredient from the database.
    """
    class Meta:
        model = Ingredient

    @classmethod
    def create_batch(cls, size, **kwargs):
        ingredients = list(Ingredient.objects.all())
        return random.sample(ingredients, size)


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    author = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(lambda _: fake.word())
    image = factory.django.ImageField(color='blue')
    text = factory.LazyAttribute(lambda _: fake.text())
    cooking_time = factory.LazyAttribute(
        lambda _: fake.random_int(min=1, max=100)
    )


class RecipeIngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeIngredient

    recipe = factory.SubFactory(RecipeFactory)
    ingredient = factory.SubFactory(IngredientFactory)
    amount = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=100))
