from calendar import c
from glob import escape
import imp
from rest_framework import viewsets
from .models import File
from .serializers import FileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse, HttpResponse
import pandas as pd
from rest_framework.decorators import api_view
import json

class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    queryset = File.objects.all()

@api_view(['POST'])
def getdataview(request, pk):
    instance = File.objects.get(id=pk)
    file = instance.file.path
    reviews_df = pd.read_csv(file, nrows=5)
    json_data = reviews_df.to_json(orient='records')
    send_data = json_data.replace("\"", "'")
    return Response(send_data)


@api_view(['POST'])
def filterview(request, pk):
    instance = File.objects.get(id=pk)
    file = instance.file.path
    reviews_df = pd.read_csv(file, nrows=50)
    reviews_df.columns =[column.replace(" ", "_") for column in reviews_df.columns]
    df = reviews_df.query('year_released == 2009')
    json_data = df.to_json(orient='records')
    send_data = json_data.replace("\"", '')
    return Response(send_data)