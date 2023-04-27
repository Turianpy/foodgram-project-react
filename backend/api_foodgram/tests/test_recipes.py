from fixtures.user_fixtures import *

import pytest
from http import HTTPStatus

from utils import assert_url_exists, check_pagination
from recipes.models import Recipe


@pytest.mark.django_db(transaction=True)
class TestRecipes:

    recipe_url = '/api/v1/recipes/'
    recipe_detail_url = '/api/v1/recipes/{id}/'
    recipe_favorite_url = '/api/v1/recipes/{id}/favorite/'
    recipe_shopping_cart_url = '/api/v1/recipes/{id}/shopping_cart/'
    recipe_download_shopping_cart_url = '/api/v1/recipes/download_shopping_cart/'
    favorited_recipes_query = '/api/v1/recipes/?is_favorited=1'
    shopping_cart_recipes_query = '/api/v1/recipes/?is_in_shopping_cart=1'

    def test_recipes_list(self, user_client, recipe_factory):
        recipe_factory.create_batch(10)
        response = user_client.get(self.recipe_url)
        assert_url_exists(response, self.recipe_url)
        check_pagination(self.recipe_url, response.json())
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что при GET запросе на {self.recipe_url} '
            'возвращается статус 200'
        )

    def test_recipes_detail(self, user_client, recipe_factory):
        recipe = recipe_factory.create()
        url = self.recipe_detail_url.format(id=recipe.id)
        response = user_client.get(url)
        assert_url_exists(response, url)
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что при GET запросе на {self.recipe_url}id/ '
            'возвращается статус 200'
        )
        assert response.json()['name'] == recipe.name, (
            f'Проверьте, что при GET запросе на {self.recipe_url}id/ '
            'возвращается информация о рецепте'
        )

    def test_recipe_post_and_patch(
            self, user_client,
            recipe_factory,
            ingredient_factory,
            tag_factory):
        ingredients = ingredient_factory.create_batch(3)
        tags = tag_factory.create_batch(3)
        recipe = recipe_factory.build()
        data = {
            'name': recipe.name,
            'tags': [tag.id for tag in tags],
            'ingredients': [{
                    'id': ingredient.id,
                    'amount': 100
                } for ingredient in ingredients],
            'cooking_time': recipe.cooking_time,
            'image': recipe.image,
            'text': recipe.text,
        }
        response = user_client.post(self.recipe_url, data=data)
        assert_url_exists(response, self.recipe_url)
        assert response.status_code == HTTPStatus.CREATED, (
            f'Проверьте, что при POST запросе на {self.recipe_url} '
            'возвращается статус 201'
        )
        assert response.json()['name'] == recipe.name, (
            f'Проверьте, что при POST запросе на {self.recipe_url} '
            'возвращается информация о рецепте'
        )
        assert Recipe.objects.get(name=recipe.name)(
            f'Проверьте, что при POST запросе на {self.recipe_url} '
            'рецепт сохраняется в базе данных'
        )
        url = self.recipe_detail_url.format(id=response.json()['id'])
        data['name'] = 'New name'
        response = user_client.patch(url, data=data)
        assert_url_exists(response, url)
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что при PATCH запросе на {self.recipe_url}id/ '
            'возвращается статус 200'
        )
        assert response.json()['name'] == 'New name', (
            f'Проверьте, что при PATCH запросе на {self.recipe_url}id/ '
            'возвращается информация о рецепте'
        )
        assert Recipe.objects.get(name='New name')(
            f'Проверьте, что при PATCH запросе на {self.recipe_url}id/ '
            'рецепт сохраняется в базе данных'
        )

    def test_recipe_delete(self, user_client, recipe_factory):
        recipe = recipe_factory.create(author=user_client.user)
        url = self.recipe_detail_url.format(id=recipe.id)
        response = user_client.delete(url)
        assert_url_exists(response, url)
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f'Проверьте, что при DELETE запросе на {self.recipe_url}id/ '
            'возвращается статус 204'
        )
        assert not Recipe.objects.filter(name=recipe.name).exists(), (
            f'Проверьте, что при DELETE запросе на {self.recipe_url}id/ '
            'рецепт удаляется из базы данных'
        )

    def test_recipe_favorite(self, user_client, recipe_factory):
        recipe = recipe_factory.create()
        url = self.recipe_favorite_url.format(id=recipe.id)
        response = user_client.post(url)
        assert_url_exists(response, url)
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что при POST запросе на {self.recipe_favorite_url}id/ '
            'возвращается статус 200'
        )
        assert response.json()['is_favorited'] is False, (
            f'Проверьте, что при POST запросе на {self.recipe_favorite_url}id/ '
            'возвращается информация о рецепте'
        )
        response = user_client.delete(url)
        assert_url_exists(response, url)
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f'Проверьте, что при DELETE запросе на {self.recipe_favorite_url}id/ '
            'возвращается статус 204'
        )
        response = user_client.get(self.recipe_detail_url.format(id=recipe.id))
        assert response.json()['is_favorited'] is False, (
            f'Проверьте, что после DELETE запроса на {self.recipe_favorite_url}id/ '
            'рецепт удаляется из избранного'
        )

    def test_recipe_shopping_cart(self, user_client, recipe_factory):
        recipe = recipe_factory.create()
        url = self.recipe_shopping_cart_url.format(id=recipe.id)
        response = user_client.post(url)
        assert_url_exists(response, url)
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что при POST запросе на {self.recipe_shopping_cart_url}id/ '
            'возвращается статус 200'
        )
        assert response.json()['is_in_shopping_cart'] is False, (
            f'Проверьте, что при POST запросе на {self.recipe_shopping_cart_url}id/ '
            'возвращается информация о рецепте'
        )
        response = user_client.delete(url)
        assert_url_exists(response, url)
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f'Проверьте, что при DELETE запросе на {self.recipe_shopping_cart_url}id/ '
            'возвращается статус 204'
        )
        response = user_client.get(self.recipe_detail_url.format(id=recipe.id))
        assert response.json()['is_in_shopping_cart'] is False, (
            f'Проверьте, что после DELETE запроса на {self.recipe_shopping_cart_url}id/ '
            'рецепт удаляется из корзины'
        )
    
    def test_download_shopping_cart(self, user_client, recipe_factory):
        recipe = recipe_factory.create()
        url = self.recipe_shopping_cart_url.format(id=recipe.id)
        user_client.post(url)
        dl_url = self.recipe_download_shopping_cart_url
        response = user_client.get(dl_url)
        assert_url_exists(response, self.download_shopping_cart_url)
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что при GET запросе на {dl_url} '
            'возвращается статус 200'
        )
        assert response['Content-Type'] == 'text/plain; charset=utf-8', (
            f'Проверьте, что при GET запросе на {dl_url} '
            'возвращается текстовый файл'
        )
        assert response['Content-Disposition'] == 'attachment; filename="shopping_cart.txt"', (
            f'Проверьте, что при GET запросе на {dl_url} '
            'возвращается файл с правильным именем'
        )
        assert recipe.name in response.content.decode(), (
            f'Проверьте, что при GET запросе на {dl_url} '
            'возвращается список ингредиентов рецепта'
        )