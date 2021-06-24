from django.contrib.auth import get_user_model
from rest_framework import serializers

from foodgram.models import Favorites, Ingredients, ShopList, Recipe
from users.models import Follow

User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='author',
        queryset=User.objects.all(),
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = ('user', 'id')


class FavoritesSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='recipe',
        queryset=Recipe.objects.all(),
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorites
        fields = ('user', 'id')


class IngredientsSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Ingredients
        fields = ('name', 'dimension')


class ShopListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='recipe',
        queryset=Recipe.objects.all(),
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ShopList
        fields = ('user', 'id')
