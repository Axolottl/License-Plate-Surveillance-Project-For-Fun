from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User

# Create your models here.

class SignedDataSerializer(serializers.Serializer):
   signed_data = serializers.CharField()
   signature = serializers.CharField()

class Material(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_key = models.TextField()