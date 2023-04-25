from rest_framework import serializers
from users.models import User


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return value

    def validate_password(self, value):
        if not User.objects.filter(password=value).exists():
            raise serializers.ValidationError('Неверный пароль')
        return value
