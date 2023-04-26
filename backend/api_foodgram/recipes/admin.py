from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('times_favorited',)
    list_display = (
        'name', 'author',
        'created', 'get_tags',
        'times_favorited', 'cooking_time'
    )
    list_filter = ('author', 'created', 'tags')
    model = Recipe
    inlines = (RecipeIngredientInline,)

    def times_favorited(self, obj):
        return obj.favorited_by.all().count()

    def get_tags(self, obj):
        return ', '.join([str(tag) for tag in obj.tags.all()])

    times_favorited.short_description = 'Количество добавлений в избранное'


admin.site.register(Recipe, admin_class=RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(RecipeIngredient)
