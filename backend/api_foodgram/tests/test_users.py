from http import HTTPStatus

import pytest
from fixtures.user_fixtures import * # noqa
from utils import assert_url_exists, check_pagination


@pytest.mark.django_db(transaction=True)
class TestUsers:
    users_url = '/api/v1/users/'
    users_me = '/api/v1/users/me/'
    users_subscriptions = '/api/v1/users/subscriptions/'
    users_subscribe = '/api/v1/users/{id}/subscribe/'

    def test_users(self, user_client, user_factory):
        user_factory.create_batch(10)
        response = user_client.get(self.users_url)
        assert_url_exists(response, self.users_url)
        check_pagination(self.users_url, response.json())
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что при GET запросе на {self.users_url} '
            'возвращается статус 200'
        )

    def test_users_me(self, user_client, user):
        u, _ = user
        response = user_client.get(self.users_me)
        assert_url_exists(response, self.users_me)
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что при GET запросе на {self.users_me} '
            'возвращается статус 200'
        )
        assert response.json()['email'] == u.email, (
            f'Проверьте, что при GET запросе на {self.users_me} '
            'возвращается информация о текущем пользователе'
        )

    def test_user_detail(self, user_client, user_factory):
        user = user_factory.create()
        response = user_client.get(f'{self.users_url}{user.id}/')
        assert_url_exists(response, f'{self.users_url}{user.id}/')
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что при GET запросе на {self.users_url}id/ '
            'возвращается статус 200'
        )
        assert response.json()['email'] == user.email, (
            f'Проверьте, что при GET запросе на {self.users_url}id/ '
            'возвращается информация о пользователе'
        )
