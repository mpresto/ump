from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# from django.contrib.auth.forms import UserCreationForm


from .models import User, Registration_Form
# from .forms import Registration_Form
import datetime

# Create your views here.

# @login_required
def home(request):
    """The home page for User Site"""
    return render(request, 'home.html')

# @login_required
def users(request):
    """Controller for user mainpage"""
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})

# @login_required
def user_detail(request, id):
    """User detail page"""
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        raise Http404('User not found.')
    return render(request, 'user_detail.html', {'user': user})


def register_user(request):
    """Register a new user"""
    # create blank form
    if request.method != 'POST':
        form = Registration_Form()

    else:
        #Process created form
        form = Registration_Form(data=request.POST)

        if form.is_valid():
            # save form
            new_user = form.save()
            new_user.last_login = timezone.now()
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST)
        # log the new user in 
            login(request, new_user)
            return HttpResponseRedirect('home')
    context = {'form': form}
    return render(request, 'register.html', context)

