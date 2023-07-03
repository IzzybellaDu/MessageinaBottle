from asyncio.windows_events import NULL
from urllib import request
from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class memory(models.Model):
    title           = models.CharField(max_length=100)
    bodyText        = models.TextField(default="Hello, world.")
    date            = models.DateField(default=date.today, blank=True)
    user            = models.ForeignKey(User, default=NULL, on_delete=models.CASCADE, related_name="memories")

    def __str__(self):
        return self.title