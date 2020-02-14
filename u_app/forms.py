from django import forms
from django.db import models
from .models import User
import datetime


# class Registration_Form(forms.ModelForm):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # # username = forms.CharField(max_length=100, help_text='Username')
#     # fullname = forms.CharField(max_length=100, help_text='First and Last Name')
#     # email = forms.EmailField(max_length=150, help_text='Email')
#     # birth_year = forms.IntegerField(help_text='YYYY')
#     # # registration_date = forms.DateTimeField()

#     class Meta:
#         model = User
#         fields = ('username', 'password', 'fullname','email', 'birth_year',)
