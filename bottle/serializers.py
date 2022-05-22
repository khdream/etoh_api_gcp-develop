from appellation.models import Appellation
from productspec.models import DenominationWine, WineCDC
from rest_framework import serializers
from bottle.models import (
    Bottle,
    BottlePhoto,
    Price,
    NoteGuide,
    Range,
    WineBottle,
    WineMaker,
    WineMakerProfile,
    Stock,
    StockList,
    Warehouse,
)




class StockListSerializer(serializers.ModelSerializer):
    bottle_prices = serializers.PrimaryKeyRelatedField(queryset=Price.objects.all(),
                                                       many=True, required=False, allow_null=True)
    stocks = serializers.PrimaryKeyRelatedField(queryset=Stock.objects.all(),
                                                many=True, required=False, allow_null=True)

    class Meta:
        model = StockList
        fields = [
            'id', 'id_range', 'id_bottle', 'sku', 'wine_name',
            'country', 'region', 'subregion', 'appellation', 'label',
            'grape_assemble', 'colour', 'type', 'vintage', 'winemaker',
            'certification', 'volume', 'weight', 'comment', 'note',
            'image', 'price_pre_taxe', 'vat', 'price_with_taxe', 'status',
            'currency', 'bottle_prices', 'stocks', 'created_at', 'updated_at'
        ]



class WarehouseSeriazer(serializers.ModelSerializer):
    stocks = serializers.PrimaryKeyRelatedField(queryset=Stock.objects.all(),
                                                many=True, required=False, allow_null=True)

    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'client', 'stocks']


class StockSeriazer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class RangeSerializer(serializers.ModelSerializer):
    # stocklists = serializers.PrimaryKeyRelatedField(queryset=StockList.objects.all(),
    #                                                 many=True, required=False, allow_null=True)

    class Meta:
        model = Range
        fields = ['id', 'name', 'client', 'created_at', 'updated_at']


class BottleSerializer(serializers.ModelSerializer):

    bottle_photos = serializers.PrimaryKeyRelatedField(queryset=BottlePhoto.objects.all(),
                                                       many=True, required=False, allow_null=True)

    class Meta:
        model = Bottle
        fields = ['id', 'wine_bottle', 'volume', 'gtin',
                  'code', 'container', 'bottle_photos', 'created_at', 'updated_at']


class WineBottleSerializer(serializers.ModelSerializer):
    bottles = serializers.PrimaryKeyRelatedField(queryset=Bottle.objects.all(),
                                                 many=True, required=False, allow_null=True)
    note_guides = serializers.PrimaryKeyRelatedField(queryset=NoteGuide.objects.all(),
                                                     many=True, required=False, allow_null=True)

    class Meta:
        model = WineBottle
        fields = [
            'id', 'wine_profile_cdc', 'vintage', 'winemaker', 'assemble', 'comment_degustation',
            'comment_vinification', 'comment_viticulture', 'certification', 'alcohol', 'name_tank',
            'bottles', 'note_guides','created_at','updated_at',
        ]


class WineMakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WineMaker
        fields = '__all__'


class WineMakerProfileSerializer(serializers.ModelSerializer):
    winemakers = serializers.PrimaryKeyRelatedField(queryset=WineMaker.objects.all(),
                                                    many=True, required=False, allow_null=True)

    class Meta:
        model = WineMakerProfile
        fields = [
            'id', 'taste_acidity', 'taste_alcohol', 'taste_body',
            'taste_sucrosite', 'aroma_complexity', 'aroma_intensity',
            'aroma_length', 'general_note', 'winemakers','created_at','updated_at',
        ]




class NoteGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteGuide
        fields = '__all__'


class BottlePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BottlePhoto
        fields = '__all__'

class BottlePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


