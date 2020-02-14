from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone


from django import forms
import datetime

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50, default='blah')
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254,)
    birth_year = models.DateField(null=True, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    last_login = ()


class Registration_Form(forms.ModelForm):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # password = models.CharField(max_length=50, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'fullname','email', 'birth_year', 'registration_date')
        # password = models.CharField(max_length=50, widget=forms.PasswordInput)