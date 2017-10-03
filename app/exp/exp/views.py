from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.shortcuts import render
import urllib.request
import urllib.parse


def test(request):
    print ("About to perform the GET request...")

    req = urllib.request.Request('http://models-api:8000/')
    return HttpResponse(req)
