from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(RecipeIngredient)

# Рецепт без ингредиентов нельзя создать ни через админку, ни через сайт
# Надо добавить inlines = (RecipeIngredientInline, )
# В котором будет min_num = 1
