from appellation.models import Appellation
from productspec.models import Assemble, Robe, WineProfileCDC, Vintage, Aroma, CategoryLexicon, Lexicon, WineCDCLexicon
from rest_framework import serializers
from bottle.models import WineBottle
from productspec.models import DenominationWine, Grape, GrapeAssembly, GrapeMainAccessory, GrapeProfile, SugarDose, WineCDC
from django.apps import apps


class AssembleSerializer(serializers.ModelSerializer):
    grape_assemble = serializers.PrimaryKeyRelatedField(queryset=GrapeAssembly.objects.all(),
                                                        many=True, required=False, allow_null=True)
    winecdc = serializers.PrimaryKeyRelatedField(queryset=WineCDC.objects.all(),
                                                 many=True, required=False, allow_null=True)

    class Meta:
        model = Assemble
        fields = ['id', 'name', 'grape_assemble',
                  'winecdc', 'created_at', 'updated_at']


class RobeSerializer(serializers.ModelSerializer):
    wine_profile_cdc = serializers.PrimaryKeyRelatedField(queryset=WineProfileCDC.objects.all(),
                                                          many=True, required=False, allow_null=True)

    class Meta:
        model = Robe
        fields = ['id', 'color_name', 'color_value',
                  'wine_profile_cdc', 'created_at', 'updated_at']


class WineProfileCDCSerializer(serializers.ModelSerializer):
    # wine_cdc = serializers.PrimaryKeyRelatedField(queryset=WineCDC.objects.all(),
    #   many=True, required=False, allow_null=True)
    color_id = serializers.PrimaryKeyRelatedField(queryset=Robe.objects.all(),
                                                  many=True, required=False, allow_null=True)

    class Meta:
        model = WineProfileCDC
        fields = [
            'id',            
            'color_id',
            'taste_acidity',
            'taste_alcohol',
            'taste_body',
            'taste_sweetness',
            'arom_complexity',
            'arom_intensity',
            'arom_length',
            'note_general',
            'color_desc',
            'note_fruity',
            'note_acidity',
            'note_body',
            'note_intensity',
            'temperature',
            'opening_time',
            'created_at',
            'updated_at',
        ]


class VintageSerializer(serializers.ModelSerializer):
    wine_bottles = serializers.PrimaryKeyRelatedField(queryset=WineBottle.objects.all(),
                                                      many=True, required=False, allow_null=True)

    class Meta:
        model = Vintage
        fields = [
            'id', 'id_productspec', 'apogee_min', 'apogee', 'apogee_max',
            'quality', 'year', 'year_as_int', 'wine_bottles', 'comment_vintage', 'created_at', 'updated_at'
        ]


class AromaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aroma
        fields = '__all__'


class CategoryLexiconSerializer(serializers.ModelSerializer):
    lexicons = serializers.PrimaryKeyRelatedField(queryset=Lexicon.objects.all(),
                                                  many=True, required=False, allow_null=True)

    class Meta:
        model = CategoryLexicon
        fields = ['id', 'name', 'lexicons', 'created_at', 'updated_at']


class LexiconSerializer(serializers.ModelSerializer):
    wine_cdc_lexicons = serializers.PrimaryKeyRelatedField(queryset=WineCDCLexicon.objects.all(),
                                                           many=True, required=False, allow_null=True)

    class Meta:
        model = Lexicon
        fields = [
            'id', 'name', 'description',
            'source', 'category', 'wine_cdc_lexicons', 'created_at', 'updated_at'
        ]


class WineCDCLexiconSerializer(serializers.ModelSerializer):
    class Meta:
        model = WineCDCLexicon
        fields = '__all__'


class GrapeSerializer(serializers.ModelSerializer):
    grape_assembles = serializers.PrimaryKeyRelatedField(queryset=GrapeAssembly.objects.all(),
                                                         many=True, required=False, allow_null=True)
    grape_main_accessory = serializers.PrimaryKeyRelatedField(queryset=GrapeMainAccessory.objects.all(),
                                                              many=True, required=False, allow_null=True)

    class Meta:
        model = Grape
        fields = ['id', 'name',
                  'varietal_profile_id',
                  'parent',
                  'color_varietal',
                  'technical_name',
                  'origin_country_id',
                  'survey_hectares',
                  'date_servey_hectares',
                  'comment_varietal',
                  'aromas',
                  'description_taste',
                  'description_visual',
                  'skins',
                  'cultural_aptitudes',
                  'phenology',
                  'susceptibility_diseases',
                  'guard_potential',
                  'yields',
                  'maturity',
                  'berry_size',
                  'type_variety',
                  'species',
                  'clones',
                  'year_cross',
                  'creator',
                  'name_origin_alphabet_origin',
                  'name_origin_alphabet_latin',
                  'name_en',
                  'language_origin',
                  'created_at',
                  'updated_at', 'grape_assembles', 'grape_main_accessory',
                  ]


class GrapeProfileSerializer(serializers.ModelSerializer):
    grapes = serializers.PrimaryKeyRelatedField(queryset=Grape.objects.all(),
                                                many=True, required=False, allow_null=True)

    class Meta:
        model = GrapeProfile
        fields = ['id', 'taste_acidity',
            'taste_alcohol',
            'taste_body',
            'taste_sweetness',
            'arom_complexity',
            'arom_intensity',
            'arom_length',
            'note_general', 'grapes']


class GrapeAssemblySerializer(serializers.ModelSerializer):
    class Meta:
        model = GrapeAssembly
        fields = '__all__'


class DenominationWineSerializer(serializers.ModelSerializer):
    appellations = serializers.PrimaryKeyRelatedField(queryset=Appellation.objects.all(),
                                                      many=True, required=False, allow_null=True)

    class Meta:
        model = DenominationWine
        fields = ['id', 'appellations', 'name', 'order', 'wine_cdc']


class SugarDoseSerializer(serializers.ModelSerializer):
    wine_cdc = serializers.PrimaryKeyRelatedField(queryset=WineCDC.objects.all(),
                                                  many=True, required=False, allow_null=True)
    appellations = serializers.PrimaryKeyRelatedField(queryset=Appellation.objects.all(),
                                                      many=True, required=False, allow_null=True)

    class Meta:
        model = SugarDose
        fields = [
            'id', 'name', 'type_wine', 'min_sugar_concentration',
            'max_sugar_concentration', 'appellations', 'wine_cdc'
        ]


class WineCDCSerializer(serializers.ModelSerializer):
    vintage = apps.get_model('productspec', 'Vintage')
    wine_cdc_lexicons = apps.get_model('productspec', 'WineCDCLexicon')
    vintages = serializers.PrimaryKeyRelatedField(queryset=vintage.objects.all(),
                                                  many=True, required=False, allow_null=True)
    wine_cdc_lexicons = serializers.PrimaryKeyRelatedField(queryset=wine_cdc_lexicons.objects.all(),
                                                           many=True, required=False, allow_null=True)
    denomination_wine = serializers.PrimaryKeyRelatedField(queryset=DenominationWine.objects.all(),
                                                           many=True, required=False, allow_null=True)

    class Meta:
        model = WineCDC
        fields = [
            'id', 'name', 'colour', 'type', 'comment_descritpion',
            'assemble',  'appellation', 'sugar_dose',
            'wine_cdc_lexicons', 'vintages', 'wine_profile_cdc', 'denomination_wine'
        ]
