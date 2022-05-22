from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.views import Response
from core.serializers import AssembleSerializer, CountrySerializer
from core.models import Assemble, Country

# Create your views here.


class CountryViewSet(ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)
