from productspec.models import Grape, WineCDC
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register


@register(Grape)
class GrapeIndex(AlgoliaIndex):
    fields = ('name', 'varietal_profile_id', 'parent', 'color_varietal', 'technical_name', 'origin_country_id', 'survey_hectares', 'date_servey_hectares',
              'comment_varietal', 'aromas', 'description_taste', 'description_visual',
              'skins', 'cultural_aptitudes', 'phenology', 'guard_potential', 'yields',
              'maturity', 'berry_size', 'species', 'year_cross', 'creator', 'clones', 'grape_assembles', 'name_origin_alphabet_origin' , 'name_origin_alphabet_latin' , 'name_en' )
    settings = {'searchableAttributes': ['name', 'name_origin_alphabet_origin' , 'name_origin_alphabet_latin' , 'name_english_alphabet_latin']}
    index_name = 'Grape'


@register(WineCDC)
class WineCDCIndex(AlgoliaIndex):
    fields = ('name', 'grape', 'color', 'appellations', 'appellation_id',
              'dgc', 'type', 'sugar_dose_id', 'denomination_wines', 'zone_appellation_id')
    settings = {'searchableAttributes': [
        'name',  'grape', 'appellations', 'colour', 'dgc', 'type', 'sugar_dose', 'denomination_wines']}
    index_name = 'WineCDC'
