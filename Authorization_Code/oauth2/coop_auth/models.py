""" Model for Authorization"""
from django.db import models

# Create your models here.

class CoopAuthToken(models.Model):
    """Keeping the token"""
    access_token = models.CharField(max_length=256)

    def __str__(self):
        return self.access_token
