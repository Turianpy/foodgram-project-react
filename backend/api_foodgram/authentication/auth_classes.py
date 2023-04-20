from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import BlacklistedToken
from rest_framework_simplejwt.exceptions import InvalidToken


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth = super().authenticate(request)
        if auth is None:
            return None
        user, token = auth
        if BlacklistedToken.objects.filter(token=token).exists():
            raise InvalidToken()
        return auth
