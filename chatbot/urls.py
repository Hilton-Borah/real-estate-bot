from django.urls import path
from .views import (
    DataFileUploadView,
    DataFileListView,
    AnalyzeQueryView,
    AvailableAreasView,
)

urlpatterns = [
    path('files/upload/', DataFileUploadView.as_view(), name='file-upload'),
    path('files/', DataFileListView.as_view(), name='file-list'),
    path('analyze/', AnalyzeQueryView.as_view(), name='analyze-query'),
    path('areas/', AvailableAreasView.as_view(), name='available-areas'),
]