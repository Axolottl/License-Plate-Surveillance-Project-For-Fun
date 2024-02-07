from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Data, MapData, AgentKeys, AgentData

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['name', 'age', 'address', 'phone', 'email', 'date', 'time']

class MapDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapData
        fields = ['latitude', 'longitude']

class AgentKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentKeys
        fields = ['key', 'agent']

class AgentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentData
        fields = ['agent', 'data']