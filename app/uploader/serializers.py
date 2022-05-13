from requests import request
from rest_framework import serializers
from .models import File
import pathlib
import pandas as pd
import csv


class ExtraFieldSerializer(serializers.Serializer):
    def to_representation(self, instance): 
        file = instance.file.path
        reviews_df = pd.read_csv(file, nrows=1)
        listed_row = {name: str(dtype) for name, dtype in reviews_df.dtypes.iteritems()}
        return listed_row

    def to_internal_value(self, data):
        return {
          self.field_name: 'Any python object made with data: %s' % data
        }


class FileSerializer(serializers.ModelSerializer):
    file_columns = ExtraFieldSerializer(source='*')
    class Meta():
        model = File
        #fields = ('id', 'file', 'remark', 'timestamp')
        fields = ('id', 'file', 'remark', 'timestamp','file_columns')


