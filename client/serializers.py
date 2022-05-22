from django.db.models import fields
from rest_framework import serializers
from client.models import Client, Message
from bottle.models import Range, Warehouse
from c2p.models import Order


class MessageSeriazer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ClientSeriazer(serializers.ModelSerializer):
    warehouses = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all(),
                                                    many=True, required=False, allow_null=True)
    ranges = serializers.PrimaryKeyRelatedField(queryset=Range.objects.all(),
                                                many=True, required=False, allow_null=True)
    orders = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(),
                                                  many=True, required=False, allow_null=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'id_customer',
                  'warehouses', 'ranges', 'orders', 'created_at', 'updated_at']



