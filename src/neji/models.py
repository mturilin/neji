from django.db import models

# Create your models here.


class CodeSession(models.Model):
    session_id = models.CharField(max_length=32)
    code = models.TextField()

