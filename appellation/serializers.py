from rest_framework import serializers
from appellation.models import (
    AdminZone,
    Appellation,
    Color,
    AppellationPhoto,
    AppellationType,
    AppellationZone,
    PlotZone,
    ViticultureZone,
)
from bottle.models import WineMaker
from productspec.models import WineCDC, SugarDose
from core.models import Country


class AppellationZoneSerializer(serializers.ModelSerializer):
    appellation_zone_photos = serializers.PrimaryKeyRelatedField(queryset=AppellationPhoto.objects.all(),
                                                                 many=True, required=False, allow_null=True)
    appellation = serializers.PrimaryKeyRelatedField(queryset=Appellation.objects.all(),
                                                     many=True, required=False, allow_null=True)
    admin_zones = serializers.PrimaryKeyRelatedField(queryset=AdminZone.objects.all(),
                                                     many=True, required=False, allow_null=True)
    plot_zones = serializers.PrimaryKeyRelatedField(queryset=PlotZone.objects.all(),
                                                    many=True, required=False, allow_null=True)

    class Meta:
        model = AppellationZone
        fields = [
            'id', 'name', 'parent_id', 'geom', 'ground', 'subsoil', 'climat',
            'elevetion_min', 'elevetion_max', 'elevetion_average',
            'precipitation_min', 'precipitation_max', 'precipitation_average',
            'situation', 'sunshine', 'temperature_min', 'temperature_max',
            'temperature_average', 'orientation', 'air', 'geology',
            'pedology', 'lithology', 'hierarchy',
            'appellation_zone_photos', 'appellation',
            'admin_zones', 'plot_zones', 'created_at', 'updated_at',
        ]


class AppellationPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppellationPhoto
        fields = '__all__'


class AppellationSerializer(serializers.ModelSerializer):
    appellation_colour = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all(),
                                                            many=True, required=False, allow_null=True)
    appellation_colour = serializers.PrimaryKeyRelatedField(queryset=AppellationType.objects.all(),
                                                            many=True, required=False, allow_null=True)
    wine_cdc = serializers.PrimaryKeyRelatedField(queryset=WineCDC.objects.all(),
                                                  many=True, required=False, allow_null=True)
    sugar_dose = serializers.PrimaryKeyRelatedField(queryset=SugarDose.objects.all(),
                                                    many=True, required=False, allow_null=True)

    class Meta:
        model = Appellation
        fields = [
            'id', 'name', 'zone_appelation', 'name_dgc', 'label', 'etymology', 'hierarchy',
            'volume_production', 'appellation_colour', 'appellation_colour', 'wine_cdc', 'dosage',
            'name_origin_alphabet_origin', 'name_origin_alphabet_latin', 'name_english_alphabet_latin', 'language_origin',
            'created_at', 'updated_at',
        ]


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class AppellationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppellationType
        fields = '__all__'


class AdminZoneSerializer(serializers.ModelSerializer):
    plot_zone = serializers.PrimaryKeyRelatedField(queryset=PlotZone.objects.all(),
                                                   many=True, required=False, allow_null=True)
    countries = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                                   many=True, required=False, allow_null=True)

    class Meta:
        model = AdminZone
        fields = ['id', 'name', 'parent', 'hierarchy', 'geom', 'plot_zone', 'countries']


class PlotZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlotZone
        fields = '__all__'


class ViticultureZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViticultureZone
        fields = '__all__'



