from rest_framework import serializers
from .models import DataFile, AnalysisQuery

class DataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFile
        fields = ['id', 'file', 'name', 'uploaded_at']
        read_only_fields = ['uploaded_at']

class AnalysisQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisQuery
        fields = ['id', 'query', 'response_summary', 'response_data', 'created_at']
        read_only_fields = ['created_at', 'response_summary', 'response_data']

class QueryInputSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=500)
    file_id = serializers.IntegerField(required=False)