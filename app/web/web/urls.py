"""web URL Configuration

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
	url(r'^$', views.homePage, name='home'),
	url(r'^listings/(?P<listing>[0-9]+)/$', views.get_listing),
	url(r'^rec/(?P<rec>[0-9]+)/$', views.get_rec),
    url(r'^users/(?P<user>[0-9]+)/$', views.get_user),
	url(r'^api/$', views.apiInfo),
    url(r'^listings/new/$', views.create_listing_form, name='create_listing'),
    url(r'^users/new/$', views.create_user_form),
    url(r'^login/$', views.login_form, name='login'),
    url(r'^logout/$', views.logout),
    url(r'^search/$', views.search),
]
