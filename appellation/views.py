
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.views import Response
from appellation.serializers import (
    AdminZoneSerializer,
    ColorSerializer,
    AppellationSerializer,
    AppellationTypeSerializer,
    AppellationPhotoSerializer,
    AppellationZoneSerializer,
    PlotZoneSerializer,
    ViticultureZoneSerializer,
)
from appellation.models import (
    AdminZone,
    Appellation,
    Color,
    AppellationType,
    AppellationPhoto,
    AppellationZone,    
    PlotZone,
    ViticultureZone,
)


class AppellationZoneViewSet(ModelViewSet):
    serializer_class = AppellationZoneSerializer
    queryset = AppellationZone.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class AppellationPhotoViewSet(ModelViewSet):
    serializer_class = AppellationPhotoSerializer
    queryset = AppellationPhoto.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class AppellationViewSet(ModelViewSet):
    serializer_class = AppellationSerializer
    queryset = Appellation.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class ColorViewSet(ModelViewSet):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class AppellationTypeViewSet(ModelViewSet):
    serializer_class = AppellationTypeSerializer
    queryset = AppellationType.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class AdminZoneViewSet(ModelViewSet):
    serializer_class = AdminZoneSerializer
    queryset = AdminZone.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class PlotZoneViewSet(ModelViewSet):
    serializer_class = PlotZoneSerializer
    queryset = PlotZone.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)


class ViticultureZoneViewSet(ModelViewSet):
    serializer_class = ViticultureZoneSerializer
    queryset = ViticultureZone.objects.all()

    def destroy(self, request, pk):
        object = self.queryset.filter(id=pk).first()
        if object:
            return Response({'message': f"Id {pk} deleted"})
        return Response({'error': f'Can not find object with this id {pk}'}, status=status.HTTP_404_NOT_FOUND)

