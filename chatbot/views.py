# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.conf import settings
# import os
# import json

# from .models import DataFile, AnalysisQuery
# from .serializers import DataFileSerializer, AnalysisQuerySerializer, QueryInputSerializer
# from .services.excel_handler import ExcelHandler
# from .services.data_processor import DataProcessor
# from .services.llm_service import LLMService

# class DataFileUploadView(APIView):
#     """API view for uploading Excel files"""
#     def post(self, request, *args, **kwargs):
#         print("Request data:")
#         if 'file' not in request.FILES:
#             return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
#             print
#         file = request.FILES['file']
        
#         # Check file extension
#         if not file.name.endswith(('.xls', '.xlsx')):
#             return Response({"error": "Only Excel files (.xls, .xlsx) are allowed"}, status=status.HTTP_400_BAD_REQUEST)
            
#         # Check file size
#         if file.size > settings.MAX_UPLOAD_SIZE:
#             return Response({"error": f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE/1024/1024}MB"}, 
#                           status=status.HTTP_400_BAD_REQUEST)
                          
#         # Create new DataFile instance
#         name = request.data.get('name', file.name)
#         data_file = DataFile(file=file, name=name)
#         data_file.save()
        
#         # Try to load the file to verify it's valid
#         try:
#             file_path = os.path.join(settings.MEDIA_ROOT, data_file.file.name)
#             excel_handler = ExcelHandler(file_path)
#             if not excel_handler.load_data():
#                 # Delete the file if it's invalid
#                 data_file.delete()
#                 return Response({"error": "Invalid Excel file format"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             # Delete the file if there's an error
#             data_file.delete()
#             return Response({"error": f"Error processing file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
#         serializer = DataFileSerializer(data_file)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class DataFileListView(generics.ListAPIView):
#     """API view for listing uploaded files"""
#     queryset = DataFile.objects.filter(is_active=True).order_by('-uploaded_at')
#     serializer_class = DataFileSerializer

# class AnalyzeQueryView(APIView):
#     """API view for analyzing real estate queries"""
    
#     def post(self, request, *args, **kwargs):
#         # Validate input
#         serializer = QueryInputSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
#         query = serializer.validated_data['query']
#         file_id = serializer.validated_data.get('file_id')
        
#         # Get the data file
#         try:
#             if file_id:
#                 data_file = DataFile.objects.get(id=file_id, is_active=True)
#             else:
#                 # Get the most recent file if no file_id provided
#                 data_file = DataFile.objects.filter(is_active=True).order_by('-uploaded_at').first()
                
#             if not data_file:
#                 return Response({"error": "No data file available for analysis"}, status=status.HTTP_404_NOT_FOUND)
                
#             file_path = os.path.join(settings.MEDIA_ROOT, data_file.file.name)
            
#         except DataFile.DoesNotExist:
#             return Response({"error": "Data file not found"}, status=status.HTTP_404_NOT_FOUND)
            
#         # Process the query
#         excel_handler = ExcelHandler(file_path)
#         if not excel_handler.load_data():
#             return Response({"error": "Error loading data file"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
#         data_processor = DataProcessor(excel_handler)
#         result = data_processor.process_query(query)
        
#         # Generate summary using LLM service
#         llm_service = LLMService()
#         summary = llm_service.generate_summary(result)
#         result['summary'] = summary
        
#         # Save the query and result
#         analysis = AnalysisQuery(
#             query=query,
#             response_summary=summary,
#             response_data=result
#         )
#         analysis.save()
        
#         return Response(result, status=status.HTTP_200_OK)

# class AvailableAreasView(APIView):
#     """API view for getting available areas from the latest uploaded file"""
    
#     def get(self, request, *args, **kwargs):
#         # Get the most recent file
#         data_file = DataFile.objects.filter(is_active=True).order_by('-uploaded_at').first()
        
#         if not data_file:
#             return Response({"error": "No data file available"}, status=status.HTTP_404_NOT_FOUND)
            
#         file_path = os.path.join(settings.MEDIA_ROOT, data_file.file.name)
        
#         # Get available areas
#         excel_handler = ExcelHandler(file_path)
#         if not excel_handler.load_data():
#             return Response({"error": "Error loading data file"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
#         areas = excel_handler.get_areas()
        
#         return Response({"areas": areas}, status=status.HTTP_200_OK)



from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import os
import pandas as pd
from typing import Dict, Any
import json

from .models import DataFile, AnalysisQuery
from .serializers import DataFileSerializer, AnalysisQuerySerializer, QueryInputSerializer
from .services.llm_service import LLMService

class DataFileUploadView(APIView):
    """API view for uploading Excel files"""
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        file = request.FILES['file']
        
        # Check file extension
        if not file.name.endswith(('.xls', '.xlsx')):
            return Response({"error": "Only Excel files (.xls, .xlsx) are allowed"}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
        # Check file size
        if file.size > settings.MAX_UPLOAD_SIZE:
            return Response(
                {"error": f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE/1024/1024}MB"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Create new DataFile instance
        name = request.data.get('name', file.name)
        data_file = DataFile(file=file, name=name)
        data_file.save()
        
        # Try to load the file to verify it's valid
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, data_file.file.name)
            df = pd.read_excel(file_path)
            if df.empty:
                data_file.delete()
                return Response({"error": "Excel file is empty"}, status=status.HTTP_400_BAD_REQUEST)
                
            # Store available areas in the model for quick access
            data_file.available_areas = ','.join(df['final location'].unique().tolist())
            data_file.save()
        except Exception as e:
            data_file.delete()
            return Response({"error": f"Error processing file: {str(e)}"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DataFileSerializer(data_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DataFileListView(generics.ListAPIView):
    """API view for listing uploaded files"""
    queryset = DataFile.objects.filter(is_active=True).order_by('-uploaded_at')
    serializer_class = DataFileSerializer

class AnalyzeQueryView(APIView):
    """API view for analyzing real estate queries"""
    
    def post(self, request, *args, **kwargs):
        # Validate input
        serializer = QueryInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        query = serializer.validated_data['query']
        file_id = serializer.validated_data.get('file_id')
        
        # Get the data file
        try:
            if file_id:
                data_file = DataFile.objects.get(id=file_id, is_active=True)
            else:
                # Get the most recent file if no file_id provided
                data_file = DataFile.objects.filter(is_active=True).order_by('-uploaded_at').first()
                
            if not data_file:
                return Response({"error": "No data file available for analysis"}, 
                              status=status.HTTP_404_NOT_FOUND)
                
            file_path = os.path.join(settings.MEDIA_ROOT, data_file.file.name)
            
        except DataFile.DoesNotExist:
            return Response({"error": "Data file not found"}, status=status.HTTP_404_NOT_FOUND)
            
        # Process the query
        try:
            # Initialize LLM service with the data file
            llm_service = LLMService()
            llm_service.load_data(file_path)
            
            # Generate comprehensive response
            response = llm_service.generate_response(query)
            
            # Save the query and result
            analysis = AnalysisQuery(
                query=query,
                response_summary=response.get('summary', ''),
                response_data=json.dumps(response)
            )
            analysis.save()
            
            return Response(response, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Error processing query: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AvailableAreasView(APIView):
    """API view for getting available areas from the latest uploaded file"""
    
    def get(self, request, *args, **kwargs):
        # Get the most recent file
        data_file = DataFile.objects.filter(is_active=True).order_by('-uploaded_at').first()
        
        if not data_file:
            return Response({"error": "No data file available"}, status=status.HTTP_404_NOT_FOUND)
            
        if hasattr(data_file, 'available_areas') and data_file.available_areas:
            areas = data_file.available_areas.split(',')
        else:
            try:
                file_path = os.path.join(settings.MEDIA_ROOT, data_file.file.name)
                df = pd.read_excel(file_path)
                areas = df['final location'].unique().tolist()
                # Update the model for future requests
                data_file.available_areas = ','.join(areas)
                data_file.save()
            except Exception as e:
                return Response(
                    {"error": f"Error loading data file: {str(e)}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response({"areas": areas}, status=status.HTTP_200_OK)

class AvailableMetricsView(APIView):
    """API view for getting available metrics from the latest uploaded file"""
    
    def get(self, request, *args, **kwargs):
        metrics = [
            "price",
            "demand",
            "sales",
            "units",
            "area",
            "price_growth",
            "demand_growth"
        ]
        return Response({"metrics": metrics}, status=status.HTTP_200_OK)