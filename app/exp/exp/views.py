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


def homePage(request):
	print ("About to perform the GET request...")
	req = urllib.request.Request('http://models-api:8000/api/listings')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp)

def get_listing(request, listing):
	s = "http://models-api:8000/api/listings/" + listing + "/"
	req = urllib.request.Request(s)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp)

def get_user(request, user):
	s = "http://models-api:8000/api/users/" + user + "/"
	req = urllib.request.Request(s)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp)

def newListingForm(request):
	s = "http://models-api:8000/api/listings/createForm/"
	req = urllib.request.Request(s)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp)

def createListing(request):
	url = "http://models-api:8000/api/listings/create/"
	result = urllib.request.urlopen(url, urllib.parse.urlencode(request.POST).encode('utf-8'))
	content = result.read()
	return HttpResponse(content)

def loginForm(request):
	s = "http://models-api:8000/api/authenticate/login/"
	req = urllib.request.Request(s)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp)

def userLogin(request):
	url = "http://models-api:8000/api/authenticate/loginUser"
	result = urllib.request.urlopen(url, urllib.parse.urlencode(request.POST).encode('utf-8'))
	content = result.read()
	return HttpResponse(content)

