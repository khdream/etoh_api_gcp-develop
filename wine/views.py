from rest_framework.viewsets import ModelViewSet
from wine.serializers import (
    DenominationWineSerializer,
    GrapeSerializer,
    GrapeAssemblySerializer,
    GrapeProfileSerializer,
    WineCDCSerializer,
    SugarDoseSerializer
)
from productspec.models import Grape, GrapeAssembly, GrapeProfile, DenominationWine, WineCDC, SugarDose
from bottle.models import Bottle, WineBottle
from bottle.serializers import BottleSerializer, NoteGuideSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import Response


class GrapeViewSet(ModelViewSet):
    serializer_class = GrapeSerializer
    queryset = Grape.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class GrapeProfileViewSet(ModelViewSet):
    serializer_class = GrapeProfileSerializer
    queryset = GrapeProfile.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class SugarDoseViewSet(ModelViewSet):
    serializer_class = SugarDoseSerializer
    queryset = SugarDose.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class WineCDCViewSet(ModelViewSet):
    serializer_class = WineCDCSerializer
    queryset = WineCDC.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class GrapeAssemblyViewSet(ModelViewSet):
    serializer_class = GrapeAssemblySerializer
    queryset = GrapeAssembly.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class DenominationWineViewSet(ModelViewSet):
    serializer_class = DenominationWineSerializer
    queryset = DenominationWine.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class BottleViewSet(ModelViewSet):
    serializer_class = BottleSerializer
    queryset = Bottle.objects.all().select_related('wine_bottle')

    def get_object(self, pk):
        rstatus = 200
        try:
            obj = self.queryset.filter(id=pk).first()
            if not obj:
                rstatus = 404

        except ValueError:
            obj = None
            rstatus = 400
        return obj, rstatus

    def destroy(self, request, **kwargs):
        bottle = self.queryset.filter(id=kwargs.get('pk'))
        if not bottle:
            return Response({"error": f"There is no bottle with this id ({kwargs.get('pk')})"}, status.HTTP_404_NOT_FOUND)
        bottle.delete()
        return Response({
            "deleted": True,
        })

    @action(methods=['GET'], detail=False, url_path='blend/(?P<pk>[^/.]+)')
    def get_bottle_blend(self, request, pk):
        if not pk:
            return Response({'error': 'Please add id'}, status=status.HTTP_400_BAD_REQUEST)
        bottle, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"Please verify the parameter. id_bouteille is incorrect. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no bottle with this id ({pk})"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            if not bottle.wine_bottle or not bottle.wine_bottle.assemble or not bottle.wine_bottle.assemble.grape_assemble.all():
                return Response({"error": f"The bottle is not linked to any grape assembles. Provided = {pk}"}, status.HTTP_404_NOT_FOUND)
            grape_assembles = bottle.wine_bottle.assemble.grape_assemble.all()
            response = []
            for grape_assemble in grape_assembles:
                response.append(
                    {
                        "name": grape_assemble.grape.name,
                        "percentage": grape_assemble.percentage
                    }
                )
            response_status = status.HTTP_200_OK

        return Response(response, response_status)

    @action(methods=['GET'], detail=False, url_path='photo/(?P<pk>[^/.]+)')
    def get_photo(self, request, pk):
        if not pk:
            return Response({'error': 'Please add id'}, status=status.HTTP_400_BAD_REQUEST)
        bottle, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"Please verify the parameter. id_bouteille is incorrect. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no bottle with this id ({pk})"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            bottle_photos = bottle.bottle_photos.all()
            if not bottle_photos:
                return Response({"error": f"There is any photo linked to this bottle. Provided = {pk}"}, status.HTTP_404_NOT_FOUND)
            results = []
            for bottle_photo in bottle_photos:
                results.append({
                    "photo": bottle_photo.url
                })
            response = {
                "results": results
            }
            response_status = status.HTTP_200_OK

        return Response(response, response_status)

    @action(methods=['GET'], detail=False, url_path='photo360/(?P<pk>[^/.]+)')
    def get_photo_360(self, request, pk):
        bottle, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"Please verify the parameter. id_bouteille is incorrect. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no bottle with this id ({pk})"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            bottle_photos = bottle.bottle_photos.filter(type_photo='360')
            if not bottle_photos:
                return Response({"error": f"There is any photo linked to this bottle. Provided = {pk}"}, status.HTTP_404_NOT_FOUND)
            results = []
            for bottle_photo in bottle_photos:
                results.append({
                    "photo": bottle_photo.url
                })
            response = {
                "results": results
            }
            response_status = status.HTTP_200_OK

        return Response(response, response_status)

    @action(methods=['GET'], detail=False, url_path='notes/(?P<pk>[^/.]+)')
    def get_bottle_notes(self, request, pk):
        if not pk:
            return Response({'error': 'Please add id'}, status=status.HTTP_400_BAD_REQUEST)
        bottle, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"Please verify the parameter. id_bouteille is incorrect. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no bottle with this id ({pk})"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            bottle_notes = bottle.wine_bottle.note_guides.all()
            if not bottle_notes:
                return Response({"error": f"There is any notes linked to this bottle. Provided = {pk}"}, status.HTTP_404_NOT_FOUND)
            response = []
            for bottle_note in bottle_notes:
                response.append(NoteGuideSerializer(bottle_note).data)
            response_status = status.HTTP_200_OK

        return Response(response, response_status)

    @action(methods=['GET'], detail=False, url_path='properties/(?P<pk>[^/.]+)')
    def get_bottle_properties(self, request, pk):
        if not pk:
            return Response({'error': 'Please add id'}, status=status.HTTP_400_BAD_REQUEST)
        bottle, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"Please verify the parameter. id_bouteille is incorrect. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no bottle with this id ({pk})"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            response = self.serializer_class(bottle).data
            response_status = status.HTTP_200_OK
        return Response(response, response_status)

    @action(methods=['POST'], detail=False, url_path='match')
    def match_bottle(self, request):
        name_app_dgc = request.data.get('name_app_dgc', '')
        winemaker = request.data.get('winemaker_name', '')
        if not name_app_dgc or not winemaker:
            return Response({
                "input": request.data,
                "bottle_info": {
                    "error": "An error as occured, check your input data"
                }
            }, status.HTTP_404_NOT_FOUND)
        type = request.data.get('type', '')
        denomination_wine = request.data.get('denomination_wine', '')
        colour = request.data.get('colour', '')
        vintage = request.data.get('vintage', '')
        volume = request.data.get('bottle_volume', 0)
        gtin = request.data.get('bottle_gtin', 0)
        code = request.data.get('bottle_code', '')
        container = request.data.get('bottle_container', '')

        bottle_queryset = self.queryset.filter(
            wine_bottle__wine_profile_cdc__wine_cdc__appellation__name=name_app_dgc)
        bottle_queryset = bottle_queryset.filter(
            wine_bottle__winemaker__name=winemaker)
        if type:
            bottle_queryset.filter(
                wine_bottle__wine_profile_cdc__wine_cdc__type=type)
        if denomination_wine:
            bottle_queryset.filter(
                wine_bottle__wine_profile_cdc__wine_cdc__denomination_wine__name=denomination_wine)
        if colour:
            bottle_queryset.filter(
                wine_bottle__wine_profile_cdc__wine_cdc__colour=colour)
        if vintage:
            bottle_queryset.filter(
                wine_bottle__wine_profile_cdc__wine_cdc__vintages__year__year=vintage)
        if volume:
            bottle_queryset.filter(volume=volume)
        if gtin:
            bottle_queryset.filter(gtin=gtin)
        if code:
            bottle_queryset.filter(code=code)
        if container:
            bottle_queryset.filter(container=container)
        wine_bottle = ''
        wine_profile = ''
        if len(bottle_queryset):
            bottle = bottle_queryset.first()
            response = {}
            if bottle:
                response['id_bottle'] = bottle.id
                wine_bottle = bottle.wine_bottle
                if wine_bottle:
                    response['id_wine_bottle'] = wine_bottle.id
                    wine_profile = wine_bottle.wine_profile_cdc
                    winemaker = wine_bottle.winemaker
                    if winemaker:
                        response['winemaker'] = {
                            'id': winemaker.id,
                            'name': winemaker.name,
                        }
                    if wine_profile:
                        wine_cdc = wine_profile.wine_cdc.all().first()
                        if wine_cdc:
                            response['id_wine_cdc'] = wine_cdc.id
                            vintage = wine_cdc.vintages.all().first()
                            if vintage:
                                response['id_vintage'] = vintage.id

            return Response({
                "input": request.data,
                "info": response
            })
        else:
            wine_bottles = WineBottle.objects.all().select_related(
                'wine_profile_cdc', 'winemaker')

            if wine_bottles.filter(
                    wine_profile_cdc__wine_cdc__appellation__name=name_app_dgc):
                wine_bottle = wine_bottles.filter(
                    wine_profile_cdc__wine_cdc__appellation__name=name_app_dgc).first()
            else:
                wine_bottle = wine_bottles.filter(
                    winemaker__name=winemaker).first()
            bottle = None
            if wine_bottle:
                bottle = Bottle.objects.create(
                    wine_bottle=wine_bottle,
                    volume=volume,
                    gtin=gtin,
                    code=code,
                    container=container
                )
                response = {}
            if bottle:
                response['id_bottle'] = bottle.id
                wine_bottle = bottle.wine_bottle
                if wine_bottle:
                    response['id_wine_bottle'] = wine_bottle.id
                    wine_profile = wine_bottle.wine_profile_cdc
                    winemaker = wine_bottle.winemaker
                    if winemaker:
                        response['winemaker'] = {
                            'id': winemaker.id,
                            'name': winemaker.name,
                        }
                    if wine_profile:
                        wine_cdc = wine_profile.wine_cdc.all().first()
                        if wine_cdc:
                            response['id_wine_cdc'] = wine_cdc.id
                            vintage = wine_cdc.vintages.all().first()
                            if vintage:
                                response['id_vintage'] = vintage.id
                return Response({
                    "input": request.data,
                    "info": response

                })
            else:
                bottle = Bottle.objects.create(
                    volume=volume,
                    gtin=gtin,
                    code=code,
                    container=container
                )
                return Response(self.serializer_class(bottle).data)


class WineViewSet(ModelViewSet):
    serializer_class = WineCDCSerializer
    queryset = WineCDC.objects.all().select_related(
        'appellation', 'wine_profile_cdc').prefetch_related('assemble')

    def get_object(self, pk):
        rstatus = 200
        try:
            obj = self.queryset.filter(id=pk).first()
            if not obj:
                rstatus = 404

        except ValueError:
            obj = None
            rstatus = 400
        return obj, rstatus

    @action(methods=['GET'], detail=False, url_path='terroir/(?P<pk>[^/.]+)')
    def get_wine_cdc(self, request, pk):
        if not pk:
            return Response({'error': 'Please add id'}, status=status.HTTP_400_BAD_REQUEST)
        wine_cdc, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"Please verify the parameter. wine_id is incorrect. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no wine_cdc with this id ({pk})"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            zone_appellation = wine_cdc.appellation.zone_appelation
            if zone_appellation:
                subsoil = zone_appellation.subsoil
                climat = zone_appellation.climat
            else:
                return Response({"message": "There is no zone appellation assigned to this wine"}, status=status.HTTP_400_BAD_REQUEST)
            response = {
                "subsoil": subsoil,
                "climat": climat,
            }
            response_status = status.HTTP_200_OK
        return Response(response, response_status)

    @action(methods=['GET'], detail=False, url_path='blend/(?P<pk>[^/.]+)')
    def get_blend(self, request, pk):
        if not pk:
            return Response({'error': 'Please add id'}, status=status.HTTP_400_BAD_REQUEST)
        wine_cdc, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"Please verify the parameter. wine_id is incorrect. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no wine_cdc with this id ({pk})"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            grape_assemble = wine_cdc.assemble.grape_assemble.all()
            if not grape_assemble:
                return Response({"error": f"The identifier provided is not linked to any wine. Provided = {pk}"}, status.HTTP_404_NOT_FOUND)
            response = []
            for grape_assemble in grape_assemble:
                response.append(
                    {
                        "name": grape_assemble.grape.name,
                        "percentage": grape_assemble.percentage
                    }
                )
            response_status = status.HTTP_200_OK
        return Response(response, response_status)

    @action(methods=['GET'], detail=False, url_path='climax/(?P<pk>[^/.]+)')
    def get_climax(self, request, pk):
        if not pk:
            return Response({'error': 'Please add id'}, status=status.HTTP_400_BAD_REQUEST)
        wine_cdc, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"Please verify the parameter. wine_id is incorrect. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no wine_cdc with this id ({pk})"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            vintage = wine_cdc.vintages.all().first()
            if not vintage:
                return Response({"error": f"The identifier provided is not linked to any vintage. Provided = {pk}"}, status.HTTP_404_NOT_FOUND)
            response = {
                "apogee": vintage.apogee
            }
            response_status = status.HTTP_200_OK
        return Response(response, response_status)

    @action(methods=['GET'], detail=False, url_path='serve/(?P<pk>[^/.]+)')
    def get_serve(self, request, pk):
        if not pk:
            return Response({'error': 'Please add id'}, status=status.HTTP_400_BAD_REQUEST)
        wine_cdc, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"Please verify the parameter. wine_id is incorrect. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no wine_cdc with this id ({pk})"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            wine_profile = wine_cdc.wine_profile_cdc
            if not wine_profile:
                return Response({"error": f"The identifier provided is not linked to any wine profile. Provided = {pk}"}, status.HTTP_404_NOT_FOUND)
            response = {
                "serve_temperature": wine_profile.temperature,
                "opening_time": wine_profile.opening_time,
            }
            response_status = status.HTTP_200_OK
        return Response(response, response_status)

    @action(methods=['GET'], detail=False, url_path='profile/(?P<pk>[^/.]+)')
    def get_profile(self, request, pk):
        if not pk:
            return Response({'error': 'Please add id'}, status=status.HTTP_400_BAD_REQUEST)
        wine_cdc, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"Please verify the parameter. wine_id is incorrect. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no wine_cdc with this id ({pk})"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            wine_profile = wine_cdc.wine_profile_cdc
            if not wine_profile:
                return Response({"error": f"The identifier provided is not linked to any wine. Provided = {pk}"}, status.HTTP_404_NOT_FOUND)
            aromes = []
            for arome in wine_profile.aromas.all():
                aromes.append({
                    "name": arome.name,
                    "category": arome.category,
                })
            robe_colour = ''
            robe_description = ''
            if wine_profile.robe:
                robe_colour = wine_profile.robe.name_colour
                robe_description = wine_profile.robe.value_colour
            response = {
                "robe_colour": robe_colour,
                "robe_description": robe_description,
                "acidity_taste": wine_profile.acidity_taste,
                "alcohol_taste": wine_profile.alcohol_taste,
                "body_taste": wine_profile.body_taste,
                "aroma_complexity": wine_profile.aroma_complexity,
                "aroma_intensity": wine_profile.aroma_intensity,
                "aroma_length": wine_profile.aroma_length,
                "aromes": aromes
            }
            response_status = status.HTTP_200_OK
        return Response(response, response_status)

    @action(methods=['GET'], detail=False, url_path='appellation_properties/(?P<pk>[^/.]+)')
    def get_properties(self, request, pk):
        if not pk:
            return Response({'error': 'Please add id'}, status=status.HTTP_400_BAD_REQUEST)
        wine_cdc, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"Please verify the parameter. wine_id is incorrect. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no wine_cdc with this id ({pk})"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            appellation_zone = wine_cdc.appellation.zone_appelation
            response = {
                'colour': '',
                'type': '',
                'sugar_dose': '',
                'viticulture_zone': '',
                'country': '',
                'label': '',
            }
            if wine_cdc.colour:
                response['colour'] = wine_cdc.colour
            if wine_cdc.type:
                response['type'] = wine_cdc.type
            if wine_cdc.sugar_dose:
                response['sugar_dose'] = wine_cdc.sugar_dose.name

            if appellation_zone:
                admin_zone = appellation_zone.admin_zones.all().first()
                country = admin_zone.countries.all().first()
                appellation = wine_cdc.appellation
                if admin_zone:
                    viticulture = admin_zone.viticulture_zone.all().first()
                    if viticulture:
                        response['viticulture_zone'] = viticulture.name
                    if admin_zone.countries.all().first():
                        response['country'] = country.name
                    if appellation.label:
                        response['label'] = wine_cdc.appellation.label
            response_status = status.HTTP_200_OK
        return Response(response, response_status)

    @action(methods=['GET'], detail=False, url_path='appellation_information/(?P<pk>[^/.]+)')
    def get_appellation_information(self, request, pk):
        if not pk:
            return Response({'error': 'Please add id'}, status=status.HTTP_400_BAD_REQUEST)
        wine_cdc, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"Please verify the parameter. wine_id is incorrect. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no wine_cdc with this id ({pk})"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            appellation = wine_cdc.appellation
            if not appellation:
                return Response({"error": f"The identifier provided is not linked to any appellation. Provided = {pk}"}, status.HTTP_404_NOT_FOUND)
            appellation_colours = appellation.appellation_colour.all()
            response = {
                'percent_colours': [],
                'grape': [],
                'volume_production': '',
                'air': '',
            }
            if appellation_colours:
                colours = []
                for colour in appellation_colours:
                    colours.append(
                        {
                            "percentage": colour.percentage,
                            "color_authorization": colour.color_authorization
                        },
                    )
                response['percent_colours'] = colours
            grape_assembles = wine_cdc.assemble.grape_assemble.all().select_related('grape')
            if grape_assembles:
                grapes = []
                for grape_assemble in grape_assembles:
                    grapes.append({
                        "type": grape_assemble.grape.type_variety,
                        "grape": grape_assemble.grape.name
                    })
                response['grape'] = grapes
            response['volume_production'] = appellation.volume_production
            if appellation.zone_appelation:
                response['air'] = appellation.zone_appelation.air
            response_status = status.HTTP_200_OK
        return Response(response, response_status)
