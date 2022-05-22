from django.conf.urls import include, re_path
from rest_framework.routers import DefaultRouter
from client.views import ClientViewSet, MessageViewSet
from c2p.urls import router


router.register(r'message', MessageViewSet, basename='message')
router.register(r'client', ClientViewSet, basename='client')

