from django.db import models
from django.core.validators import FileExtensionValidator

class File(models.Model):
    file = models.FileField(blank=False, null=False, validators=[FileExtensionValidator( ['csv'] )])
    remark = models.CharField(max_length=20, blank=True, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)