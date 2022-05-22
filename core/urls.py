from core.views import  CountryViewSet
from client.urls import router



router.register(r'country', CountryViewSet,
                basename='country')
