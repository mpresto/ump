from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# from rest_framework.decorators import api_view

from django.contrib import messages

from django.contrib.auth.hashers import PBKDF2PasswordHasher   # for hashing, duh

from .models import MyUser, Doggo, Rating
from .forms import Registration_Form, Doggo_Upload_Form, Rating_Form
from django.utils import timezone
import datetime
import pickle
import sqlite3

# Create your views here.


# BASIC PAGE VIEWS


# @api_view(['GET'])
def home_view(request):
    """The home page for User Database Site"""
    return render(request, 'home_template.html')


@login_required
def about_me(request):
    """About Me page for my website"""
    return TemplateResponse(request, 'about_me.html')


# VIEWS FOR USERS

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
        "some_other_data": "I'm an important hooman!"
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

            authenticated_user = authenticate(
                email=new_user.email,
                password=request.POST['password']
                )

        # log the new user in
            login(request, new_user)
            return HttpResponseRedirect('home-page')

    context = {'form': form}
    return render(request, 'register.html', context)


# AUTHENTICATION


def my_login(request):
    """Render the login page for users"""
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


# VIEWS FOR DOGGOS #

@login_required
def doggo_polling(request):
    """Page for voting on your favorite pups!"""
    dogs = Doggo.objects.all()

    return render(request, 'doggo_poll_template.html', {'dogvars': dogs})


@login_required
def submit_rating(request):
    """Record user's rating value for the doggo"""
    if request.method != 'POST':
        form = Rating_Form()

    else:
        # Process created form
        form = Rating_Form(data=request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(
                    request, messages.SUCCESS, 'Rating submitted!'
                    )
            # update Doggo.average_rating()

        dogs = Doggo.objects.all()
        return render(request, 'doggo_poll_template.html', {'dogvars': dogs})


@login_required
def create_a_doggo(request):
    """Register a new user"""
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

            # get new_doggos's id
            # info_for_template = Doggo.objects.get(id=new_doggo.dog_id)

            # take user to doggie detail page
            # return HttpResponse(info_for_template)
            messages.add_message(
                request, messages.SUCCESS, 'Doggo successfully registered!'
                )
            return TemplateResponse(request, 'home_template.html')

    context = {'form': form}
    return render(request, 'doggo_upload_template.html', context)


@login_required
def doggo_detail_view(request, dog_id):
    """Doggo detail page"""

    def get_average_rating(self):
        """Query database and calculate average rating for a doggo"""
        connection = sqlite3.connect("db.sqlite3")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT CAST(AVG(vote_value)as int) FROM u_app_rating
            WHERE rated_doggo_id=?""", (dog_id,))

        return cursor.fetchone()

    # check for the dog's id
    try:
        this_doggo = Doggo.objects.get(id=dog_id)
        this_vote_average = get_average_rating(dog_id)
        formatted_vote_average = ' '.join(map(str, (this_vote_average)))

    # return 404 if dog_id not found
    except Doggo.DoesNotExist:
        return TemplateResponse(request, 'dog_404_template.html')

    # template information:
    data_for_template = {
        "doggo_info": {'dogvar_detail': this_doggo},
        "some_other_data": "I'm a floofy angel!",
        "average_rating": formatted_vote_average,
        }
    return render(request, 'doggo_detail_template.html', data_for_template)
