from rest_framework import response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework_swagger import renderers
from rest_framework.views import APIView
from rest_framework.schemas import SchemaGenerator
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import math
import json
import requests
from algoliasearch.search_client import SearchClient
from django.conf import settings
from django.db.models import CharField, TextField
from django.db.models.functions import Lower
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry, Point
from appellation.models import AdminZone, Appellation, AppellationPhoto, AppellationZone, PlotZone, ViticultureZone
from appellation.serializers import (
    AdminZoneSerializer,
    AppellationPhotoSerializer,
    AppellationSerializer,
    AppellationZoneSerializer,
    PlotZoneSerializer,
    ViticultureZoneSerializer
)
from core.models import Country
from core.serializers import CountrySerializer
from productspec.serializers import GrapeSerializer, WineCDCSerializer
from productspec.models import Grape, WineCDC
from bottle.models import WineBottle, WineMaker
from bottle.serializers import WineBottleSerializer,  WineMakerSerializer
from django.core.serializers import serialize
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import Response


client = SearchClient.create(settings.ALGOLIA.get(
    'APPLICATION_ID'), settings.ALGOLIA.get('API_KEY'))
CharField.register_lookup(Lower)
TextField.register_lookup(Lower)


class WSEAutocomplateViewSet(ViewSet):
    serializer_class = AppellationSerializer
    queryset = Appellation.objects.all()

    @action(methods=['GET'], detail=False, url_path='autocomplete/(?P<query>[^/.]+)')
    def autocomplate(self, request, query):
        separator = ' '
        for _, sep in request.query_params.items():
            if sep in query:
                separator = sep.strip()
        words = query.split(separator)

        query_filter = Q()
        for word in words:
            word = word.strip().lower()
            query_filter |= Q(name__lower__icontains=word)
        name_qs = self.queryset.filter(query_filter)
        if len(name_qs) < 3:
            for word in words:
                query_filter |= Q(name_dgc__lower__icontains=word)
        queryset = self.queryset.filter(query_filter)[:3]
        results = {}
        if queryset:
            response_status = status.HTTP_200_OK
            for result in queryset:
                results[result.id] = result.name or result.name_dgc
        else:
            response_status = status.HTTP_404_NOT_FOUND

        response = {
            "input": query,
            "count": len(queryset),
            "results": results
        }
        return Response(response, status=response_status)

    @action(methods=['GET'], detail=False, url_path='appellation_zone/(?P<query>[^/.]+)')
    def autocomplate_appellation_zone(self, request, query):
        try:
            appellation = self.queryset.filter(id=query).first()
        except ValueError:
            words = query.split(' ')
            query_filter = Q()
            for word in words:
                word = word.lower()
                query_filter |= Q(name__lower__istartswith=word)
            appellation = self.queryset.filter(query_filter).first()
            query_filter = Q()
            if not appellation:
                for word in words:
                    word = word.lower()
                    query_filter |= Q(name__lower__icontains=word)
            appellation = self.queryset.filter(query_filter).first()
            if not appellation:
                for word in words:
                    word = word.lower()
                    query_filter |= Q(name_dgc__lower__icontains=word)
            appellation = self.queryset.filter(query_filter).first()
        if appellation:
            response_status = status.HTTP_200_OK
            response = {
                "id": appellation.id,
                "appellation": appellation.name,
                "gdc": appellation.name_dgc,
            }
        else:
            response_status = status.HTTP_404_NOT_FOUND
            response = {
                "error": "No appellations found",
            }
        return Response(response, response_status)


class WSEViticultureZoneViewSet(ViewSet):
    serializer_class = ViticultureZoneSerializer
    queryset = ViticultureZone.objects.all().select_related('zone_admin')

    @action(methods=['GET'], detail=False, url_path='vineyard/autocomplete/(?P<query>[^/.]+)')
    def autocomplete_vineyard(self, request, query):
        source = request.query_params.get('source')
        get_info_from_database = False
        if source in ['true', 'True'] or source is True:
            get_info_from_database = True
        if get_info_from_database:
            lower_query = query.lower()
            vineyards = self.queryset.filter(
                name__lower__istartswith=lower_query, hierarchy__lower='vineyard')
            results = []
            for vineyard in vineyards:
                results.append(self.serializer_class(vineyard).data)
            if results:
                response = {
                    "info": query,
                    "results": results
                }
                response_status = status.HTTP_200_OK
            else:
                response = {
                    "info": query,
                    "message": f"Could not find '{query}' in our database."
                }
                response_status = status.HTTP_404_NOT_FOUND
            return Response(response, response_status)
        else:
            index = client.init_index('ViticultureZone')
            results = index.search(query).get('hits')
            vineyards_ids = [vineyard.get(
                'objectID') for vineyard in results if vineyard.get('hierarchy').lower() == 'vineyard']
            vineyards = self.queryset.filter(id__in=vineyards_ids)
            results = []
            for vineyard in vineyards:
                results.append(self.serializer_class(vineyard).data)
            if results:
                response = {
                    "info": query,
                    "results": results
                }
                response_status = status.HTTP_200_OK
            else:
                response = {
                    "info": query,
                    "message": f"Could not find '{query}' in our database."
                }
                response_status = status.HTTP_404_NOT_FOUND
            return Response(response, response_status)

    @action(methods=['GET'], detail=False, url_path='region/autocomplete/(?P<query>[^/.]+)')
    def autocomplete_region(self, request, query):
        source = request.query_params.get('source')
        get_info_from_database = False
        if source in ['true', 'True'] or source is True:
            get_info_from_database = True
        if get_info_from_database:
            lower_query = query.lower()
            regions = self.queryset.filter(
                name__lower__istartswith=lower_query, hierarchy__lower='region')
            results = []
            for region in regions:
                results.append(self.serializer_class(region).data)
            if results:
                response = {
                    "info": query,
                    "results": results
                }
                response_status = status.HTTP_200_OK
            else:
                response = {
                    "info": query,
                    "message": f"Could not find '{query}' in our database."
                }
                response_status = status.HTTP_404_NOT_FOUND
            return Response(response, response_status)
        else:
            index = client.init_index('ViticultureZone')
            results = index.search(query).get('hits')
            regions_ids = [region.get(
                'objectID') for region in results if region.get('hierarchy').lower() == 'region']
            regions = self.queryset.filter(id__in=regions_ids)
            results = []
            for region in regions:
                results.append(self.serializer_class(region).data)
            if results:
                response = {
                    "info": query,
                    "results": results
                }
                response_status = status.HTTP_200_OK
            else:
                response = {
                    "info": query,
                    "message": f"Could not find '{query}' in our database."
                }
                response_status = status.HTTP_404_NOT_FOUND
            return Response(response, response_status)


class WSEGrapeAutocomplete(ViewSet):
    serializer_class = GrapeSerializer
    queryset = Grape.objects.all().select_related('country')

    @action(methods=['GET'], detail=False, url_path='grape/autocomplete/(?P<query>[^/.]+)')
    def autocomplete_grape(self, request, query):
        source = request.query_params.get('source')
        get_info_from_database = False
        if source in ['true', 'True'] or source is True:
            get_info_from_database = True
        if get_info_from_database:
            lower_query = query.lower()
            grapes = self.queryset.filter(name__lower__istartswith=lower_query)
            results = []
            for grape in grapes:
                results.append(self.serializer_class(grape).data)
            if results:
                response = {
                    "info": query,
                    "results": results
                }
                response_status = status.HTTP_200_OK
            else:
                response = {
                    "info": query,
                    "message": f"Could not find '{query}' in our database."
                }
                response_status = status.HTTP_404_NOT_FOUND
            return Response(response, response_status)
        else:
            index = client.init_index('Grape')
            results = index.search(query).get('hits')
            grape_ids = [grape.get('objectID') for grape in results]
            grapes = self.queryset.filter(id__in=grape_ids)
            results = []
            for grape in grapes:
                results.append(self.serializer_class(grape).data)
            if results:
                response = {
                    "info": query,
                    "results": results
                }
                response_status = status.HTTP_200_OK
            else:
                response = {
                    "info": query,
                    "message": f"Could not find '{query}' in our database."
                }
                response_status = status.HTTP_404_NOT_FOUND
            return Response(response, response_status)


class WSECountryAutocomplete(ViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

    @action(methods=['GET'], detail=False, url_path='country/autocomplete/(?P<query>[^/.]+)')
    def autocomplete_country(self, request, query):
        source = request.query_params.get('source')
        get_info_from_database = False
        if source in ['true', 'True'] or source is True:
            get_info_from_database = True
        if get_info_from_database:
            lower_query = query.lower()
            countries = self.queryset.filter(
                name__lower__istartswith=lower_query)
            results = []
            for country in countries:
                results.append(self.serializer_class(country).data)
            if results:
                response = {
                    "info": query,
                    "results": results
                }
                response_status = status.HTTP_200_OK
            else:
                response = {
                    "info": query,
                    "message": f"Could not find '{query}' in our database."
                }
                response_status = status.HTTP_404_NOT_FOUND
            return Response(response, response_status)
        else:
            index = client.init_index('Country')
            results = index.search(query).get('hits')
            country_ids = [country.get('objectID') for country in results]
            countries = self.queryset.filter(id__in=country_ids)
            results = []
            for country in countries:
                results.append(self.serializer_class(country).data)
            if results:
                response = {
                    "info": query,
                    "results": results
                }
                response_status = status.HTTP_200_OK
            else:
                response = {
                    "info": query,
                    "message": f"Could not find '{query}' in our database."
                }
                response_status = status.HTTP_404_NOT_FOUND
            return Response(response, response_status)


class WSEWineChoosing(ViewSet):
    serializer_class = WineCDCSerializer
    queryset = WineCDC.objects.all().select_related(
        'appellation', 'sugar_dose',  'assemble')

    @action(methods=['GET'], detail=False, url_path='autocomplete/(?P<field>[^/.]+)/(?P<query>[^/.]+)')
    def autocomplate(self, request, field, query):
        source = request.query_params.get('source')
        get_info_from_database = False
        if source in ['true', 'True'] or source is True:
            get_info_from_database = True
        if get_info_from_database:
            if field == 'grape':
                params = {
                    'assemble__grape_assemble__grape__name__lower__icontains': query}
            elif field == 'appellation':
                params = {
                    'appellation__name__lower__icontains': query}
            elif field == 'dgc':
                params = {'appellation__name_dgc__lower__icontains': query}
            elif field == 'denomination_wine':
                params = {'denomination_wine__name__lower__icontains': query}
            else:
                params = {f'{field}__lower__icontains': query}
            queryset = self.queryset.filter(Q(**params))[:3]
            if field == 'grape':
                params = {
                    'assemble__grape_assemble__grape__name__lower__icontains': query}
                results = list(set(queryset.values_list(
                    'assemble__grape_assemble__grape__name', flat=True)))
            elif field == 'appellation':
                params = {
                    'appellation__name__lower__icontains': query}
                results = list(set(queryset.values_list(
                    'appellation__name', flat=True)))
            elif field == 'dgc':
                params = {'appellation__name_dgc__lower__icontains': query}
                results = list(set(queryset.values_list(
                    'appellation__name_dgc', flat=True)))
            elif field == 'denomination_wine':
                params = {'denomination_wine__name__lower__icontains': query}
                results = list(set(queryset.values_list(
                    'denomination_wine__name', flat=True)))
            else:
                params = {f'{field}__lower__icontains': query}
                results = list(set(queryset.values_list(
                    field, flat=True)))
            if queryset:
                response_status = status.HTTP_200_OK
            else:
                response_status = status.HTTP_404_NOT_FOUND
            result = {}
            i = 0
            for res in results:
                result[i] = res
                i += 1
            response = {
                "input": query,
                "count": len(results),
                "results": result
            }
            return Response(response, status=response_status)
        else:
            fields = ['name', 'grape', 'colour', 'appellation',
                      'dgc',  'denomination_wine']
            if not field in fields:
                return Response({
                    "field": field,
                    "search_value": query,
                    "error": "Your field may be wrong"
                }, status.HTTP_400_BAD_REQUEST)
            index = client.init_index('WineCDC')
            if field == 'appellation':
                field = 'appellations'
            elif field == 'denomination_wine':
                field = 'denomination_wines'
            results = index.search(query, {
                'restrictSearchableAttributes': [
                    field
                ],
            }).get('hits')
            if len(results) == 0:
                rstatus = status.HTTP_404_NOT_FOUND
            else:
                rstatus = status.HTTP_200_OK
            names_of_wine = {}
            i = 0
            for result in results:
                names_of_wine[i] = (result.get(field))
                i += 1
            response = {
                "field": field,
                "search_value": query,
                "results": names_of_wine
            }
            return Response(response, rstatus)

    @ action(methods=['GET'], detail=False, url_path='get/wine')
    def get_wine_by_params(self, request):
        source = request.query_params.get('source')
        get_info_from_database = False
        if source in ['true', 'True'] or source is True:
            get_info_from_database = True
        if get_info_from_database:
            query = Q()
            grape_qs = []
            params = {}
            for key, value in request.query_params.items():
                params[key] = value
                items = value.split(',')
                if len(items) > 1:
                    or_query = Q()
                    for item in items:
                        field = {key: item}
                        or_query |= Q(**field)

                    query &= or_query
                else:
                    if key in ['appellation', 'sugar_dose']:
                        key = f'{key}__name__lower__icontains'
                    elif key == 'grape':
                        for wine in self.queryset:
                            has_grape = wine.assemble.grape_asseble.filter(
                                grape__name__lower__icontains=value)
                            if has_grape:
                                grape_qs.append(wine)
                        continue
                    elif key == 'dgc':
                        key = 'appellation__name_dgc__lower__icontains'
                    if type(value) is str:
                        value = value.lower()
                    field = {key: value}
                    query &= Q(**field)

            if query:
                queryset = self.queryset.filter(query)
                qs_ids = queryset.values_list('id', flat=True)
            else:
                queryset = []
                qs_ids = []
            grape_qs = [wine for wine in grape_qs if wine.id not in qs_ids]

            results = []
            for result in queryset:
                appellation = ''
                grape = ''
                denomination_wine = ''
                sugar_dose = ''
                name_dgc = ''
                if result.appellation:
                    appellation = result.appellation.name
                if result.assemble.grape_asseble.all().first().grape:
                    grape = result.assemble.grape_asseble.all().first().grape.name
                if result.denomination_wine:
                    denomination_wine = result.denomination_wine.name
                if result.sugar_dose:
                    sugar_dose = result.sugar_dose.name
                if result.appellation:
                    name_dgc = result.appellation.name_dgc
                results.append(
                    {
                        "Appellation": appellation,
                        "Dgc": name_dgc,
                        "Grape": grape,
                        "Colour": result.colour,
                        "Denomination Wine": denomination_wine,
                        "Type": result.type,
                        "Sugar Dose": sugar_dose
                    },
                )
            for result in grape_qs:
                appellation = ''
                grape = ''
                denomination_wine = ''
                sugar_dose = ''
                name_dgc = ''
                if result.appellation:
                    appellation = result.appellation.name
                if result.assemble.grape_asseble.all().first().grape:
                    grape = result.assemble.grape_asseble.all().first().grape.name
                if result.denomination_wine:
                    denomination_wine = result.denomination_wine.name
                if result.sugar_dose:
                    sugar_dose = result.sugar_dose.name
                if result.appellation:
                    name_dgc = result.appellation.name_dgc
                results.append(
                    {
                        "Appellation": appellation,
                        "Dgc": name_dgc,
                        "Grape": grape,
                        "Colour": result.colour,
                        "Denomination Wine": denomination_wine,
                        "Type": result.type,
                        "Sugar Dose": sugar_dose
                    },
                )
            if results:
                response_status = status.HTTP_200_OK
            else:
                response_status = status.HTTP_404_NOT_FOUND
            response = {
                "infos": {
                    "Appellation": params.get('appellation', ''),
                    "Dgc": params.get('dgc', ''),
                    "Grape": params.get('grape', ''),
                    "Colour": params.get('colour', ''),
                    "Denomination Wine": params.get('denomination_wine', ''),
                    "Type": params.get('type', ''),
                    "Sugar Dose": params.get('sugar_dose', ''),
                },
                "result": results
            }
            return Response(response, response_status)
        else:
            params = {}
            index = client.init_index('WineCDC')
            index.set_settings({
                'attributesForFaceting': [
                    'grape',
                    'name',
                    'appellations',
                    'dgc',
                    'type',
                    'colour',
                    'sugar_dose',
                    'denomination_wines',
                ]
            })
            facet_filters = []
            for key, value in request.query_params.items():
                params[key] = value
                items = value.split(',')
                if len(items) > 1:
                    or_query = []
                    for item in items:
                        or_query.append(f'{key}:{item}')
                    facet_filters.append(or_query)
                else:
                    if key == 'appellation':
                        facet_filters.append(f'appellations:{value}')
                    elif key == 'sugar_dose':
                        facet_filters.append(f'sugar_doses:{value}')
                    elif key == 'denomination_wine':
                        facet_filters.append(f'denomination_wines:{value}')
                    else:
                        facet_filters.append(f'{key}:{value}')
            results = index.search('', {
                "facetFilters": facet_filters
            }).get('hits')
            result = []
            for instance in results:

                result.append(
                    {
                        "Appellation": instance.get('appellations', ''),
                        "Dgc": instance.get('dgc', ''),
                        "Grape": instance.get('grape', ''),
                        "Colour": instance.get('colour', ''),
                        "Denomination Wine": instance.get('denomination_wines', ''),
                        "Type": instance.get('type', ''),
                        "Sugar Dose": instance.get('sugar_doses', '')
                    },
                )
            if results:
                response_status = status.HTTP_200_OK
            else:
                response_status = status.HTTP_404_NOT_FOUND
            response = {
                "infos": {
                    "Appellation": params.get('appellation', ''),
                    "Dgc": params.get('dgc', ''),
                    "Grape": params.get('grape', ''),
                    "Colour": params.get('colour', ''),
                    "Denomination Wine": params.get('denomination_wine', ''),
                    "Type": params.get('type', ''),
                    "Sugar Dose": params.get('sugar_dose', ''),
                },
                "result": result
            }
            return Response(response, response_status)

    @ action(methods=['GET'], detail=False, url_path='get/wine_id')
    def get_wine_by_id(self, request):
        source = request.query_params.get('source')
        get_info_from_database = False
        if source in ['true', 'True'] or source is True:
            get_info_from_database = True
        if get_info_from_database:
            query = Q()
            grape_qs = []
            params = {}
            for key, value in request.query_params.items():
                params[key] = value
                items = value.split(',')
                if len(items) > 1:
                    or_query = Q()
                    for item in items:
                        field = {key: item}
                        or_query |= Q(**field)

                    query &= or_query
                else:
                    if key in ['appellation', 'sugar_dose', 'denomination_wine']:
                        key = f'{key}__name__icontains'
                    elif key == 'grape':
                        for wine in self.queryset:
                            has_grape = wine.assemble.grape_assemble.filter(
                                grape__name__icontains=value)
                            if has_grape:
                                grape_qs.append(wine)
                        continue
                    elif key == 'dgc':
                        key = 'appellation__name_dgc__icontains'
                    field = {key: value}
                    query &= Q(**field)
            if query:
                queryset = self.queryset.filter(query)
                qs_ids = list(queryset.values_list('id', flat=True))
            else:
                queryset = []
                qs_ids = []
            grape_qs_ids = [
                wine.id for wine in grape_qs if wine.id not in qs_ids]
            results = grape_qs_ids + qs_ids
            if results:
                response_status = status.HTTP_200_OK
            else:
                response_status = status.HTTP_404_NOT_FOUND
            response = {
                "infos": {
                    "appellation": params.get('appellation', ''),
                    "dgc": params.get('dgc', ''),
                    "grape": params.get('grape', ''),
                    "coulour": params.get('coulour', ''),
                    "denomination_wine": params.get('denomination_wine', ''),
                    "type": params.get('type', '')
                },
                "results": results,
            }
            return Response(response)
        else:
            index = client.init_index('WineCDC')
            params = {}
            index.set_settings({
                'attributesForFaceting': [
                    'grape',
                    'name',
                    'appellations',
                    'dgc',
                    'type',
                    'colour',
                    'sugar_dose',
                    'denomination_wines',
                ]
            })
            facet_filters = []
            for key, value in request.query_params.items():
                params[key] = value
                items = value.split(',')
                if len(items) > 1:
                    or_query = []
                    for item in items:
                        or_query.append(f'{key}:{item}')
                    facet_filters.append(or_query)
                else:
                    if key == 'appellation':
                        facet_filters.append(f'appellations:{value}')
                    elif key == 'sugar_dose':
                        facet_filters.append(f'sugar_doses:{value}')
                    elif key == 'denomination_wine':
                        facet_filters.append(f'denomination_wines:{value}')
                    else:
                        facet_filters.append(f'{key}:{value}')
            results = index.search('', {
                "facetFilters": facet_filters
            }).get('hits')
            result = []
            for instance in results:

                result.append(
                    int(instance.get('objectID'))
                )
            if results:
                response_status = status.HTTP_200_OK
            else:
                response_status = status.HTTP_404_NOT_FOUND
            response = {
                "infos": {
                    "Appellation": params.get('appellation', ''),
                    "Dgc": params.get('dgc', ''),
                    "Grape": params.get('grape', ''),
                    "Colour": params.get('colour', ''),
                    "Denomination Wine": params.get('denomination_wine', ''),
                    "Type": params.get('type', ''),
                    "Sugar Dose": params.get('sugar_dose', ''),
                },
                "result": result
            }
            return Response(response, response_status)

    @ action(methods=['GET'], detail=False, url_path='corrector/(?P<field>[^/.]+)/(?P<query>[^/.]+)?')
    def corrector(self, request, field, query):
        fields = ['name', 'grape', 'colour', 'appellation',
                  'dgc',  'denomination_wine', 'name_origin_alphabet_origin' , 'name_origin_alphabet_latin' , 'name_english_alphabet_latin']
        proximity = int(request.query_params.get('proximity', 1))
        hits_per_page = int(request.query_params.get('hits_per_page', 10))
        all_distinct = request.query_params.get('all_distinct', False)
        if not field in fields:
            return Response({
                "field": field,
                "search_value": query,
                "hit_per_page": hits_per_page,
                "proximity": proximity,
                "error": "Your field may be wrong"
            }, status.HTTP_400_BAD_REQUEST)
        index = client.init_index('WineCDC')
        if all_distinct:
            index.set_settings({
                'typoTolerance': True,
                'minProximity': proximity,
                'hitsPerPage': hits_per_page,
                'attributeForDistinct': 'name',
            })
        else:
            index.set_settings({
                'typoTolerance': True,
                'minProximity': proximity,
                'hitsPerPage': hits_per_page,
            })
        if field == 'appellation':
            field = 'appellations'
        elif field == 'denomination_wine':
            field = 'denomination_wines'
        results = index.search(query, {
            'restrictSearchableAttributes': [
                field
            ],
            'distinct': 1                       # distinct not working without attributeForDistinct
        }).get('hits')
        if len(results) == 0:
            rstatus = status.HTTP_404_NOT_FOUND
        else:
            rstatus = status.HTTP_200_OK
        names_of_wine = []
        for result in results:
            names_of_wine.append(result.get('name'))
        response = {
            "field": field,
            "search_value": query,
            "hit_per_page": hits_per_page,
            "proximity": proximity,
            "all_distinct": all_distinct,
            "hits": names_of_wine
        }
        return Response(response, rstatus)

    @ action(methods=['GET'], detail=False, url_path='geovinum/(?P<field>[^/.]+)/(?P<query>[^/.]+)?')
    def geovinum(self, request, field, query):
        fields = ['name', 'grape', 'colour', 'appellation',
                  'dgc',  'denomination_wine']
        proximity = int(request.query_params.get('proximity', 1))
        hits_per_page = int(request.query_params.get('hits_per_page', 10))
        all_distinct = request.query_params.get('all_distinct', False)

        if not field in fields:
            return Response({
                "field": field,
                "search_value": query,
                "hit_per_page": hits_per_page,
                "proximity": proximity,
                "error": "Your field may be wrong"
            }, status.HTTP_400_BAD_REQUEST)
        index = client.init_index('WineCDC')
        if all_distinct:
            index.set_settings({
                'typoTolerance': True,
                'minProximity': proximity,
                'hitsPerPage': hits_per_page,
                'attributeForDistinct': 'appellations',
            })
        else:
            index.set_settings({
                'typoTolerance': True,
                'minProximity': proximity,
                'hitsPerPage': hits_per_page,
            })
        if field == 'appellation':
            field = 'appellations'
        elif field == 'denomination_wine':
            field = 'denomination_wines'
        results = index.search(query, {
            'restrictSearchableAttributes': [
                field
            ],
            'distinct': 1
        }).get('hits')
        if len(results) == 0:
            rstatus = status.HTTP_404_NOT_FOUND
        else:
            rstatus = status.HTTP_200_OK
        appellatin_information = []
        for result in results:
            appellatin_information.append({
                'id_appellation': result.get('appellation_id'),
                'appellation': result.get('appellations'),
                'dgc': result.get('dgc'),
                'zone_appellation_id': result.get('zone_appellation_id'),
            }
            )
        response = {
            "field": field,
            "search_value": query,
            "hit_per_page": hits_per_page,
            "proximity": proximity,
            "all_distinct": all_distinct,
            "hits": appellatin_information
        }
        return Response(response, rstatus)

    @ action(methods=['GET'], detail=False, url_path='cleaner/(?P<query>[^/.]+)?')
    def cleaner(self, request, query):
        proximity = int(request.query_params.get('proximity', 1))
        hits_per_page = int(request.query_params.get('hits_per_page', 3))

        index = client.init_index('WineCDC')
        index.set_settings({
            'typoTolerance': True,
            'minProximity': proximity,
            'hitsPerPage': hits_per_page,
        })
        results = index.search(query).get('hits')
        if len(results) == 0:
            rstatus = status.HTTP_404_NOT_FOUND
        else:
            rstatus = status.HTTP_200_OK
        names_of_wine = []
        for result in results:
            names_of_wine.append({
                'name': result.get('name'),
                'grape': result.get('grape'),
                'colour': result.get('colour'),
                'id_appellation': result.get('appellation_id'),
                'appellation': result.get('appellations'),
                'zone_appellation_id': result.get('zone_appellation_id'),
                'dgc': result.get('dgc'),
                'type': result.get('type'),
                'sugar_dose': result.get('sugar_dose'),
                'denomination_wine': result.get('denomination_wines'),
            }
            )
        response = {
            "search_value": query,
            "hit_per_page": hits_per_page,
            "proximity": proximity,
            "hits": names_of_wine
        }
        return Response(response, rstatus)


class WinemakerViewSet(ModelViewSet):
    serializer_class = WineMakerSerializer
    queryset = WineMaker.objects.all()

    def get_object(self, **kwargs):
        try:
            winemaker = self.queryset.filter(id=kwargs.get('pk')).first()
        except ValueError:
            winemaker = self.queryset.filter(name=kwargs.get('pk')).first()
        return winemaker

    @ action(methods=['GET'], detail=False, url_path='autocomplete/(?P<query>[^/.]+)')
    def autocomplate(self, request, query):
        source = request.query_params.get('source')
        get_info_from_database = False
        if source in ['true', 'True'] or source is True:
            get_info_from_database = True
        if get_info_from_database:
            lower_query = query.lower()
            winemakers = self.queryset.filter(
                name__lower__istartswith=lower_query)
            results = []
            for winemaker in winemakers:
                results.append(self.serializer_class(winemaker).data)
            if results:
                response = {
                    "info": query,
                    "results": results
                }
                response_status = status.HTTP_200_OK
            else:
                response = {
                    "info": query,
                    "message": f"Could not find '{query}' in our database."
                }
                response_status = status.HTTP_404_NOT_FOUND
            return Response(response, response_status)
        else:
            index = client.init_index('WineMaker')
            index.search_rules('', {'anchoring': 'startsWith'})

            result = index.search(query).get('hits')
            results = []
            for winemaker_result in result:
                winemaker = self.queryset.filter(
                    id=int(winemaker_result.get('objectID'))).first()
                results.append(self.serializer_class(winemaker).data)
            if results:
                response = {
                    "info": query,
                    "results": results
                }
                response_status = status.HTTP_200_OK
            else:
                response = {
                    "info": query,
                    "message": f"Could not find '{query}' in our database."
                }
                response_status = status.HTTP_404_NOT_FOUND
            return Response(response, response_status)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(
                {
                    "infos": request.data,
                    "result": serializer.data
                }, status=status.HTTP_201_CREATED)
        else:
            response = Response({
                "infos": request.data,
                "result": f"Another winemaker has this name. Please choose another name. [Requested : '{request.data.get('name')}']"
            }, status=status.HTTP_409_CONFLICT)
        return response

    def retrieve(self, request, *args, **kwargs):
        winemaker = self.get_object(**kwargs)

        if winemaker:
            serializer = self.serializer_class(winemaker)
            response = Response(serializer.data)
        else:
            response = Response({"error": "not found"},
                                status=status.HTTP_404_NOT_FOUND)
        return response

    def update(self, request, **kwargs):
        winemaker = self.get_object(**kwargs)
        if winemaker:
            serializer = self.get_serializer(
                winemaker, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

            response = Response(
                {
                    "infos": request.data,
                    "result": serializer.data
                })
        else:
            response = Response(
                {
                    "infos": request.data,
                    "result": f"Another winemaker has this name. Please choose another name. [Requested : '{request.data.get('name')}']"
                }, status=status.HTTP_404_NOT_FOUND)

        return response

    def destroy(self, request, **kwargs):
        winemaker = self.get_object(**kwargs)
        if winemaker:
            response = Response(
                {
                    "infos": {
                        "id": winemaker.id,
                        "name": winemaker.name
                    },
                    "result": True
                })
            winemaker.delete()

        else:
            response = Response(
                {
                    "error": f"The winemaker {kwargs.get('pk')} does not excists",
                    "result": False
                }, status=status.HTTP_404_NOT_FOUND)
        return response


class DescriptionViewSet(ViewSet):
    serializer_class = WineBottleSerializer
    queryset = WineBottle.objects.all().select_related(
        'vintage', 'winemaker')

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

    @ action(methods=['GET'], detail=False, url_path='tasting/(?P<pk>[^/.]+)')
    def get_description_tasting(self, request, pk):
        wine_bottle, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"An error happened. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": "There is no wine bottle corrprint(esponding to value. Provided = 0"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            response = {
                "comment_degustation": wine_bottle.comment_degustation
            }
            response_status = status.HTTP_200_OK

        return Response(response, response_status)

    @ action(methods=['GET'], detail=False, url_path='winemaking/(?P<pk>[^/.]+)')
    def get_description_winemaking(self, request, pk):
        wine_bottle, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"An error happened. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": "There is no wine bottle corresponding to value. Provided = 0"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            response = {
                "comment_vinification": wine_bottle.comment_vinification
            }
            response_status = status.HTTP_200_OK

        return Response(response, response_status)

    @ action(methods=['GET'], detail=False, url_path='viticulture/(?P<pk>[^/.]+)')
    def get_description_viticulture(self, request, pk):
        wine_bottle, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"An error happened. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no wine bottle corresponding to value. Provided = {pk}"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            response = {
                "comment_viticulture": wine_bottle.comment_viticulture
            }
            response_status = status.HTTP_200_OK

        return Response(response, response_status)

    @ action(methods=['GET'], detail=False, url_path='vintage/(?P<pk>[^/.]+)')
    def get_description_vintage(self, request, pk):
        wine_bottle, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"An error happened. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no wine bottle corresponding to value. Provided = {pk}"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            if wine_bottle.vintage:
                response = {
                    "comment_vintage": wine_bottle.vintage.comment_vintage
                }
                response_status = status.HTTP_200_OK

        return Response(response, response_status)


class WinemakerDescriptionViewSet(ModelViewSet):
    serializer_class = WineMakerSerializer
    queryset = WineMaker.objects.all()

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

    @ action(methods=['GET'], detail=False, url_path='winemaker/(?P<pk>[^/.]+)')
    def get_description_winemaker(self, request, pk):
        winemaker, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"An error happened. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no wine maker corresponding to value. Provided = {pk}"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            response = {
                "comment_winemaker": winemaker.comment_winemaker
            }
            response_status = status.HTTP_200_OK

        return Response(response, response_status)


class WineCDCDescriptionViewSet(ModelViewSet):
    serializer_class = WineCDCSerializer
    queryset = WineCDC.objects.all()

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

    @ action(methods=['GET'], detail=False, url_path='wine/(?P<pk>[^/.]+)')
    def get_description_wine(self, request, pk):
        wine_cdc, rstatus = self.get_object(pk)
        if rstatus == 400:
            response = {
                "error": f"An error happened. Provided = {pk}"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif rstatus == 404:
            response = {
                "error": f"There is no wine bottle corresponding to value. Provided = {pk}"
            }
            response_status = status.HTTP_404_NOT_FOUND
        else:
            response = {
                "comment_descritpion": wine_cdc.comment_descritpion
            }
            response_status = status.HTTP_200_OK

        return Response(response, response_status)


class GeoWinemakersViewSet(ModelViewSet):
    serializer_class = WineMakerSerializer
    queryset = WineMaker.objects.all().select_related('country')

    def list(self, request):
        winemakers_with_location = self.queryset.filter(
            gps_location__isnull=False)
        if not winemakers_with_location:
            return Response({
                'message': f"There is no winemakers with locations"
            }, status.HTTP_404_NOT_FOUND)
        response = json.loads(serialize('geojson', winemakers_with_location,
                                        geometry_field='gps_location',
                                        fields=(
                                            'name',
                                            'viticulture', 'siren', 'date_creation',
                                            'address', 'country', 'type_winemaker',
                                            'comment_winemaker',)))

        return Response(response)


class GeoAppellationViewSet(ModelViewSet):
    serializer_class = AppellationZoneSerializer
    queryset = AppellationZone.objects.all()
    multiple_lookup_fields = ['name', 'id']

    def get_object(self, id_or_name):
        try:
            appellation = self.queryset.filter(id=id_or_name).first()
        except ValueError:
            appellation = self.queryset.filter(name=id_or_name).first()
        return appellation

    @ action(methods=['GET'], detail=False, url_path='geocoding/(?P<address>[^/.]+)')
    def get_description_wine(self, request, address):
        url = f'https://nominatim.openstreetmap.org/search/{ address }/?format=json'
        responses_for_address = requests.get(url).json()
        if not responses_for_address:
            return Response({
                'message': f"The address provided cannot be found. Please verify the address. Provided = { address }"
            }, status.HTTP_404_NOT_FOUND)
        features = []
        for response_for_address in responses_for_address:
            latitude = response_for_address.get('lat')
            longtitude = response_for_address.get('lon')
            coordinates = [longtitude, latitude]
            display_name = response_for_address.get('display_name')
            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": coordinates
                    },
                    "properties": {
                        "name": display_name
                    }
                }
            )

        response = {
            "type": "FeatureCollection",
            "crs": {
                "type": "name",
                "properties": {
                    "name": "EPSG:4326"
                }
            },
            "features": features
        }
        return Response(response)

    @ action(methods=['GET'], detail=False, url_path='polygon/(?P<id_or_name>[^/.]+)')
    def get_polygon(self, request, id_or_name):
        appellation = self.get_object(id_or_name)
        if not appellation:
            return Response({
                'message': f"Cannot retrieve the polygon associated. Provided = { id_or_name }"
            }, status.HTTP_404_NOT_FOUND)
        response = json.loads(serialize('geojson', [appellation],
                                        geometry_field='geom',
                                        fields=(
            'name',
            'ground', 'subsoil', 'climat',
            'min_elevetion', 'max_elevetion', 'average_elevetion',
            'min_precipitation', 'max_precipitation', 'average_precipitation',
                                            'situation', 'sunshine', 'min_temperature', 'max_temperature',
                                            'average_temperature', 'orientation', 'air', 'geology',
                                            'pedology', 'lithology', 'hierarchy',)))

        return Response(response)

    @ action(methods=['GET'], detail=False, url_path='centerpoint/(?P<id>[^/.]+)')
    def get_centerpoint(self, request, id):
        appellation_zone = self.queryset.filter(id=id).first()
        if not appellation_zone:
            return Response({
                'message': f"This id is not linked to any appellation zone. Provided = {id}"
            }, status.HTTP_404_NOT_FOUND)

        if not appellation_zone.geom:
            return Response({
                'message': f"This appellation zone has wron property geom. Provided = {id}"
            }, status.HTTP_404_NOT_FOUND)

        geom = GEOSGeometry(appellation_zone.geom).centroid.coords
        return Response({"lng": geom[0],
                         "lat": geom[1]})

    @ action(methods=['GET'], detail=False, url_path='boundingbox/(?P<id>[^/.]+)')
    def get_bounding_box(self, request, id):
        appellation_zone = self.queryset.filter(id=id).first()
        if not appellation_zone:
            return Response({
                'message': f"This id is not linked to any appellation zone. Provided = {id}"
            }, status.HTTP_404_NOT_FOUND)

        if not appellation_zone.geom:
            return Response({
                'message': f"This appellation zone has wron property geom. Provided = {id}"
            }, status.HTTP_404_NOT_FOUND)

        geom = GEOSGeometry(appellation_zone.geom).envelope
        if geom.geom_type == 'Point':
            return Response({'message': f"It is a point {geom.coords}"})
        polygon_points = geom.extent
        width = polygon_points[2] - polygon_points[0]
        height = polygon_points[3] - polygon_points[1]
        response = {
            "width": width,
            "height": height,
            "bounding_box": [
                {
                    "x-min": polygon_points[0],
                    "y-min": polygon_points[1],
                    "x-max": polygon_points[2],
                    "y-max": polygon_points[3]
                }
            ]
        }
        return Response(response)

    @ action(methods=['GET'], detail=False, url_path='boundingbox_multiple')
    def get_multiple_bounding_box(self, request):
        params = request.query_params.copy()

        geometry_figure = GEOSGeometry('POINT EMPTY')
        if 'zones_appepplation' in params:
            appellation_geoms = self.queryset.filter(
                id__in=[int(id) for id in params.get('zones_appepplation').split(',')]).values_list('geom', flat=True)
            for geom in appellation_geoms:
                geometry_figure = geometry_figure.union(GEOSGeometry(geom))
        if 'plot_zones' in params:
            plot_geoms = self.queryset.filter(
                id__in=[int(id) for id in params.get('plot_zones').split(',')]).values_list('geom', flat=True)
            for geom in plot_geoms:
                if geom:
                    geometry_figure = geometry_figure.union(GEOSGeometry(geom))
        if 'points' in params:
            points = params.get('points').split('|')
            for point in points:
                try:
                    latitude = point.split(':')[0]
                    longtitude = point.split(':')[1]
                    point = Point(float(latitude), float(longtitude))
                    geometry_figure = geometry_figure.union(
                        GEOSGeometry(point))
                except Exception:
                    return Response({'message': f"Please verify your data {params.get('points')}"}, status.HTTP_400_BAD_REQUEST)
        if geometry_figure == GEOSGeometry('POINT EMPTY'):
            return Response({'message': f"Can not find any information with thi parameters"}, status.HTTP_404_NOT_FOUND)
        polygon_points = geometry_figure.extent
        width = polygon_points[2] - polygon_points[0]
        height = polygon_points[3] - polygon_points[1]
        response = {
            "width": width,
            "height": height,
            "bounding_box": [
                {
                    "x-min": polygon_points[0],
                    "y-min": polygon_points[1],
                    "x-max": polygon_points[2],
                    "y-max": polygon_points[3]
                }
            ]
        }
        return Response(response)

    @ action(methods=['GET'], detail=False, url_path='image')
    def get_image(self, request):
        center_point = request.query_params.get('center_point')
        real_width = request.query_params.get('real_width')
        real_height = request.query_params.get('real_height')
        img_height = request.query_params.get('img_height')
        img_width = request.query_params.get('img_width')
        bearing = request.query_params.get('bearing')
        pitch = request.query_params.get('pitch')

        if not center_point or not real_height or not real_width or not img_height or not img_width:
            return Response(
                {"message": "Please verify your data. Required fields (center_point , real_height ,real_width, img_height ,img_width)"},
                status.HTTP_400_BAD_REQUEST
            )
        coordinates = center_point.split(',')
        if len(coordinates) < 2:
            return Response(
                {"message": "Please verify center_point"},
                status.HTTP_400_BAD_REQUEST
            )

        latitude = float(coordinates[1])

        int_real_width = int(real_width)
        int_img_width = int(img_width)
        int_real_height = int(real_height)
        int_img_height = int(img_height)

        # calculate the meters per pixel corresponding to the width , height
        result_width = int_real_width / int_img_width
        result_height = int_real_height / int_img_height

        final_result = max(result_height, result_width)

        cosinos_radian = math.cos(math.radians(latitude))

        slippy_map_tilenames = 156543.03 * cosinos_radian / final_result

        zoom_level = math.log10(slippy_map_tilenames) / math.log10(2) - 1.5

        key = settings.MAP_KEY
        url = f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/{center_point},{zoom_level},{bearing},{pitch}/{img_width}x{img_height}?access_token={key}"

        return Response({"url": url})


class PlotViewSet(ModelViewSet):
    serializer_class = PlotZoneSerializer
    queryset = PlotZone.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not 'hierarchy' in request.data or \
                not 'code_insee' in request.data or \
                not "prefix" in request.data or \
                not 'section' in request.data or not 'number' in request.data:
            return Response({
                "message": "One or vital parameter are missing. Please check everything. Provided:" +
                f"'code_insee': {request.data.get('code_insee')}, 'hierarchy': {request.data.get('hierarchy')}," +
                f"'section': {request.data.get('section')}, 'number': {request.data.get('number')}, 'geom': {request.data.get('geom')}"})
        if serializer.is_valid():
            serializer.save()
            response = json.loads(serialize('geojson', [serializer.instance],
                                            geometry_field='geom',
                                            fields=('hierarchy', 'code_insee', 'prefix', 'section', 'number')))
            return Response(response)
        else:
            return Response(serializer.errors)

    @ action(methods=['GET', 'PUT', 'DELETE'], detail=False, url_path='(?P<code_insee>[^/.]+)/(?P<section>[^/.]+)/(?P<number>[^/.]+)')
    def retrieve_plot(self, request, code_insee, section, number=None):
        plot_query_set = self.queryset.filter(
            code_insee=code_insee, section=section)
        if number:
            plot_query_set = plot_query_set.filter(number=number)
        plot = plot_query_set.first()
        if not plot:
            data = f"{code_insee}, " + f"{section}"
            if number:
                data += f", {number}"
            return Response({'message': f"There is any row corresponding to the data. Provided ({data})"})
        if request.method == "GET":
            response = json.loads(serialize('geojson', [plot],
                                            geometry_field='geom',
                                            fields=('hierarchy', 'code_insee', 'prefix', 'section', 'number')))
            return Response(response)
        elif request.method == "PUT":
            geom = request.data.get('geom')
            data = {
                "code_insee": code_insee,
                "section": section,
                "number": number,
                "geom": geom,
            }
            serializer = self.get_serializer(plot, data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
            response = json.loads(serialize('geojson', [serializer.instance],
                                            geometry_field='geom',
                                            fields=('hierarchy', 'code_insee', 'prefix', 'section', 'number')))
            return Response(response)
        else:
            plot.delete()
            return Response({"messege": True})


class SectionViewSet(ModelViewSet):
    serializer_class = PlotZoneSerializer
    queryset = PlotZone.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if request.data.get('number'):
            return Response({"message": "You cannot create a section with the " +
                             "'number' key because it is used for parcelle creation. Please remove" +
                             "it or see Parcelle documentation part. Provided " +
                             f"'code_insee': {request.data.get('code_insee')}, 'hierarchie': '{request.data.get('hierarchy')}' " +
                             f", 'section': '{request.data.get('section')}', 'number': {request.data.get('number')}, 'geom': '{request.data.get('geom')}'"},
                            status.HTTP_406_NOT_ACCEPTABLE)
        if not 'hierarchy' in request.data or \
                not 'code_insee' in request.data or \
                not "prefix" in request.data or \
                not 'section' in request.data:
            return Response({
                "message": "One or vital parameter are missing. Please check everything. Provided:" +
                f"'code_insee': {request.data.get('code_insee')}, 'hierarchy': {request.data.get('hierarchy')}," +
                f"'section': {request.data.get('section')}, 'number': {request.data.get('number')}, 'geom': {request.data.get('geom')}"})
        if serializer.is_valid():
            serializer.save()
            response = json.loads(serialize('geojson', [serializer.instance],
                                            geometry_field='geom',
                                            fields=('hierarchy', 'code_insee', 'prefix', 'section', 'number')))
            return Response(response)
        else:
            return Response(serializer.errors)

    @ action(methods=['GET', 'PUT', 'DELETE'], detail=False, url_path='(?P<code_insee>[^/.]+)/(?P<section>[^/.]+)')
    def retrieve_section(self, request, code_insee, section):
        plot_query_set = self.queryset.filter(
            code_insee=code_insee, section=section)
        plot = plot_query_set.first()
        if not plot:
            data = f"{code_insee}, " + f"{section}"
            return Response({'message': f"There is any row corresponding to the data. Provided ({data})"})

        if request.method == "GET":
            response = json.loads(serialize('geojson', [plot],
                                            geometry_field='geom',
                                            fields=('hierarchy', 'code_insee', 'prefix', 'section', 'number')))
            return Response(response)
        elif request.method == "PUT":
            geom = request.data.get('geom')
            code_from_request = request.data.get('code_insee')
            section_from_request = request.data.get('section')
            data = {
                "code_insee": code_from_request,
                "section": section_from_request,
                "geom": geom,
            }
            serializer = self.get_serializer(plot, data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
            response = json.loads(serialize('geojson', [serializer.instance],
                                            geometry_field='geom',
                                            fields=('hierarchy', 'code_insee', 'prefix', 'section', 'number')))
            return Response(response)
        else:
            plot.delete()
            return Response({"messege": True})


class GeoAutocomplateViewSet(ModelViewSet):
    serializer_class = AppellationSerializer
    queryset = Appellation.objects.all()

    @ action(methods=['GET'], detail=False, url_path='autocomplete/(?P<start_of_name>[^/.]+)')
    def autocomplete(self, request, start_of_name):
        source = request.query_params.get('source')
        get_info_from_database = False
        if source in ['true', 'True'] or source is True:
            get_info_from_database = True
        if get_info_from_database:
            # without algolia
            query = start_of_name.lower()
            queryset = self.queryset.filter(name__lower__istartswith=query)
            if len(queryset) == 0:
                return Response({
                    "input": start_of_name,
                    "message": f"We cannot find '{ start_of_name }' in our data base."
                }, status.HTTP_404_NOT_FOUND)
            retrieved_from_input = {}
            results = []
            for appellation in queryset:
                i = 0
                id_zone_appellation = ''
                if appellation.zone_appelation:
                    id_zone_appellation = appellation.zone_appelation.id
                results.append({
                    'appellation': appellation.name,
                    'dgc': appellation.name_dgc,
                    'id_zone_appellation': id_zone_appellation
                })
                retrieved_from_input[i] = appellation.name or appellation.name_dgc
                i += 1
            first_matched = queryset.first().name
            response = {
                'input': query,
                'matched': first_matched,
                'retrieved_from_input': retrieved_from_input,
                'count': len(queryset),
                'results': results
            }
            return Response(response)
        else:
            # with algolia
            index = client.init_index('Appellation')
            index.search_rules('', {'anchoring': 'startsWith'})
            result_ids = [result.get('objectID') for result in index.search(
                start_of_name).get('hits')]
            queryset = self.queryset.filter(id__in=result_ids)
            if len(queryset) == 0:
                return Response({
                    "input": start_of_name,
                    "message": f"We cannot find '{ start_of_name }' in our data base."
                }, status.HTTP_404_NOT_FOUND)
            retrieved_from_input = {}
            results = []
            i = 0
            for appellation in queryset:

                id_zone_appellation = ''
                if appellation.zone_appelation:
                    id_zone_appellation = appellation.zone_appelation.id
                results.append({
                    'appellation': appellation.name,
                    'dgc': appellation.name_dgc,
                    'id_zone_appellation': id_zone_appellation
                })
                retrieved_from_input[i] = appellation.name or appellation.name_dgc
                i += 1
            first_matched = queryset.first().name
            response = {
                'input': start_of_name,
                'matched': first_matched,
                'retrieved_from_input': retrieved_from_input,
                'count': len(queryset),
                'results': results
            }
            return Response(response)

    @action(methods=['GET'], detail=False, url_path='corrector/(?P<query>[^/.]+)')
    def corrector(self, request, query):
        index = client.init_index('Appellation')
        index.set_settings({
            'typoTolerance': True,
        })
        result = index.search(query, {
            'restrictSearchableAttributes': [
                'name',
            ]
        })
        if result.get('nbHits') == 0:
            return Response({
                "input": query,
                "message": "Any appellation could be find."
            }, status.HTTP_404_NOT_FOUND)

        results = []
        for appellation in result.get('hits'):
            appellation_zone = ''
            if appellation.get('zone_appelation'):
                appellation_zone = appellation.get('zone_appelation').id
            results.append({
                "id_appellation": appellation.get('objectID'),
                "appellation": appellation.get('name', ''),
                "name_dgc": appellation.get('name_dgc', ''),
                "id_zone_appellation": appellation_zone
            },)
        return Response({"input": "Alox Cortno",
                         "number": result.get('nbHits'),
                         "results": results
                         })

    @ action(methods=['GET'], detail=False, url_path='grape/(?P<grape>[^/.]+)')
    def grape_variety(self, request, grape):
        source = request.query_params.get('source')
        get_info_from_database = False
        if source in ['true', 'True'] or source is True:
            get_info_from_database = True
        if get_info_from_database:
            query = grape.lower()
            queryset = self.queryset.filter(
                wineCDC__assemble__grape_assemble__grape__name__lower=query)
            if len(queryset) == 0:
                return Response({
                    "error": f"This grape { grape } in not linked to any appellation"
                }, status.HTTP_404_NOT_FOUND)
            results = []
            for appellation in queryset:
                id_zone_appellation = ''
                if appellation.zone_appelation:
                    id_zone_appellation = appellation.zone_appelation.id
                results.append({
                    'id_zone_appellation': id_zone_appellation,
                    'name': appellation.name,
                })
            return Response(results)
        else:
            index = client.init_index('WineCDC')
            result = index.search(grape).get('hits')
            if len(result) == 0:
                return Response({
                    "error": f"This grape { grape } in not linked to any appellation"
                }, status.HTTP_404_NOT_FOUND)
            results = []
            for appellation in result:
                results.append({
                    'id_zone_appellation': appellation.get('id_zone_appellation', ''),
                    'name': appellation.get('name', ''),
                })
            return Response(results)


class ZoneAdminCadastreViewSet(ModelViewSet):

    serializer_class = AdminZoneSerializer
    queryset = AdminZone.objects.all()

    @action(methods=['GET'], detail=False, url_path='cadastre/(?P<place>[^/.]+)/(?P<name>[^/.]+)/(?P<code_insee>[^/.]+)')
    def get_cadastre(self, request, place, name, code_insee):
        queryset = self.queryset.filter(
            name=name, plot_zone__code_insee=code_insee, hierarchy=place)
        if len(queryset) == 0:
            return Response({
                "error": f"There is no { place } corresponding to informations provided. Provided ('{ name }', '{ code_insee }')"
            }, status.HTTP_404_NOT_FOUND)
        response = json.loads(serialize('geojson', queryset,
                                        geometry_field='geom',
                                        fields=('name', 'code', 'hierarchy')))
        return Response(response)

    @action(methods=['GET'], detail=False, url_path='autocomplete/lieudit/(?P<start_name>[^/.]+)')
    def autocomplate(self, request, start_name):
        source = request.query_params.get('source')
        get_info_from_database = False
        if source in ['true', 'True'] or source is True:
            get_info_from_database = True
        if not get_info_from_database:
            # Algolia search
            index = client.init_index('AdminZone')
            index.search_rules('', {'anchoring': 'startsWith'})
            result = index.search(start_name).get('hits')[:10]

            if len(result) == 0:
                return Response({
                    "message": f"We cannot find any lieudit starting with '{ start_name }' in our data base."
                }, status.HTTP_404_NOT_FOUND)

            results = []
            for zone_admin in result:
                results.append({
                    'name': zone_admin.get('name', ''),
                    'code': zone_admin.get('code_insee', '')
                })
            response = {
                "input": start_name,
                "number": len(result),
                "results": results
            }
            return Response(response)
        else:
            # without algolia
            query = start_name.lower()
            queryset = self.queryset.filter(
                name__lower__istartswith=query)[:10]
            if len(queryset) == 0:
                return Response({
                    "message": f"We cannot find any lieudit starting with '{ start_name }' in our data base."
                }, status.HTTP_404_NOT_FOUND)

            results = []
            for zone_admin in queryset:
                code_insee = ''
                if zone_admin.plot_zone.all().first():
                    code_insee = zone_admin.plot_zone.all().first().code_insee
                results.append({
                    'name': zone_admin.name,
                    'code': code_insee
                })
            response = {
                "input": start_name,
                "number": len(queryset),
                "results": results
            }
            return Response(response)


class LandscapeViewSet(ModelViewSet):
    serializer_class = AppellationPhotoSerializer
    queryset = AppellationPhoto.objects.all()

    def list(self, request):
        queryset = self.queryset.filter(gps_coordinates__isnull=False)
        if len(queryset) == 0:
            return Response({"error": f"There is no Landscape with coordinates"}, status.HTTP_404_NOT_FOUND)
        response = json.loads(serialize('geojson', queryset,
                                        geometry_field='gps_coordinates',
                                        fields=('shooting', 'definition', 'file_name', 'url', 'date', 'source', 'description', 'media_photo')))
        return Response(response)


class Landscape360ViewSet(ModelViewSet):
    serializer_class = AppellationPhotoSerializer
    queryset = AppellationPhoto.objects.all()

    def list(self, request):
        queryset = self.queryset.filter(
            media_photo="360")
        if len(queryset) == 0:
            return Response({"error": f"There is no Landscape360 with coordinates"}, status.HTTP_404_NOT_FOUND)

        features = []
        features = json.loads(serialize('geojson', queryset,
                                        geometry_field='gps_coordinates',
                                        fields=('shooting', 'definition', 'file_name', 'url', 'date', 'source', 'description', 'media_photo')))

        response = features
        return Response(response)


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)
