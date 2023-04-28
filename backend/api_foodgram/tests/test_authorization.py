from http import HTTPStatus

import pytest
from fixtures.user_fixtures import * # noqa
from utils import assert_url_exists


@pytest.mark.django_db(transaction=True)
class TestAuth:
    signup_url = '/api/v1/users/'
    login_url = '/api/v1/auth/token/login/'
    logout_url = '/api/v1/auth/token/logout/'

    def test_signup(self, client, user_factory, django_user_model):
        user = user_factory.build()
        data = {
            'username': user.username,
            'password': user.password,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        response = client.post(self.signup_url, data=data)
        assert_url_exists(response, self.signup_url)
        assert response.status_code == HTTPStatus.CREATED, (
            f'Проверьте, что при POST запросе на {self.signup_url} '
            'с корректными данными возвращается статус 201'
        )
        last_user = django_user_model.objects.last()
        assert last_user.username == user.username, (
            f'Проверьте, что при POST запросе на {self.signup_url}  '
            'с корректными данными создается пользователь'
        )

    def test_nodata_signup(self, client):
        response = client.post(self.signup_url)
        assert_url_exists(response, self.signup_url)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Проверьте, что при POST запросе на {self.signup_url} '
            'с некорректными данными возвращается статус 400'
        )

    def test_invalid_data_signup(self, client):
        data = {
            'username': 'test',
            'password': 'test',
            'email': 'test@test.test',
            'first_name': 'test',
            'last_name': 'test'
        }
        response = client.post(self.signup_url, data=data)
        assert_url_exists(response, self.signup_url)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Проверьте, что при POST запросе на {self.signup_url} '
            'с некорректными данными возвращается статус 400'
        )

    def test_duplicate_username_or_email_signup(self, client, user_factory):
        user = user_factory.create()
        data = {
            'username': user.username,
            'password': user.password,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        response = client.post(self.signup_url, data=data)
        assert_url_exists(response, self.signup_url)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Проверьте, что при POST запросе на {self.signup_url} '
            'с существующим username или email возвращается статус 400'
        )

    def test_nodata_login(self, client):
        response = client.post(self.login_url)
        assert_url_exists(response, self.login_url)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Проверьте, что при POST запросе на {self.login_url} '
            'с некорректными данными возвращается статус 400'
        )

    def test_login_logout(self, client, user_factory, user_client):
        user = user_factory.create()
        user.set_password('Tester123987')
        user.save()
        data = {
            "email": user.email,
            "password": 'Tester123987'
        }
        response = client.post(self.login_url, data=data)
        assert_url_exists(response, self.login_url)
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что при POST запросе на {self.login_url} '
            'с корректными данными возвращается статус 200'
            f'{response.data}'
        )
        assert 'auth_token' in response.data, (
            f'Проверьте, что при POST запросе на {self.login_url} '
            'возвращается токен'
        )
        response = user_client.post(self.logout_url)
        assert_url_exists(response, self.logout_url)
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f'Проверьте, что при POST запросе на {self.logout_url} '
            'с корректными данными возвращается статус 204'
        )
