# from django.db import models
# from u_app.models import MyUser
# import datetime

# # Create your models here.

# class Doggo(models.Model):
#     """A class for our doggos"""
#     name = models.CharField(max_length=200)
#     age = models.IntegerField(blank=True)
#     description = models.CharField(max_length=500)
#     entry_date = models.DateTimeField(auto_now_add=True)


# class Rating(models.Model):
#     """A model for our rating records"""
#     user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
#     doggo = models.ForeignKey(Doggo, on_delete=models.CASCADE)