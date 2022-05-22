from rest_framework import serializers
from food_and_wine_pairing.models import (
    Cooking,
    Food,
    FoodCategory,
    FoodWineMatch,
    Ingredient,
    Recipe,
    RecipeCooking,
    RecipeIngredient,
    RecipeSpice,
    Spice
)


class FoodSeriazer(serializers.ModelSerializer):
    food_wine_match = serializers.PrimaryKeyRelatedField(queryset=FoodWineMatch.objects.all(),
                                                         many=True, required=False, allow_null=True)

    class Meta:
        model = Food
        fields = ['id', 'name', 'description',
                  'category', 'slug', 'food_wine_match', 'created_at', 'updated_at']


class FoodWineMatchSeriazer(serializers.ModelSerializer):
    class Meta:
        model = FoodWineMatch
        fields = '__all__'


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ['id', 'name', 'food']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'description', 'slug', 'recipe_ingredient', 'created_at', 'updated_at']


class CookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooking
        fields = ['id', 'name', 'description', 'slug', 'recipes_cooking', 'created_at', 'updated_at']


class SpiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spice
        fields = ['id', 'name', 'description', 'slug', 'recipe_spices', 'created_at', 'updated_at']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'slug',
                  'recipe_ingredients', 'recipe_spices', 'recipe_cooking', 'created_at', 'updated_at']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class RecipeSpiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeSpice
        fields = '__all__'


class RecipeCookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCooking
        fields = '__all__'


class AMVFoodSerializer(serializers.ModelSerializer):
    food_wine_match = serializers.PrimaryKeyRelatedField(queryset=FoodWineMatch.objects.all(),
                                                         many=True, required=False, allow_null=True)

    class Meta:
        model = Food
        fields = ['id', 'name', 'description',
                  'category', 'slug', 'food_wine_match', 'created_at', 'updated_at']
