from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User

# Create your views here.

# @login_required
def home(request):
    """The home page for User Site"""
    users = User.objects.all()
    return render(request, 'home.html', {'users': users})
    return HttpResponse("Welcome to the User Database")

# @login_required
def user_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        raise Http404('User not found.')
    return render(request, 'user_detail.html', {'user': user})
