# from django.db import models

# # Create your models here.


from django.db import models

class DataFile(models.Model):
    """Model to store uploaded Excel files"""
    file = models.FileField(upload_to='data_files/')
    name = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class AnalysisQuery(models.Model):
    """Model to store user queries and results"""
    query = models.TextField()
    response_summary = models.TextField(blank=True, null=True)
    response_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.query[:50]