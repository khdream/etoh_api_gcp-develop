from rest_framework import serializers

from django.contrib.auth.models import User
from user_management.models import GroupAccess, APIuser, APIstatistics




class GroupAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupAccess
        fields = ('name','apiList')

class GroupAccessSerializerNameOnly(serializers.ModelSerializer):
    class Meta:
        model = GroupAccess
        fields = ('name',)

class APIuserSerializerGroupOnly(serializers.ModelSerializer):
    groupAccess = GroupAccessSerializerNameOnly(read_only=True, many=True)
    class Meta:
        model = APIuser
        fields = ('groupAccess',)

class UserSerializerIDonly(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserSerializer(serializers.ModelSerializer):
    apiuser = APIuserSerializerGroupOnly(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'apiuser',)
#        fields = ('__all__')

class APIstatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIstatistics
        fields = ('__all__')

