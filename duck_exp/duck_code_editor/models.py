from django.db import models

class CodeSnippet(models.Model):
    code = models.TextField()