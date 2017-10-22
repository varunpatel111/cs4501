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
        return JsonResponse(d, status=400)

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
            return JsonResponse(d, status=400)


def isValidAuthenticator(request):
    if (request.POST.get('user')):
        user = (request.POST.get('user'))
        user_num = int(user)
        if (len(CustomUser.objects.filter(id=user_num)) == 0):
            return False
        if (authenticate(request, user_num)):
            return False
        else:
            return True
    else:
        return False

# Create a new authenticator

def login(request):
    d = dict()
    if request.method != "POST":
        d["status"] = "FAILED"
        d["message"] = "This should be a POST request."
        return JsonResponse(d, status=400)

    if request.method == "POST":
        if (isValidAuthenticator(request)):
            user = (request.POST.get('user'))
            user_num = int(user)
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
            return JsonResponse(d)
        else:
            d["status"] = "FAILED"
            d["message"] = "Either the fields are incorrect or that user authentication exists!"
            return JsonResponse(d, status=400)

def logout(request, user):
    d = {}
    if request.method == "DELETE":
        user_num = int(user)
        if (len(Authenticator.objects.filter(user_id=user_num)) == 0):
            d["status"] = "FAILED"
            d["message"] = "THAT AUTHENTICATOR DOESN'T EXIST"
            return JsonResponse(d,  status=404)
        A = Authenticator.objects.filter(user_id=user_num)[0]
        A.delete()
        d["status"] = "SUCCESS"
        d["message"] = "AUTHENTICATOR DELETED SUCCESSFULLY"
        return JsonResponse(d)
    else:
        d["status"] = "FAILED"
        d["message"] = "This should be a DELETE request."
        return JsonResponse(d, status=400)

# Authenticate
def authenticate(request, user):
    if(len(Authenticator.objects.filter(user_id_id=user)) != 0):
        return True
    else:
        return False
