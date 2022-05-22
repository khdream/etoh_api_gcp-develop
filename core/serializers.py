from productspec.models import WineCDC
from rest_framework import serializers
from core.models import Country
from bottle.models import WineMaker





class CountrySerializer(serializers.ModelSerializer):
    # winemaker = serializers.PrimaryKeyRelatedField(queryset=WineMaker.objects.all(),
    #                                                many=True, required=False, allow_null=True)

    class Meta:
        model = Country
        fields = ['id', 'name',
                  'zone_admin', 'id_language', 'originalname_originalalphabet', 'originalname_latinalphabet',
                  'name_fr', 'name_en', 'name_en_full', 'languages', 'code_isoalpha2', 'code_isoalpha3',
                  'code_isonum', 'created_at', 'updated_at', ]
