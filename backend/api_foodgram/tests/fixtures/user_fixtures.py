import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def user_superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        username='admin',
        email='admin@foodgram.com',
        password='admin'
    )


@pytest.fixture
def user(django_user_model, user_profile_factory):
    user = django_user_model.objects.create_user(
        username='test_user',
        email='test@test.test',
        password='Qwerty1235'
    )
    profile = user_profile_factory.create(user=user)
    return user, profile


@pytest.fixture
def superuser_token(user_superuser):
    token = AccessToken.for_user(user_superuser)
    return {'access': str(token), }


@pytest.fixture
def user_token(user):
    token = AccessToken.for_user(user[0])
    return {'access': str(token), }


@pytest.fixture
def superuser_client(superuser_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {superuser_token["access"]}'
    )
    return client


@pytest.fixture
def user_client(user_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {user_token["access"]}'
    )
    return client
