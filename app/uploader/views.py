from calendar import c
from glob import escape
import imp
from warnings import filters
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
def getdataview(request, pk, nrows):
    instance = File.objects.get(id=pk)
    file = instance.file.path
    reviews_df = pd.read_csv(file, nrows=nrows)
    json_data = reviews_df.to_json(orient='records')
    send_data = json_data.replace("\"", "'")
    return Response(send_data)


@api_view(['POST'])
def filterview(request, pk, nrows):
    instance = File.objects.get(id=pk)
    file = instance.file.path
    filters = request.data['filters']
    sorters = request.data['sorters']
    new_str = ''
    reviews_df = pd.read_csv(file, nrows=nrows)
    for key, value in filters.items():
        if key in reviews_df.columns:
            if type(value) == str:
                value = "'" + value + "'"
                new_str += ' and ' + str(key).replace(" ", "_") + '==' + str(value)
            if type(value) == dict:
                filter_param = value.get('expression')
                expr_value = value.get('filter_data')
                new_str += ' and ' + str(key).replace(" ", "_") + filter_param + '=' + str(expr_value)
    if new_str[5:] == '':
        return Response('Not valid columns for this csv file')
    else:
        reviews_df.columns = [column.replace(" ", "_") for column in reviews_df.columns]
        sort_list = [sort_key.replace(" ", "_") for sort_key in sorters]
        reviews_df = reviews_df.query(new_str[5:]).sort_values(by=sort_list, ascending=False)
        json_data = reviews_df.to_json(orient='records')
        send_data = json_data.replace("\"", "'")
        return Response(send_data)