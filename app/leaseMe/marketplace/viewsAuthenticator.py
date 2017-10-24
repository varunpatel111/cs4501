from .models import CustomUser
from .models import Listing
from .models import Authenticator
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.shortcuts import render
from .forms import ListingForm
from django.template.loader import render_to_string
from datetime import datetime
import os
import hmac
from .forms import ListingForm
from django.template.loader import render_to_string
from django.contrib.auth import hashers
from django.forms.models import model_to_dict
from django import db

def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__


def all_authenticators(request):
    if request.method != "GET":
        d = dict()
        d["status"] = "FAILED"
        d["message"] = "Request should be a GET request."
        return JsonResponse(d)

    else:
        queryset = Authenticator.objects.all().values()
        arr = []
        for obj in queryset:
            arr.append(obj)
        d = {}
        if(len(queryset) > 0):
            d["status"] = "SUCCESS"
            d["data"] = arr
            return JsonResponse(d)
        else:
            d["status"] = "FAILED"
            d["message"] = "No authenticators currently."
            return JsonResponse(d)


def isValidAuthenticator(request, userId):
    user_num = userId
    if (len(CustomUser.objects.filter(id=user_num)) == 0):
        return False
    if (authenticate(request, user_num)):
        return False
    else:
        return True

# Authenticate
def authenticate(request, user):
    if(len(Authenticator.objects.filter(user_id_id=user)) != 0):
        return True
    else:
        return False


# Create a new authenticator

def login(request):
    d = dict()
    if request.method != "POST":
        d["status"] = "FAILED"
        d["message"] = "This should be a POST request."
        return JsonResponse(d)


    if request.method == "POST":
        username = request.POST.get('username')
        password = (request.POST.get('password'))
        if(actualUser(username, password)):
            if (isValidAuthenticator(request, int(CustomUser.objects.filter(username=username)[0].id))):
                user_num = int(CustomUser.objects.filter(username=username)[0].id)
                user = CustomUser.objects.filter(id=user_num)[0]
                date_created = datetime.now()
                key = '0!i@++*n5lxns$^f=zl5(48a(g^0f%b71mn%7^6w%06=kmlzs6'
                authenticator = hmac.new(key = key.encode('utf-8'),msg = os.urandom(32),digestmod = 'sha256').hexdigest()
                while (len(Authenticator.objects.filter(authenticator=authenticator)) != 0):
                    authenticator = hmac.new(key = key.encode('utf-8'),msg = os.urandom(32),digestmod = 'sha256').hexdigest()
                newAuthenticator = Authenticator(user_id=user, date_created=date_created, authenticator=authenticator)
                newAuthenticator.save()
                d["id"] = newAuthenticator.id
                d["status"] = "SUCCESS"
                d["message"] = "Authenticator created successfully"
                d["authenticator"] = authenticator
                return JsonResponse(d)
            else:
                d["status"] = "FAILED"
                d["message"] = "Either the fields are incorrect or that user authentication exists!"
                return JsonResponse(d)
        else:
            d["status"] = "FAILED"
            d["message"] = "Incorrect Username or Password"
            return JsonResponse(d)


def actualUser(username, password):
    if(len(CustomUser.objects.filter(username=username)) == 0):
        return False
    else:
        return hashers.check_password(password, CustomUser.objects.filter(username=username)[0].password)



def logout(request):
    d = {}
    if request.method == "POST":
        authenticator = request.POST.get('authenticator')
        if (len(Authenticator.objects.filter(authenticator=authenticator)) == 0):
            d["status"] = "FAILED"
            d["message"] = "THAT AUTHENTICATOR DOESN'T EXIST"
            return JsonResponse(d)
        A = Authenticator.objects.filter(authenticator=authenticator)[0]
        A.delete()
        d["status"] = "SUCCESS"
        d["message"] = "AUTHENTICATOR DELETED SUCCESSFULLY"
        return JsonResponse(d)
    else:
        d["status"] = "FAILED"
        d["message"] = "This should be a POST request."
        return JsonResponse(d)

def getUserId(request):
    d = {}
    if request.method == "POST":
        authenticator = request.POST.get('authenticator')
        if (len(Authenticator.objects.filter(authenticator=authenticator)) == 0):
            d["status"] = "FAILED"
            d["message"] = "THAT AUTHENTICATOR DOESN'T EXIST"
        else:
            A = Authenticator.objects.filter(authenticator=authenticator)[0]
            user_Id = A.user_id_id
            d["user_id"] = user_Id
            return JsonResponse(d)
