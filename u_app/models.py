from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import connection

import sqlite3

# Create your models here.


class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)
    birth_date = models.DateField(blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'birth_date',]


class Doggo(models.Model):
    """A class for our doggos"""
    name = models.CharField(max_length=200)
    image_url = models.CharField(max_length=500)
    age = models.IntegerField(blank=True)
    description = models.CharField(max_length=500)
    entry_date = models.DateTimeField(auto_now_add=True)
    submitter = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class Rating(models.Model):
    """A model for our rating records"""
    user_who_voted = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    rated_doggo = models.ForeignKey(Doggo, on_delete=models.CASCADE)
    vote_value = models.IntegerField(default=0)
