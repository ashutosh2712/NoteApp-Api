from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Note(models.Model):
    body = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
