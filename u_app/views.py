from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

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
    # return HttpResponse("Yooooo")
    """Log in an existing user"""
    # submit form input
    email = request.POST.get('username')
    password = request.POST.get('password')


    # string = repr({'email-submitted': email, 'password-submiited': password })
    # return HttpResponse(string)



    # authenticate the user
    # user = authenticate(request, email=email, password=password)

    # pull one user by email (based on form input email)
    try:
        user = MyUser.objects.get(email=email)
    except MyUser.DoesNotExist:
        # if not found user return false authentication
        raise Http404('User not found.')

    legitpassword = user.password == password

    # compare form input password to found user

    if legitpassword is True:
        login(request, user)
        # messages.info(request, "Logged in successfully!")
        return HttpResponse("Logged in successfully!")
    else:
        return HttpResponse("NOT Logged in :(")




# def logout_view(request):
#     logout(request)
#     # Redirect to a success page.
#     messages.info(request, "Logged out successfully!")
#     return render(request, 'home.html')



