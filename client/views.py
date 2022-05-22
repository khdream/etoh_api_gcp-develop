from rest_framework.viewsets import ModelViewSet

from client.serializers import ClientSeriazer, CommandSeriazer, MessageSeriazer
from client.models import Client, Command, Message
from rest_framework import status
from rest_framework.views import Response
# Create your views here.


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSeriazer
    queryset = Message.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSeriazer
    queryset = Client.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        id_customer = request.data.get('id_customer')
        if not id_customer:
            return Response({'error': 'Please enter name of the food'}, status=status.HTTP_400_BAD_REQUEST)
        if self.queryset.filter(id_customer=id_customer):
            return Response({'error': f'There is already exists food with that customer id  : {id_customer}'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


