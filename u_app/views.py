from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# from rest_framework.decorators import api_view

from django.contrib import messages

from django.contrib.auth.hashers import PBKDF2PasswordHasher   # for hashing, duh

from .models import MyUser, Doggo
from .forms import Registration_Form, Doggo_Upload_Form
from django.utils import timezone
import datetime
import pickle

# Create your views here.


# @api_view(['GET'])
def home_view(request):
    """The home page for User Database Site"""
    return render(request, 'home_template.html')


# @api_view(['GET'])
@login_required
def users(request):
    """Controller for user mainpage"""
    users = MyUser.objects.all()

    return render(request, 'users.html', {'users': users})


# @api_view(['GET', 'POST'])
@login_required
def user_detail(request, id):
    """User detail page"""
    try:
        user = MyUser.objects.get(id=id)
    except MyUser.DoesNotExist:
        raise Http404('User not found.')

    data_for_template = {
        "all_about_user":
            {
                'user_detail': user
            },
        "some_other_data": "I am important!"
    }

    return render(request, 'user_detail.html', data_for_template)


def register_user(request):
    """Register a new user"""
    # create blank form
    if request.method != 'POST':
        form = Registration_Form()

    else:
        # Process created form
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
            return HttpResponseRedirect('home-page')

    context = {'form': form}
    return render(request, 'register.html', context)


# MANUAL LOGIN/AUTHENTICATION

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
        return render(request, 'home_template.html')

    else:
        messages.add_message(request, messages.INFO, 'Please try again!')
        return render(request, 'login.html')


@login_required
def about_me(request):
    """About Me page for my website"""
    return TemplateResponse(request, 'about_me.html')


@login_required
def doggo_polling(request):
    """Page for voting on your favorite pups!"""
    # populate doggo poll template
    return TemplateResponse(request, 'doggo_poll_template.html')
    # FAILSAFE: # return HttpResponse('Get ready for cute dogs')


@login_required
def submit_rating(request):
    """Submit vote"""
    # return HttpResponse('Submitting your rating...')
    # submit form input
    vote_value = request.POST.get('rate_value')
    # user_who_voted = request.POST.get(MyUser.id)
    return HttpResponse(vote_value)

    # if 10 > vote_value > 20:
    #     messages.add_message(request, messages.INFO,
    #         'Rating must be between 10 and 20, because all dogs are 10/10 or more!')
    #     return render(request, 'doggo_poll_template.html')
    # else:
    #     messages.add_message(request, messages.SUCCESS, 'Submitted your rating!')
    #     return render(request, 'doggo_poll_template.html')

    # collect submitting user's id
    # collect doggo's id
    # set doggo's rating for that user
    # return a success message


@login_required
def create_a_doggo(request):
    """Register a new user"""
    # return HttpResponse('Upload A Dog')
    # create blank form
    if request.method != 'POST':
        form = Doggo_Upload_Form()

    else:
        # Process created form
        form = Doggo_Upload_Form(data=request.POST)

        if form.is_valid():
            # save form
            new_doggo = form.save()
            new_doggo.entry_date = timezone.now()
            new_doggo.save(update_fields=['entry_date'])

        # take user to doggie detail page
            return HttpResponseRedirect('doggo_polls')

    context = {'form': form}
    return render(request, 'doggo_upload_template.html', context)
