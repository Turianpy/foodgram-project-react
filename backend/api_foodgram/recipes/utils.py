def calculate_shopping_cart(user):
    recipes = user.profile.shopping_cart.all()
    ingredients = {}
    for recipe in recipes:
        for ingredient in recipe.ingredients.all():
            if ingredient.name in ingredients:
                ingredients[ingredient.name]['amount'] += ingredient.amount
            else:
                ingredients[ingredient.name] = {
                    'measurement_unit': ingredient.measurement_unit,
                    'amount': ingredient.amount,
                }

    return ingredients