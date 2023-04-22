def calculate_shopping_cart(user):
    recipes = user.profile.shopping_cart.all()
    ingredients = {}
    for recipe in recipes:
        recipe_ingredients = recipe.recipe_ingredients.all()
        for recipe_ingredient in recipe_ingredients:
            ingredient = recipe_ingredient.ingredient
            if ingredient.name in ingredients:
                ingredients[ingredient.name]['amount'] += recipe_ingredient.amount
            else:
                ingredients[ingredient.name] = {
                    'measurement_unit': ingredient.measurement_unit,
                    'amount': recipe_ingredient.amount
                }
    return ingredients
