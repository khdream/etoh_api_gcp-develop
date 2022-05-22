from algoliasearch.search_client import SearchClient
from django.db.models import CharField, TextField, Q
from django.db.models.functions import Lower
from django.conf import settings
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import Response
from food_and_wine_pairing.models import Food

from food_and_wine_pairing.serializers import AMVFoodSerializer, FoodWineMatchSeriazer, FoodWineMatch

from food_and_wine_pairing.serializers import (
    AMVFoodSerializer,
    CookingSerializer,
    FoodSeriazer,
    FoodCategorySerializer,
    FoodWineMatchSeriazer,
    IngredientSerializer,
    RecipeCookingSerializer,
    RecipeIngredientSerializer,
    RecipeSerializer,
    RecipeSpiceSerializer,
    SpiceSerializer,
)
from food_and_wine_pairing.models import (
    Cooking,
    Food,
    FoodCategory,
    FoodWineMatch,
    Ingredient,
    Recipe,
    RecipeCooking,
    RecipeIngredient,
    RecipeSpice,
    Spice,
)


CharField.register_lookup(Lower)
TextField.register_lookup(Lower)

client = SearchClient.create(settings.ALGOLIA.get(
    'APPLICATION_ID'), settings.ALGOLIA.get('SEARCH_API_KEY'))


class FoodViewSet(ModelViewSet):
    serializer_class = FoodSeriazer
    queryset = Food.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        name = request.data.get('name')
        if not name:
            return Response({'error': 'Please enter name of the food'}, status=status.HTTP_400_BAD_REQUEST)
        if self.queryset.filter(name=name):
            return Response({'error': f'There is already exists food with that name : {name}'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class FoodWineMatchViewSet(ModelViewSet):
    serializer_class = FoodWineMatchSeriazer
    queryset = FoodWineMatch.objects.all()


class FoodCategoryViewSet(ModelViewSet):
    serializer_class = FoodCategorySerializer
    queryset = FoodCategory.objects.all()


class IngredientViewSet(ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class CookingViewSet(ModelViewSet):
    serializer_class = CookingSerializer
    queryset = Cooking.objects.all()


class SpiceViewSet(ModelViewSet):
    serializer_class = SpiceSerializer
    queryset = Spice.objects.all()


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


class RecipeIngredientViewSet(ModelViewSet):
    serializer_class = RecipeIngredientSerializer
    queryset = RecipeIngredient.objects.all()


class RecipeSpiceViewSet(ModelViewSet):
    serializer_class = RecipeSpiceSerializer
    queryset = RecipeSpice.objects.all()


class RecipeCookingViewSet(ModelViewSet):
    serializer_class = RecipeCookingSerializer
    queryset = RecipeCooking.objects.all()


class AMVFoodViewSet(ModelViewSet):
    serializer_class = AMVFoodSerializer
    queryset = Food.objects.all()
    multiple_lookup_fields = ['name', 'id']

    def get_object(self, **kwargs):
        try:
            food_object = self.queryset.filter(id=kwargs.get('pk')).first()
        except ValueError:
            food_object = self.queryset.filter(
                name__lower=kwargs.get('pk').lower()).first()
        return food_object

    def create(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(
                {
                    "food_is_created": True,
                    "message": f"{ serializer.data.get('name') or serializer.data.get('id') }",
                    "data_send": request.data,
                    "link": reverse('amv_food-detail', args=[serializer.data.get('id')], request=request)
                }, status=status.HTTP_201_CREATED)
        else:
            existing_food_id = self.queryset.filter(
                name=request.data.get('name')).first().id
            response = Response({
                "food_is_created": False,
                "message": "Food with this name already exists",
                "data_send": request.data,
                "link": reverse('amv_food-detail', args=[existing_food_id], request=request)
            }, status=status.HTTP_409_CONFLICT)
        return response

    def retrieve(self, request, *args, **kwargs):
        food_object = self.get_object(**kwargs)

        if food_object:
            serializer = self.serializer_class(food_object)
            response = Response(serializer.data)
        else:
            response = Response({"error": "not found"},
                                status=status.HTTP_404_NOT_FOUND)
        return response

    def update(self, request, **kwargs):
        food_object = self.get_object(**kwargs)
        if food_object:
            serializer = AMVFoodSerializer(
                food_object, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

            response = Response(
                {
                    "search": kwargs.get('pk', ''),
                    "data": request.data,
                    "update": True,
                    "message": f'{food_object.name or food_object.id } updated'
                })
        else:
            response = Response(
                {
                    "search": kwargs.get('pk', ''),
                    "data": request.data,
                    "update": False,
                    "message": 'No food found to be updated'
                }, status=status.HTTP_404_NOT_FOUND)

        return response

    def destroy(self, request, **kwargs):
        food_object = self.get_object(**kwargs)
        if food_object:
            response = Response(
                {
                    "search": kwargs.get('pk', ''),
                    "deleted": True,
                    "message": f'{food_object.name or food_object.id } deleted'
                })
            food_object.delete()

        else:
            response = Response(
                {
                    "search": kwargs.get('pk', ''),
                    "deleted": False,
                    "message": 'No food gound to be deleted'
                }, status=status.HTTP_404_NOT_FOUND)
        return response


class AMVAutocomplateViewSet(ViewSet):
    serializer_class = AMVFoodSerializer
    queryset = Food.objects.all()

    @action(methods=['GET'], detail=False, url_path='autocomplete-food/(?P<query>[^/.]+)')
    def autocomplate_food(self, request, query):
        source = request.query_params.get('source')
        get_info_from_database = False
        if source in ['true', 'True'] or source is True:
            get_info_from_database = True
        if get_info_from_database:
            query = query.lower()
            queryset = self.queryset.filter(name__lower__startswith=query)[:3]
            results = []
            for food in queryset:
                results.append({
                    'id': food.id,
                    'name': food.name,
                    'description': food.description
                })
            if results:
                response_status = status.HTTP_200_OK
            else:
                response_status = status.HTTP_404_NOT_FOUND

            return Response({
                "search": query,
                "results": results
            }, status=response_status)
        else:
            index = client.init_index('Food')
            query = query.lower()
            objects = index.search(query).get('hits')[:3]
            results = []
            for food in objects:
                results.append({
                    'id': food.get("objectID"),
                    'name': food.get('name'),
                    'description': food.get('description')
                })
            if results:
                response_status = status.HTTP_200_OK
            else:
                response_status = status.HTTP_404_NOT_FOUND

            return Response({
                "search": query,
                "results": results
            }, status=response_status)


class AMVAgreement(ModelViewSet):
    serializer_class = FoodWineMatchSeriazer
    queryset = FoodWineMatch.objects.all()

    @action(methods=['POST'], detail=False, url_path='create-match')
    def create_match(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(
                {
                    "data": request.data,
                    "created": True,
                    "messege": "Accord inserted"
                }, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            response = Response(
                {
                    "data": request.data,
                    "created": False,
                    "messege": errors
                }, status=status.HTTP_409_CONFLICT)
        return response

    @action(methods=['GET'], detail=False, url_path='match_by_food/(?P<query>[^/.]+)')
    def find_match_by_food(self, request, query):
        query = query.lower()
        food_queryset = Food.objects.filter(
            name__lower__startswith=query).prefetch_related('food_wine_match')
        results = {}
        for food in food_queryset:
            if food.food_wine_match.all():
                results[food.name] = []
                for food_wine_match in food.food_wine_match.all():
                    results[food.name].append(
                        self.get_serializer(food_wine_match).data)
        if results:
            response_status = status.HTTP_200_OK
        else:
            response_status = status.HTTP_404_NOT_FOUND
        response = {
            "food_search": query,
            "results": results
        }
        return Response(response, response_status)

    @action(methods=['GET'], detail=False, url_path='food_by_match')
    def find_match_by_field(self, request):
        fields_of_matcher = [
            'country', 'region', 'vineyard', 'appellation'
            'dgs', 'grape', 'type', 'colour',
            'dose', 'denomination_wine', 'source'
        ]
        query = Q()
        accord_search = {}
        for key, value in request.query_params.items():
            if key not in fields_of_matcher:
                return Response({
                    "error": f"Field { key } does not exist"
                })
            accord_search[key] = value
            field = {key: value}
            query &= Q(**field)
        queryset = self.queryset.filter(query).select_related('food')
        results = []
        food = []
        for food_match in queryset:
            if food_match.food not in food and food_match.food:

                food.append(food_match.food)
                results.append({
                    "id": food_match.food.id,
                    "name": food_match.food.name,
                    "description": food_match.food.description,
                    "slug": food_match.food.slug,
                })
        if results:
            response_status = status.HTTP_200_OK
        else:
            response_status = status.HTTP_404_NOT_FOUND
        response = {
            "accord_search": accord_search,
            "count_limit": 10,
            "results": results[:10]
        }
        return Response(response, response_status)
