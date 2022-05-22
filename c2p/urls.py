from bottle.urls import router
from views import OrderViewSet

router.register(r'command', OrderViewSet, basename='command')