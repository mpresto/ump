from django.db import models
import datetime

# Create your models here.

class Doggo(models.Model):
    """A class for our doggos"""
    name = models.CharField(max_length=200)
    age = models.IntegerField(blank=True)
    entry_date = modesl.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    """A model for our vote records"""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    doggo = models.ForeighKey(Doggo, on_delete=models.CASCADE)