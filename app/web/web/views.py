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
import math

def apiInfo(request):

	return render(request, 'index.html')

def homePage(request):
	req = urllib.request.Request('http://exp-api:8000/api/homePage')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)

	data = resp["data"]

	rows = math.ceil(len(data)/3)

	return render(request, 'homepage.html', {'data': data}, {'rows': rows})
