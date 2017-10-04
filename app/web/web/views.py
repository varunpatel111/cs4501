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

def get_listing(request, listing):
	s = "http://exp-api:8000/api/listingPage/" + listing + "/"
	req = urllib.request.Request(s)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp_user = json.loads(resp_json)

	data = resp_user["data"]
	l = data[0]
	user_id = l['user_id']

	p = "http://exp-api:8000/api/userPage/" + str(user_id) + "/"
	req2 = urllib.request.Request(p)
	resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
	resp_listing = json.loads(resp_json2)

	data1 = resp_listing["data"]
	u = data1[0]

	all_data = {}
	all_data['listing'] = l
	all_data['user'] = u

	return render(request, 'listing.html',  {'data': all_data})

