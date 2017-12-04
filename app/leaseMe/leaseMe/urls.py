"""leaseMe URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from marketplace import viewsListings
from marketplace import viewsAuthenticator
from marketplace import viewsUsers
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^recommendations/', viewsListings.recommendations),
    url(r'^api/rec/del/(?P<rec>[0-9]+)/$', viewsListings.delete_recs),
    url(r'^api/rec/(?P<rec>[0-9]+)/$', viewsListings.get_recs),

    #url(r'^', include(router.urls)),
    #url(r'^api/', include(ro, csrf_exempt(direct_to_template), uter.urls))
    url(r'^api/users/$', viewsUsers.all_users),
    url(r'^api/users/(?P<user>[0-9]+)/$', viewsUsers.get_user),
    url(r'^api/users/create/$', viewsUsers.users_create),
    url(r'^api/listings/$', viewsListings.all_listings),
    url(r'^api/listings/(?P<listing>[0-9]+)/$', viewsListings.get_listing),
    url(r'^api/listings/create/$', viewsListings.listings_create),
    url(r'^api/listings/createForm/$', viewsListings.new_listing_form),
    url(r'^api/users/createForm/$', viewsUsers.new_user_form),
    url(r'^api/login/$', viewsAuthenticator.login),
    url(r'^api/logout/$', viewsAuthenticator.logout),
    url(r'^api/authenticators/$', viewsAuthenticator.all_authenticators),
    url(r'^api/authenticate/(?P<user>[0-9]+)/$', viewsAuthenticator.authenticate),
    url(r'^api/getUserId/$', viewsAuthenticator.getUserId),
    #url(r'^api/validateUser/$', views.validateUser),

    # Forms
    url(r'^api/authenticate/login/$', viewsUsers.loginUser),
    url(r'^api/authenticate/logout/$', viewsUsers.logoutUser),
    #url(r'^users/(?P<pk>[0-9]+)/', views.CustomUserDetail.as_view()),
    #url(r'^users', views.CustomUserList.as_view()),
    #url(r'^listings', views.ListingList.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
