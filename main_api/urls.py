"""main_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, re_path
from rest_framework_swagger.views import get_swagger_view
from food_and_wine_pairing.views import AMVAgreement, AMVAutocomplateViewSet, AMVFoodViewSet
from rest_framework.routers import DefaultRouter
from bottle.urls import router as crud_router
from main_api.views import (
    DescriptionViewSet,
    GeoAutocomplateViewSet,
    GeoAppellationViewSet,
    GeoWinemakersViewSet,
    Landscape360ViewSet,
    LandscapeViewSet,
    PlotViewSet,
    SectionViewSet,
    WSEAutocomplateViewSet,
    WSECountryAutocomplete,
    WSEGrapeAutocomplete,
    WSEViticultureZoneViewSet,
    WSEWineChoosing,
    WineCDCDescriptionViewSet,
    WinemakerDescriptionViewSet,
    WinemakerViewSet,
    ZoneAdminCadastreViewSet,
    SwaggerSchemaView
)
from main_api.cron import algolia_reindex_cron
from bottle.views import CustomerViewSet, StocklistViewsSet, StockListCrudViewSet
from productspec.views import BottleViewSet, WineViewSet

from user_management.views import UserViewSet, GroupAccessViewSet, AuthAPIView, StatisticsAPIViewSet
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'groupaccess', GroupAccessViewSet, basename='GroupAccess')
router.register(r'stats', StatisticsAPIViewSet, basename='APIstatistics')

router.register(r'stock/list', StockListCrudViewSet,
                basename='stock_list')
router.register(r'amv/food', AMVFoodViewSet,
                basename='amv_food')
router.register(r'amv', AMVAutocomplateViewSet,
                basename='amv_autocomplate')
router.register(r'amv', AMVAgreement,
                basename='create_match')
router.register(r'wse', WSEAutocomplateViewSet,
                basename='wse-autocomplate')
router.register(r'wse', WSEWineChoosing,
                basename='wse-wine')
router.register(r'wse', WSEGrapeAutocomplete,
                basename='grape_autocomplate')
router.register(r'wse', WSECountryAutocomplete,
                basename='country_autocomplate')
router.register(r'wse', WSEViticultureZoneViewSet,
                basename='region_vineyard')
router.register(r'wmk', WinemakerViewSet,
                basename='wmk')
router.register(r'bottle/description', DescriptionViewSet,
                basename='description')
router.register(r'bottle/description', WinemakerDescriptionViewSet,
                basename='description')
router.register(r'bottle/description', WineCDCDescriptionViewSet,
                basename='description')
router.register(r'bottle', BottleViewSet,
                basename='bottle')
router.register(r'wine', WineViewSet,
                basename='wine')
router.register(r'stock', StocklistViewsSet,
                basename='stock')
router.register(r'stock', CustomerViewSet,
                basename='stock')
router.register(r'geo/cadastre/section', SectionViewSet,
                basename='section')
router.register(r'geo/cadastre/plot', PlotViewSet,
                basename='plot')
router.register(r'geo/winemakers', GeoWinemakersViewSet,
                basename='geo_winemakers')
router.register(r'geo/landscape', LandscapeViewSet,
                basename='landscape')
router.register(r'geo/landscape360', Landscape360ViewSet,
                basename='landscape360')
router.register(r'geo', GeoAppellationViewSet,
                basename='polygon')
router.register(r'geo', GeoAutocomplateViewSet,
                basename='autocomplate')
router.register(r'geo', ZoneAdminCadastreViewSet,
                basename='cadastre')

# change emain name and terms
# regenerate file in yaml format
# change the openapi-appengine.yaml with it
schema_view = get_schema_view(
    openapi.Info(
        title="Etoh API",
        default_version='v2',
        description="Food and Wine Matching",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
swager_ui = get_swagger_view(title='Etoh API')
urlpatterns = [
    path('authentication/', AuthAPIView.as_view()),
    path('authentication/apikey/', AuthAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', swager_ui),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('admin/', admin.site.urls),
    path('algolia-reindex/', algolia_reindex_cron, name='algolia_reindex'),
    re_path('^', include(router.urls)),
    re_path('^api/', include(crud_router.urls)),

]
