from django import forms
from django.db import models
from .models import MyUser, Doggo, Rating
from user_site import settings
import datetime


class Registration_Form(forms.ModelForm):
    """A registration form for our users"""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    birth_date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS, help_text='DD-MM-YYYY'
        )
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = MyUser
        fields = (
            'email', 'password', 'confirm_password', 'full_name', 'birth_date',
            )


class Doggo_Upload_Form(forms.ModelForm):
    """An upload form to create/register a new dog"""
    name = forms.CharField(max_length=200)
    image_url = forms.CharField(
        max_length=500, help_text='Paste a URL to your puppers photo!'
        )
    age = forms.IntegerField()
    description = forms.CharField(max_length=500)
    submitter = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    class Meta:
        model = Doggo
        fields = ('name', 'image_url', 'age', 'description', 'submitter',)


class Rating_Form(forms.ModelForm):
    """A form to submit user votes on doggos"""
    user_who_voted = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    rated_doggo = models.ForeignKey(Doggo, on_delete=models.CASCADE)
    vote_value = forms.IntegerField()

    class Meta:
        model = Rating
        fields = ('vote_value', 'rated_doggo', 'user_who_voted',)
