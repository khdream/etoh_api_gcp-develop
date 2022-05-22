from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register


from appellation.models import (
    AdminZone,
    Appellation,
    ViticultureZone,
)
from core.models import Country


@register(Appellation)
class AppellationIndex(AlgoliaIndex):
    fields = ('name', 'name_dgc', 'zone_appelation', 'name_origin_alphabet_origin' , 'name_origin_alphabet_latin' , 'name_english_alphabet_latin')
    settings = {'searchableAttributes': ['name',  'name_dgc', 'name_origin_alphabet_origin' , 'name_origin_alphabet_latin' , 'name_english_alphabet_latin']}
    index_name = 'Appellation'


@register(AdminZone)
class AdminZoneIndex(AlgoliaIndex):
    fields = ('name', 'code_insee')
    settings = {'searchableAttributes': ['name']}
    index_name = 'AdminZone'


@register(ViticultureZone)
class ViticultureZoneIndex(AlgoliaIndex):
    fields = ('name', 'hierarchy', 'name_origin_alphabet_origin' , 'name_origin_alphabet_latin' , 'name_english_alphabet_latin')
    settings = {'searchableAttributes': ['name' , 'name_origin_alphabet_origin' , 'name_origin_alphabet_latin' , 'name_english_alphabet_latin']}
    index_name = 'ViticultureZone'


