from django.shortcuts import render

# Create your views here.
from serializers import OrderSeriazer
from models import Order
from rest_framework import status
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSeriazer
    queryset = Order.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)
