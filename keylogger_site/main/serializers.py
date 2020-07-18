from rest_framework import serializers

from .models import *


class KeyloggerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyloggerData
        fields = ['keylogger_ref', 'date', 'data']

class KeyloggerIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyloggerID
        fields = ['id']