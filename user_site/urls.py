"""user_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.urls import views as auth_views

from u_app import views


urlpatterns = [
    path('admin', admin.site.urls),
    path('home-page', views.home_view, name='home'),
    path('users-page', views.users, name='users'),
    path('users/<id>', views.user_detail, name='user_detail'),
    path('register', views.register_user, name='register'),
    path('login-page', views.my_login, name='login'),
    path('login-submit-endpoint', views.submit_login),
    path('logout', auth_views.LogoutView.as_view
            (template_name='home_template.html'), name='logout'),
    path('about-me-page', views.about_me, name='about_me'),
    path('doggo-poll-page', views.doggo_polling, name='doggo_polls'),
    path('submit-my-rating', views.submit_rating, name='submit_vote'),
    path('doggo-uploader', views.create_a_doggo, name='register_dog'),
    path('doggos/<dog_id>', views.doggo_detail_view, name='doggo_detail'),
]
