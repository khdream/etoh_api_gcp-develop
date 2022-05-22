from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register


from core.models import Country


@register(Country)
class CountryIndex(AlgoliaIndex):
    fields = ('name', 'originalname_originalalphabet' , 'originalname_latinalphabet' , 'name_en')
    settings = {'searchableAttributes': ['name', 'name_origin_alphabet_origin' , 'name_origin_alphabet_latin' , 'name_english_alphabet_latin']}
    index_name = 'Country'
