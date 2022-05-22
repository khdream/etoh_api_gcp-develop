from food_and_wine_pairing.views import (
    CookingViewSet,
    FoodViewSet,
    FoodCategoryViewSet,
    FoodWineMatchViewSet,
    IngredientViewSet,
    RecipeViewSet,
    RecipeIngredientViewSet,
    RecipeSpiceViewSet,
    RecipeCookingViewSet,
    SpiceViewSet,
)
from core.urls import router


router.register(r'food', FoodViewSet, basename='food')
router.register(r'food_wine_match', FoodWineMatchViewSet,
                basename='food_wine_match')
router.register(r'food_category', FoodCategoryViewSet,
                basename='food_category')
router.register(r'ingredient', IngredientViewSet, basename='ingredient')
router.register(r'cooking', CookingViewSet, basename='cooking')
router.register(r'spice', SpiceViewSet, basename='spice')
router.register(r'recipe', RecipeViewSet, basename='recipe')
router.register(r'recipe_ingredient', RecipeIngredientViewSet,
                basename='recipe_ingredient')
router.register(r'recipe_spice', RecipeSpiceViewSet,
                basename='recipe_spice')
router.register(r'recipe_cooking', RecipeCookingViewSet,
                basename='recipe_cooking')
