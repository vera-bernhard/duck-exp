from django.db import models

# Create your models here.
from django.db import models

class CodeSnippet(models.Model):
    title = models.CharField(max_length=100)
    code = models.TextField()