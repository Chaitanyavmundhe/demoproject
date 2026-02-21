from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    CATEGORY_CHOICES = ['CSE','IT','Mechanical','Assignment','Notes','Electronics']
    
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category    = models.CharField(max_length=50)
    semester    = models.CharField(max_length=20)
    file        = models.FileField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)