from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken
from .serializers import LoginSerializer
from .models import BlacklistedToken


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token = RefreshToken.for_user(user)
    return Response({
        'auth_token': str(token.access_token)
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    try:
        token = AccessToken(request.headers.get('Authorization').split(' ')[1])
        BlacklistedToken.objects.create(token=token, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except InvalidToken:
        return Response(status=status.HTTP_400_BAD_REQUEST)
