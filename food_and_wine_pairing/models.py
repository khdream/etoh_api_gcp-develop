from django.db import models
from datetime import date, datetime  
# Create your models here.


class FoodCategory(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Food Category'
        verbose_name_plural = 'Food Categories'
        db_table = 'food_category'

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=255, blank=True,
                            null=True, unique=True)
    description = models.TextField(null=True, blank=True)
    category = models.ManyToManyField(FoodCategory, through='LinkFoodCategory')
    slug = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Food'
        db_table = 'food_food'

    def __str__(self):
        return self.name


class FoodWineMatch(models.Model):
    food = models.ForeignKey(
        Food, on_delete=models.CASCADE, null=True, blank=True, related_name='food_wine_match')
    country = models.CharField(max_length=255,  null=True, blank=True)
    region = models.TextField(null=True, blank=True)
    vineyard = models.TextField(null=True, blank=True)
    appellation = models.TextField(blank=True, null=True)
    dgs = models.TextField(null=True, blank=True)
    grape = models.TextField(blank=True, null=True)
    type = models.TextField(null=True, blank=True)
    color = models.TextField(blank=True, null=True)
    dose = models.TextField(blank=True, null=True)
    dvitivini = models.TextField(blank=True, null=True)
    source = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Food Wine Match'
        verbose_name_plural = 'Food Wine Matchs'
        db_table = 'food_wine_pairing'

    def __str__(self):
        return f' FoodWineMatch {self.id}'

class LinkFoodCategory(models.Model):
    id_mets = models.ForeignKey(
        Food, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipe_spices')
    id_categorie = models.ForeignKey(
        FoodCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipe_spices')
    value = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Recipe spice relation'
        verbose_name_plural = 'Recipe spice relations'
        db_table = 'food_link_food_category'

    def __str__(self):
        return self.value

class Ingredient(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        db_table = 'food_ingredient'

    def __str__(self):
        return self.name


class Cooking(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Cooking'
        verbose_name_plural = 'Cooking'
        db_table = 'food_cooking'

    def __str__(self):
        return self.name


class Spice(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Spice'
        verbose_name_plural = 'Spices'
        db_table = 'food_spice'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    food = models.ForeignKey(
        Food, on_delete=models.CASCADE, null=True, blank=True, related_name='recipes')
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipies'
        db_table = 'food_recipe'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipe_ingredient')
    value = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Recipe ingredient relation'
        verbose_name_plural = 'Recipe ingredient relations'
        db_table = 'food_recipe_ingredient'

    def __str__(self):
        return self.value


class RecipeSpice(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipe_spices')
    spice = models.ForeignKey(
        Spice, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipe_spices')
    value = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Recipe spice relation'
        verbose_name_plural = 'Recipe spice relations'
        db_table = 'food_recipe_spice'

    def __str__(self):
        return self.value


class RecipeCooking(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipe_cooking')
    cooking = models.ForeignKey(
        Cooking, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipes_cooking')
    value = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Recipe cooking relation'
        verbose_name_plural = 'Recipe cooking relations'
        db_table = 'food_recipe_cooking'

    def __str__(self):
        return self.value
