from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


from .models import User

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


# def register_user(request):
#     """Register a new user"""
#     if request.method != 'POST':
#         # display blank form
#         form = UserCreationForm()
#     else:
#         new_user = form.save()
#         # Log the user in and then redirect to home page
#         authenticated_user = authenticate(
#             username=new_user.username,
#             password=request.POST['password1'])
#         login(request, authenticated_user)
#         return HttpResponseRedirect()


