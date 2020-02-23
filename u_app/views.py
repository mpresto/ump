from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from django.contrib.auth.hashers import PBKDF2PasswordHasher # for hashing, duh

from .models import MyUser, Registration_Form
from django.utils import timezone
import datetime
import pickle

# Create your views here.


def home(request):
    """The home page for User Database Site"""
    return render(request, 'home.html')


@login_required
def users(request):
    """Controller for user mainpage"""
    users = MyUser.objects.all()
   
    return render(request, 'users.html', {'users': users})

@login_required
def user_detail(request, id):
    """User detail page"""
    try:
        user = MyUser.objects.get(id=id)
    except MyUser.DoesNotExist:
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
            new_user.save(update_fields=['last_login'])

            authenticated_user = authenticate(email=new_user.email,
                password=request.POST['password'])

        # log the new user in 
            login(request, new_user)
            return HttpResponseRedirect('home')

    context = {'form': form}
    return render(request, 'register.html', context)




# WORKING ON MANUAL LOGIN/LOGOUT METHODS

def my_login(request): 
    return TemplateResponse(request, 'login.html')

def submit_login(request):
    """Log in an existing user"""
    # submit form input
    email = request.POST.get('email')
    password = request.POST.get('password')

    # pull one user by email (based on form input email):
    try:
        user = MyUser.objects.get(email=email)
    except MyUser.DoesNotExist:
        # if user not found, return false authentication
            # raise Http404('User not found.')
        messages.add_message(request, messages.INFO, 'Please try again!')
        return render(request, 'login.html')

    # define password requirements:
    legitpassword = user.password == password

    # compare form input password to found user
    if legitpassword is True:
        login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Logged in successfully!')
        return render(request, 'home.html')

    else:
        messages.add_message(request, messages.INFO, 'Please try again!')
        return render(request, 'login.html')




# def logout_view(request):
#     logout(request)
#     # Redirect to a success page.
#     messages.info(request, "Logged out successfully!")
#     return render(request, 'home.html')



