from rest_framework import serializers

from .models import *


class GetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyloggerData
        fields = ['keylogger_ref', 'date', 'data']

class GetIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyloggerID
        fields = ['id']

# class SaveNewDataSerializer(serializers.Serializer):