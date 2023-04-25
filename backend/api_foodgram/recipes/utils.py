def calculate_shopping_cart(user):
    """
    Calculate shopping cart for a user.
    Duplicate ingredients are summed on amount.
    """
    recipes = user.profile.shopping_cart.all()
    ingredients = {}
    for recipe in recipes:
        recipe_ingredients = recipe.recipe_ingredients.all()
        for ri in recipe_ingredients:
            ingredient = ri.ingredient
            if ingredient.name in ingredients:
                ingredients[ingredient.name]['amount'] += ri.amount
            else:
                ingredients[ingredient.name] = {
                    'measurement_unit': ingredient.measurement_unit,
                    'amount': ri.amount
                }
    return ingredients
