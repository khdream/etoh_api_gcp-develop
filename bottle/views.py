
from client.models import Client
from client.serializers import ClientSeriazer
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from bottle.models import (Bottle, BottlePhoto, NoteGuide, Price, Range, Stock,
                           StockList,Warehouse, WineBottle,
                            WineMaker, WineMakerProfile )
from bottle.serializers import (BottlePhotoSerializer,
                                BottlePriceSerializer, BottleSerializer,
                                NoteGuideSerializer, RangeSerializer,
                                 StockListSerializer,
                                StockSeriazer, 
                                WarehouseSeriazer, WineBottleSerializer,
                                WineMakerProfileSerializer,
                                WineMakerSerializer)


class RangeViewSet(ModelViewSet):
    serializer_class = RangeSerializer
    queryset = Range.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)

class BottleViewSet(ModelViewSet):
    serializer_class = BottleSerializer
    queryset = Bottle.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)

class BottlePriceViewSet(ModelViewSet):
    serializer_class = BottlePriceSerializer
    queryset = Price.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)

class WineBottleViewSet(ModelViewSet):
    serializer_class = WineBottleSerializer
    queryset = WineBottle.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class WineMakerViewSet(ModelViewSet):
    serializer_class = WineMakerSerializer
    queryset = WineMaker.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class WineMakerProfileViewSet(ModelViewSet):
    serializer_class = WineMakerProfileSerializer
    queryset = WineMakerProfile.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)





class NoteGuideViewSet(ModelViewSet):
    serializer_class = NoteGuideSerializer
    queryset = NoteGuide.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class BottlePhotoViewSet(ModelViewSet):
    serializer_class = BottlePhotoSerializer
    queryset = BottlePhoto.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)
   

class StockListViewSet(ModelViewSet):
    serializer_class = StockListSerializer
    queryset = StockList.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)



class WareHouseViewSet(ModelViewSet):
    serializer_class = WarehouseSeriazer
    queryset = Warehouse.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class StockViewSet(ModelViewSet):
    serializer_class = StockSeriazer
    queryset = Stock.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class StocklistViewsSet(ModelViewSet):
    serializer_class = StockListSerializer
    queryset = StockList.objects.all().select_related('bottle', 'scale')

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

    @action(methods=['GET'], detail=False, url_path='filter')
    def get_stock_by_params(self, request):
        if not request.query_params:
            return Response({'error': "Please add something to filter "}, status=status.HTTP_400_BAD_REQUEST)
        query = Q()
        response = []
        for key, value in request.query_params.items():
            field = {key: value}
            query &= Q(**field)
            try:
                queryset = self.queryset.filter(query)
            except ValueError:
                return Response(
                    {
                        "message": f"An error happened, please verify values provided. Details : ValueError: invalid literal for int() with base 10: '{key} = {value}'"
                    },
                    status.HTTP_400_BAD_REQUEST
                )
        if queryset:
            for stock in queryset:
                response.append(self.serializer_class(stock).data)
        else:
            return Response({"message": f"There is no stocklist with this parameters"}, status.HTTP_404_NOT_FOUND)
        return Response(response)

    @action(methods=['GET'], detail=False, url_path='info/(?P<pk>[^/.]+)')
    def get_stock_info(self, request, pk):
        if not pk:
            return Response({'error': "Please add id "}, status=status.HTTP_400_BAD_REQUEST)
        stocklist, rstatus = self.get_object(pk)

        if rstatus == 400:
            response = {
                "message": f"Please verify the parameter. Id_stocklist is incorrect. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "message": f"There is no stocklist with this id. Provided = {pk}"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            response = {}
            response['info_client'] = self.serializer_class(stocklist).data

            bottle = stocklist.bottle
            if not bottle:
                return Response({'message': 'This stocklist has no bottle '}, status=status.HTTP_404_NOT_FOUND)
            wine_bottle = bottle.wine_bottle
            if not wine_bottle:
                return Response({'message': f'The bottle {bottle} has no wine bottle '}, status=status.HTTP_404_NOT_FOUND)
            wine_profile = wine_bottle.wine_profile_cdc
            wine_cdc = ''
            if wine_profile:
                wine_cdc = wine_profile.wine_cdc.all().first()
            appellation = ''
            colour = ''
            type = ''
            vintage_quality = ''
            vintage_apogee = ''
            vintage_year = ''
            certification = wine_bottle.certification
            notation = []
            notes = wine_bottle.note_guides.all()
            acidity_taste = ''
            alcohol_taste = ''
            body_taste = ''
            aroma_complexity = ''
            aroma_intensity = ''
            aroma_length = ''
            general_note = ''
            robe_description = ''
            fruity_note = ''
            acidity_note = ''
            body_note = ''
            intensity_note = ''
            temperature = ''
            opening_time = ''
            robe_colour = ''
            type_aging = ''

            if notes:
                for note in notes:
                    notation.append(
                        {
                            "guide": note.guide,
                            "note": note.note
                        }
                    )

            assemble = []
            if wine_cdc:
                appellation = wine_cdc.appellation.name
                if wine_cdc.assemble:
                    for grape_assemble in wine_cdc.assemble.grape_assemble.all():
                        assemble.append({
                            'grape': grape_assemble.grape.name,
                            'percentage': grape_assemble.percentage,
                        })
                vintage = wine_cdc.vintages.all().first()
                if vintage:
                    vintage_apogee = vintage.apogee
                    vintage_quality = vintage.quality
                    vintage_year = vintage.year
                colour = wine_cdc.colour
                type = wine_cdc.type

            if wine_profile:
                acidity_taste = wine_profile.acidity_taste
                alcohol_taste = wine_profile.alcohol_taste
                body_taste = wine_profile.body_taste
                aroma_complexity = wine_profile.aroma_complexity
                aroma_intensity = wine_profile.aroma_intensity
                aroma_length = wine_profile.aroma_length
                general_note = wine_profile.general_note
                robe_description = wine_profile.robe_description
                fruity_note = wine_profile.fruity_note
                acidity_note = wine_profile.acidity_note
                body_note = wine_profile.body_note
                intensity_note = wine_profile.intensity_note
                temperature = wine_profile.temperature
                opening_time = wine_profile.opening_time
                robe = wine_profile.robe
                if robe:
                    robe_colour = robe.name_colour
                aging = wine_profile.aging
                if aging:
                    type_aging = aging.type_aging
            response['wine_info'] = {
                'bottle_id': bottle.id,
                'appellation': appellation,
                'colour': colour,
                'type': type,
                'vintage_apogee': vintage_apogee,
                'vintage_quality': vintage_quality,
                'vintage': vintage_year,
                'certification': certification,
                'notation': notation,
                'aroma_complxity': aroma_complexity,
                'aroma_intensity': aroma_intensity,
                'arome_length': aroma_length,
                'acidity_taste': acidity_taste,
                'alcohol_taste': alcohol_taste,
                'body_taste': body_taste,
                'acidity_note': acidity_note,
                'body_note': body_note,
                'fruity_note': fruity_note,
                'intensity_note': intensity_note,
                'general_note': general_note,
                'robe_colour': robe_colour,
                'robe_description': robe_description,
                'temperature': temperature,
                'opening_time': opening_time,
                'type_aging': type_aging,
            }
            response_status = status.HTTP_200_OK
        return Response(response, response_status)

    @action(methods=['GET'], detail=False, url_path='provinum/info/(?P<pk>[^/.]+)')
    def get_stock_wine_info(self, request, pk):
        if not pk:
            return Response({'error': "Please add id "}, status=status.HTTP_400_BAD_REQUEST)
        stocklist, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "message": f"Please verify the parameter. Id_stocklist is incorrect. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "message": f"There is no stocklist with this id. Provided = {pk}"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            bottle = stocklist.bottle
            wine_bottle = bottle.wine_bottle
            wine_profile = wine_bottle.wine_profile_cdc
            wine_cdc = ''
            if wine_profile:
                wine_cdc = wine_profile.wine_cdc.all().first()
            notes = ''
            certification = ''
            if wine_bottle:
                notes = wine_bottle.note_guides.all()
                certification = wine_bottle.certification
            climat = ''
            type = ''
            vintage_quality = ''
            vintage_apogee = ''
            vintage_year = ''
            notation = []
            acidity_taste = ''
            alcohol_taste = ''
            body_taste = ''
            aroma_complexity = ''
            aroma_intensity = ''
            aroma_length = ''
            general_note = ''
            robe_description = ''
            fruity_note = ''
            acidity_note = ''
            body_note = ''
            intensity_note = ''
            temperature = ''
            opening_time = ''
            robe_colour = ''
            type_aging = ''

            if notes:
                for note in notes:
                    notation.append(
                        {
                            "guide": note.guide,
                            "note": note.note
                        }
                    )

            assemble = []
            if wine_cdc:
                if wine_cdc.assemble:
                    for grape_assemble in wine_cdc.assemble.grape_assemble.all():
                        assemble.append({
                            'grape': grape_assemble.grape.name,
                            'percentage': grape_assemble.percentage,
                        })
                vintage = wine_cdc.vintages.all().first()
                if vintage:
                    vintage_apogee = vintage.apogee
                    vintage_apogee_start = vintage.start_apogee
                    vintage_apogee_end = vintage.end_apogee
                    vintage_quality = vintage.quality
                    vintage_year = vintage.year
                type = wine_cdc.type

                if wine_cdc.appellation.zone_appelation:
                    climat = wine_cdc.appellation.zone_appelation.climat

            if wine_profile:
                acidity_taste = wine_profile.acidity_taste
                alcohol_taste = wine_profile.alcohol_taste
                body_taste = wine_profile.body_taste
                aroma_complexity = wine_profile.aroma_complexity
                aroma_intensity = wine_profile.aroma_intensity
                aroma_length = wine_profile.aroma_length
                general_note = wine_profile.general_note
                robe_description = wine_profile.robe_description
                fruity_note = wine_profile.fruity_note
                acidity_note = wine_profile.acidity_note
                body_note = wine_profile.body_note
                intensity_note = wine_profile.intensity_note
                temperature = wine_profile.temperature
                opening_time = wine_profile.opening_time
                robe = wine_profile.robe
                if robe:
                    robe_colour = robe.name_colour
                aging = wine_profile.aging
                if aging:
                    type_aging = aging.type_aging
            response = {
                'wine_name': stocklist.wine_name,
                'country': stocklist.country,
                'region': stocklist.region,
                'subregion': stocklist.subregion,
                'appellation': stocklist.appellation,
                'label': stocklist.label,
                'grape_assemble': assemble,
                'colour': stocklist.colour,
                'type': stocklist.type,
                'vintage': stocklist.vintage,
                'winemaker': stocklist.winemaker,
                'certification': stocklist.certification,
                'volume': stocklist.volume,
                'weight': stocklist.weight,
                'alcohol': stocklist.alcohol,
                'ranking': stocklist.ranking,
                'note': stocklist.note,
                'image': stocklist.image,
                'price_pre_taxe': stocklist.price_pre_taxe,
                'vat': stocklist.vat,
                'price_with_taxe': stocklist.price_with_taxe,
                'status': stocklist.status,
                'currency': stocklist.currency,
                'bottle_id': stocklist.bottle.id,
                'sku': stocklist.sku,
                'type': type,
                'vintage_apogee': vintage_apogee,
                'vintage_apogee_start': vintage_apogee_start,
                'vintage_apogee_end': vintage_apogee_end,
                'vintage_quality': vintage_quality,
                'vintage': vintage_year,
                'certification': certification,
                'notation': notation,
                'aroma_complxity': aroma_complexity,
                'aroma_intensity': aroma_intensity,
                'arome_length': aroma_length,
                'acidity_taste': acidity_taste,
                'alcohol_taste': alcohol_taste,
                'body_taste': body_taste,
                'acidity_note': acidity_note,
                'body_note': body_note,
                'fruity_note': fruity_note,
                'intensity_note': intensity_note,
                'general_note': general_note,
                'robe_colour': robe_colour,
                'robe_description': robe_description,
                'temperature': temperature,
                'opening_time': opening_time,
                'type_aging': type_aging,
            }

            response['climat'] = climat

            response_status = status.HTTP_200_OK
        return Response(response, response_status)


class CustomerViewSet(ModelViewSet):
    serializer_class = ClientSeriazer
    queryset = Client.objects.all().prefetch_related('scales', 'commands')

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

    @action(methods=['GET'], detail=False, url_path='sommelier/(?P<customer_id>[^/.]+)/(?P<date_min>[^/.]+)')
    def get_stock_clint_by_date(self, request, customer_id, date_min):
        if not customer_id:
            return Response({'error': "Please add id "}, status=status.HTTP_400_BAD_REQUEST)
        client, rstatus = self.get_object(customer_id)
        if rstatus == 400:
            response = {
                "message": f"Please verify the parameter. Customer id  is incorrect. Provided = { customer_id }"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "message": f"There is no Customer with this id. Provided = { customer_id }"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            client = self.queryset.filter(
                id=customer_id, commands__date__gte=date_min).first()
            if not client:
                response = {
                    "message": f"There is no Customer with this date. Provided = { date_min }"
                }
                response_status = status.HTTP_404_NOT_FOUND
                return Response(response, response_status)

            stocklists = client.scales.all().first().stocklists.all()
            results = []
            for stocklist in stocklists:
                bottle = stocklist.bottle
                if not bottle:
                    continue
                if bottle.wine_bottle:
                    wine_bottle = bottle.wine_bottle
                    wine_profile = wine_bottle.wine_profile_cdc
                    certification = wine_bottle.certification
                    notes = wine_bottle.note_guides.all()
                    if wine_profile:
                        aromas = wine_profile.aromas.all()
                        wine_cdc = wine_profile.wine_cdc.all().first()

                type = ''
                vintage_quality = ''
                vintage_apogee = ''
                vintage_year = ''
                notation = []
                acidity_taste = ''
                alcohol_taste = ''
                body_taste = ''
                aroma_complexity = ''
                aroma_intensity = ''
                aroma_length = ''
                general_note = ''
                robe_description = ''
                fruity_note = ''
                acidity_note = ''
                body_note = ''
                intensity_note = ''
                temperature = ''
                opening_time = ''
                robe_colour = ''
                type_aging = ''
                climat = ''
                denomination_wine = ''
                id_zone_admin = 0

                aromes = []
                for arome in aromas:
                    aromes.append({
                        "name": arome.name,
                        "category": arome.category,
                    })

                if notes:
                    for note in notes:
                        notation.append(
                            {
                                "guide": note.guide,
                                "note": note.note
                            }
                        )

                assemble = []
                if wine_cdc:
                    if wine_cdc.assemble:
                        for grape_assemble in wine_cdc.assemble.grape_assemble.all():
                            assemble.append({
                                'grape': grape_assemble.grape.name,
                                'percentage': grape_assemble.percentage,
                            })
                    vintage = wine_cdc.vintages.all().first()
                    if vintage:
                        vintage_apogee = vintage.apogee
                        vintage_apogee_start = vintage.start_apogee
                        vintage_apogee_end = vintage.end_apogee
                        vintage_quality = vintage.quality
                        vintage_year = vintage.year
                    type = wine_cdc.type

                    if wine_cdc.appellation.zone_appelation:
                        climat = wine_cdc.appellation.zone_appelation.climat
                        id_zone_admin = wine_cdc.appellation.zone_appelation.admin_zones.all().first().id

                    if wine_cdc.appellation:
                        denomination_wine = wine_cdc.appellation.denomination_wine
                        if denomination_wine:
                            denomination_wine = denomination_wine.name

                if wine_profile:
                    acidity_taste = wine_profile.acidity_taste
                    alcohol_taste = wine_profile.alcohol_taste
                    body_taste = wine_profile.body_taste
                    aroma_complexity = wine_profile.aroma_complexity
                    aroma_intensity = wine_profile.aroma_intensity
                    aroma_length = wine_profile.aroma_length
                    general_note = wine_profile.general_note
                    robe_description = wine_profile.robe_description
                    fruity_note = wine_profile.fruity_note
                    acidity_note = wine_profile.acidity_note
                    body_note = wine_profile.body_note
                    intensity_note = wine_profile.intensity_note
                    temperature = wine_profile.temperature
                    opening_time = wine_profile.opening_time
                    robe = wine_profile.robe
                    if robe:
                        robe_colour = robe.name_colour
                    aging = wine_profile.aging
                    if aging:
                        type_aging = aging.type_aging
                response = {
                    'wine_name': stocklist.wine_name,
                    'country': stocklist.country,
                    'region': stocklist.region,
                    'subregion': stocklist.subregion,
                    'appellation': stocklist.appellation,
                    'label': stocklist.label,
                    'grape_assemble': assemble,
                    'colour': stocklist.colour,
                    'type': stocklist.type,
                    'vintage': stocklist.vintage,
                    'winemaker': stocklist.winemaker,
                    'certification': stocklist.certification,
                    'denomination_wine': denomination_wine or '',
                    'volume': stocklist.volume,
                    'weight': stocklist.weight,
                    'alcohol': stocklist.alcohol,
                    'ranking': stocklist.ranking,
                    'note': stocklist.note,
                    'image': stocklist.image,
                    'price_pre_taxe': stocklist.price_pre_taxe,
                    'vat': stocklist.vat,
                    'price_pre_taxe': stocklist.price_pre_taxe,
                    'status': stocklist.status,
                    'currency': stocklist.currency,
                    'bottle_id': stocklist.bottle.id,
                    'sku': stocklist.sku,
                    'id_zone_admin': id_zone_admin,
                    'climat': climat,
                    'type': type,
                    'vintage_apogee': vintage_apogee,
                    'vintage_apogee_start': vintage_apogee_start,
                    'vintage_apogee_end': vintage_apogee_end,
                    'vintage_quality': vintage_quality,
                    'vintage': vintage_year,
                    'certification': certification,
                    'notation': notation,
                    'aroma_complxity': aroma_complexity,
                    'aroma_intensity': aroma_intensity,
                    'arome_length': aroma_length,
                    'acidity_taste': acidity_taste,
                    'alcohol_taste': alcohol_taste,
                    'body_taste': body_taste,
                    'acidity_note': acidity_note,
                    'body_note': body_note,
                    'fruity_note': fruity_note,
                    'intensity_note': intensity_note,
                    'general_note': general_note,
                    'robe_colour': robe_colour,
                    'robe_description': robe_description,
                    'temperature': temperature,
                    'opening_time': opening_time,
                    'type_aging': type_aging,
                    'aromes': aromas
                }
                results.append(response)
            response = {'results': results}

            response_status = status.HTTP_200_OK
        return Response(response, response_status)

    @action(methods=['GET'], detail=False, url_path='stocklist/(?P<client_id>[^/.]+)')
    def get_stock_wine_info(self, request, client_id):
        if not client_id:
            return Response({'error': "Please add id "}, status=status.HTTP_400_BAD_REQUEST)
        client, rstatus = self.get_object(client_id)
        if rstatus == 400:
            response = {
                "message": f"Please verify the parameter. Customer id  is incorrect. Provided = { client_id }"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "message": f"There is no Customer with this id. Provided = {client_id}"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            stocklists = client.scales.all().first().stocklists.all().values_list('id', flat=True)
            if not stocklists:
                return Response({
                    "message": f"There are any stocklist related to this specific customer. Provided = {client_id}"
                }, status.HTTP_404_NOT_FOUND)
            results = [stock_id for stock_id in stocklists]
            response = {"results": results}

            response_status = status.HTTP_200_OK
        return Response(response, response_status)


class StockListCrudViewSet(ModelViewSet):
    serializer_class = StockListSerializer
    queryset = StockList.objects.all()

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

    @action(methods=['POST'], detail=False, url_path='(?P<scale_id>[^/.]+)/(?P<client_id>[^/.]+)')
    def create_stocklist(self, request, scale_id, client_id):
        if not scale_id:
            return Response({'error': 'Please add scale id'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['scale'] = int(scale_id)
        serializer = self.get_serializer(data=request.data)
        bottle = request.data.get('bottle', 0)
        scale = request.data.get('scale', 0)
        alcohol = request.data.get('alcohol', 0)
        volume = request.data.get('volume', 0.0)
        price_pre_taxe = request.data.get('price_pre_taxe', 0.0)
        price_with_taxe = request.data.get('price_with_taxe', 0.0)
        vat = request.data.get('vat', 0.0)
        integers = [alcohol, scale, bottle]
        floats = [volume, price_pre_taxe, price_with_taxe, vat]
        for integer in integers:
            if not type(integer) is int:
                return Response({
                    'message': "One or more provided parameters needs to be in integer type." +
                    f"Please review them before send the request. More info : invalid literal for int() with base 10: '{ integer }'."}, status.HTTP_400_BAD_REQUEST)
        for fl in floats:
            if not isinstance(fl, float):
                return Response({
                    'message': "One or more provided parameters needs to be in integer type." +
                    f"Please review them before send the request. More info : invalid literal for float() with base 10: '{ fl }'."}, status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        if not pk:
            return Response({"error": "Please verify your data , (missisng id)"}, status=status.HTTP_400_BAD_REQUEST)
        stocklist, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "message": f"Please verify the parameter. Id_stocklist is incorrect. Provided = { pk }"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "message": f"There is no stocklist with this id. Provided = { pk }"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            response = self.serializer_class(stocklist).data
            response_status = status.HTTP_200_OK
        return Response(response, response_status)

    def update(self, request, pk):
        if not pk:
            return Response({"error": "Please verify your data , (missisng id)"}, status=status.HTTP_400_BAD_REQUEST)
        stocklist, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "message": f"Please verify the parameter. Id_stocklist is incorrect. Provided = { pk }"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "message": f"There is no stocklist with this id. Provided = { pk }"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            serializer = self.serializer_class(stocklist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = serializer.data
                response_status = status.HTTP_200_OK
            else:
                response = serializer.errors
                response_status = status.HTTP_400_BAD_REQUEST
        return Response(response, response_status)

    def destroy(self, request, pk):
        if not pk:
            return Response({"error": "Please verify your data , (missisng id)"}, status=status.HTTP_400_BAD_REQUEST)

        stocklist, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "message": f"Please verify the parameter. Id_stocklist is incorrect. Provided = { pk }"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "message": f"There is no stocklist with this id. Provided = { pk }"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            stocklist.delete()
            response = {'message': 'deleted'}
            response_status = status.HTTP_200_OK
        return Response(response, response_status)
