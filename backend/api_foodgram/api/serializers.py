import base64

from django.contrib.auth.password_validation import validate_password
from django.core.files.base import ContentFile
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from rest_framework.validators import ValidationError
from users.models import User, UserProfile

MAX_COOKING_TIME = 32_000
MIN_COOKING_TIME = 1
MAX_AMOUNT = 32_000
MIN_AMOUNT = 1


class Base64ImageField(serializers.ImageField):
    """
    Custom serializer field for uploading base64 encoded images.
    """
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField(method_name='subscribed')

    class Meta:
        model = User
        fields = (
            'email', 'username',
            'first_name', 'last_name',
            'id', 'is_subscribed'
        )

    def subscribed(self, obj):
        user = self.context['request'].user
        return user in obj.subscribers.all()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(many=True)
    author = UserSerializer()
    is_favorited = serializers.SerializerMethodField(method_name='favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='in_shopping_cart'
    )
    cooking_time = serializers.IntegerField(
        min_value=MIN_COOKING_TIME,
        max_value=MAX_COOKING_TIME
    )

    class Meta:
        model = Recipe
        fields = '__all__'

    def favorited(self, obj):
        user = self.context['request'].user
        return user.profile in obj.favorited_by.all()

    def in_shopping_cart(self, obj):
        user = self.context['request'].user
        return user.profile in obj.added_to_cart_by.all()


class IngredientRecipeCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for RecipeIngredient model + Ingredient model
    for use in RecipeCreateSerializer.
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id')
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = (
        serializers.CharField(
            read_only=True,
            source='ingredient.measurement_unit'))
    amount = serializers.IntegerField(
        min_value=MIN_AMOUNT,
        max_value=MAX_AMOUNT
    )

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']


class RecipeCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for Recipe creation and updates
    """
    ingredients = IngredientRecipeCreateSerializer(
        many=True,
        source='recipe_ingredients'
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        exclude = ('author',)

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user

        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipe_ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.add_ingredients(recipe, ingredients)
        recipe.tags.set(tags)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipe_ingredients')
        instance = super().update(instance, validated_data)
        self.add_ingredients(instance, ingredients)
        instance.tags.set(tags)

        return instance

    def add_ingredients(self, instance, ingredients):
        """
        Bulk create RecipeIngredient objects for given recipe
        """
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=instance,
                ingredient=ingredient['ingredient']['id'],
                amount=ingredient['amount']
            ) for ingredient in ingredients if ingredient.get('amount', None)
        ])


class ShortRecipeSerializer(serializers.ModelSerializer):
    """
    Recipe serializer for use in various User serializers
    """

    cooking_time = serializers.IntegerField(
        min_value=MIN_COOKING_TIME,
        max_value=MAX_COOKING_TIME
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSerializerWithRecipes(UserSerializer):
    """
    User serializer with recipes and recipes_limit param handling
    """
    recipes = ShortRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'recipes',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        recipes_limit = self.context.get('recipes_limit')
        if recipes_limit:
            data['recipes'] = data['recipes'][:int(recipes_limit)]
        return data


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for user creation
    """
    class Meta:
        model = User
        fields = (
            'email', 'username',
            'first_name', 'last_name',
            'password', 'id'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user)
        return user


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise ValidationError('Неверный пароль')
        return value
