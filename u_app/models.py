from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=30)
    fullname = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    birth_year = models.IntegerField()
    registration_date = models.DateTimeField()
