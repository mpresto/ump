from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from user_site import settings


from django import forms
import datetime

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


class Registration_Form(forms.ModelForm):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    birth_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, help_text='DD-MM-YYYY')
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = MyUser
        fields = ('email', 'password', 'confirm_password', 'full_name', 'birth_date',)
