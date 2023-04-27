from factories import (RecipeFactory, IngredientFactory, RecipeIngredientFactory, TagFactory, UserFactory, UserProfileFactory)
from pytest_factoryboy import register

register(RecipeFactory)
register(IngredientFactory)
register(RecipeIngredientFactory)
register(TagFactory)
register(UserFactory)
register(UserProfileFactory)
