from rest_framework import serializers
from users.models import User


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()
            if user:
                if not user.check_password(password):
                    raise serializers.ValidationError(
                        'Incorrect password'
                    )
            else:
                raise serializers.ValidationError(
                    'User with this email does not exist'
                )
            data['user'] = user
        else:
            raise serializers.ValidationError(
                'Email and password are required'
            )
        return data
