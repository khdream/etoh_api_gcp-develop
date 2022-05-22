from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from food_and_wine_pairing.models import Food, FoodWineMatch


@register(Food)
class FoodIndex(AlgoliaIndex):
    fields = ('name', 'description')
    settings = {'searchableAttributes': ['name', 'description']}
    index_name = 'Food'


@register(FoodWineMatch)
class FoodWineMatchIndex(AlgoliaIndex):
    fields = ('vineyard')
    settings = {'searchableAttributes': ['vineyard']}
    index_name = 'FoodWineMatch'
