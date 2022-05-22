from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
import algoliasearch_django as algoliasearch
from bottle.models import WineMaker


@register(WineMaker)
class WineMakerIndex(AlgoliaIndex):
    fields = ('name', 'siren', 'viticulture', 'creation_date',
              'address', 'gps_location', 'type_winemaker', 'comment_winemaker')
    settings = {'searchableAttributes': [
        'name'
    ]}
    index_name = 'WineMaker'
