#from wine.urls import router
from django.db import router
from appellation.views import (
    AdminZoneViewSet,
    AppellationViewSet,
    ColorViewSet,
    AppellationTypeViewSet,
    AppellationPhotoViewSet,
    AppellationZoneViewSet,
    PlotZoneViewSet,
    ViticultureZoneViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'appellation_zone', AppellationZoneViewSet,
                basename='appellation_zone')
router.register(r'appellation_photo', AppellationPhotoViewSet,
                basename='appellation_photo')
router.register(r'appellation', AppellationViewSet,
                basename='appellation')
router.register(r'appellation_colour', ColorViewSet,
                basename='appellation_colour')
router.register(r'appellation_type', AppellationTypeViewSet,
                basename='appellation_type')
router.register(r'admin_zone', AdminZoneViewSet,
                basename='admin_zone')
router.register(r'plot_zone', PlotZoneViewSet,
                basename='plot_zone')
router.register(r'viticulture_zone', ViticultureZoneViewSet,
                basename='viticulture_zone')

