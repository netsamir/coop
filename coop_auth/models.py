""" Model for Authorization"""
from django.db import models

# Create your models here.

class CoopAuthToken(models.Model):
    """Keeping the token"""
    user_id = models.CharField(max_length=128, primary_key=True)
    access_token = models.CharField(max_length=256)
    expire_at = models.DateTimeField()

    def __str__(self):
        return self.user_id + ":" + self.access_token
