"""exp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^api/homePage', views.homePage),
	url(r'^api/listingPage/(?P<listing>[0-9]+)/$', views.get_listing),
	url(r'^api/userPage/(?P<user>[0-9]+)/$', views.get_user),
    url(r'^api/newListing/$', views.newListingForm),
    url(r'^api/createListing/', views.createListing),
    url(r'^api/createUser/', views.createUser),
    url(r'^api/newUser/', views.newUserForm),
    url(r'^api/loginForm/', views.loginForm),
    url(r'^api/userLogin/', views.userLogin),
    url(r'^api/getUserId/', views.getUserId),
    url(r'^api/logoutUser/', views.logoutUser),
]
