from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.shortcuts import render
import urllib
import urllib.request
import urllib.parse
import math
from urllib.request import urlopen
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse

def apiInfo(request):
	return render(request, 'index.html')

def homePage(request):
	req = urllib.request.Request('http://exp-api:8000/api/homePage')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	logged_in = user_logged_in(request)
	data = resp["data"]
	response = render(request, 'homepage.html', {'data': data, 'logged_in': logged_in})
	if request.COOKIES.get('next') != None:
		response.delete_cookie("next")
	return response


def get_listing(request, listing):
	url = "http://exp-api:8000/api/listingPage/"
	if user_logged_in(request):
		result = urllib.request.urlopen(url, urllib.parse.urlencode({"authenticator" : request.COOKIES.get('authenticator'), "listing" : listing}).encode("utf-8"))
	else:
		result = urllib.request.urlopen(url, urllib.parse.urlencode({"listing" : listing}).encode("utf-8"))

	resp = result.read().decode('utf-8')
	resp_user = json.loads(resp)

	if(resp_user["status"] == "SUCCESS"):
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
		logged_in = user_logged_in(request)

		return render(request, 'listing.html',  {'data': all_data, 'logged_in' : logged_in})
	else:
		return render(request, 'Error.html')

def get_user(request, user):
	req = urllib.request.Request("http://exp-api:8000/api/userPage/" + str(user) + "/")
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	if(resp["status"] == "SUCCESS"):
		data = resp["data"]
		logged_in = user_logged_in(request)
		return render(request, 'users.html', {'data': data, 'logged_in' : logged_in})
	else:
		return render(request, 'Error.html')

def create_listing_form(request):
	if request.method == "GET":
		if user_logged_in(request):
			req = urllib.request.Request("http://exp-api:8000/api/newListing/")
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
			resp = json.loads(resp_json)
			html = resp["html"]
			return render(request, 'listing_form.html', {'html': html})
		else:
			response = HttpResponseRedirect("/login")
			response.set_cookie("next", "/listings/new/")
			return response
	else:
		url = "http://exp-api:8000/api/getUserId/"
		result = urllib.request.urlopen(url, urllib.parse.urlencode({"authenticator" : request.COOKIES.get('authenticator')}).encode("utf-8"))
		resp = result.read().decode('utf-8')
		resp = json.loads(resp)
		user = resp["user_id"]
		d = request.POST.copy()
		d["user"] = user
		url = "http://exp-api:8000/api/createListing/"
		result = urllib.request.urlopen(url, urllib.parse.urlencode(d).encode("utf-8"))
		resp = result.read().decode('utf-8')
		resp = json.loads(resp)
		if resp["status"] == "SUCCESS":
			messages.success(request, 'Listing created succesfully.')
			return HttpResponseRedirect("/")
		else:
			messages.warning(request, 'Listing sent was invalid.')
			return HttpResponseRedirect("/listings/new/")

def user_logged_in(request):
	authenticator = request.COOKIES.get('authenticator')
	if not authenticator:
		return False
	else:
		return True


def create_user_form(request):
	if user_logged_in(request):
		messages.warning(request, 'You are logged into an account.')
		return HttpResponseRedirect("/")
	else:
		if request.method == "GET":
			req = urllib.request.Request("http://exp-api:8000/api/newUser/")
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
			resp = json.loads(resp_json)
			html = resp["html"]
			return render(request, 'user_form.html', {'html': html})
		else:
			url = "http://exp-api:8000/api/createUser/"
			result = urllib.request.urlopen(url, urllib.parse.urlencode(request.POST).encode("utf-8"))
			resp = result.read().decode('utf-8')
			resp = json.loads(resp)
			if resp["status"] == "FAILED":
				if resp["message"] == "This username already exists":
					messages.warning(request, 'An account with this username already exists.')
					return HttpResponseRedirect("/users/new")
				elif resp["message"] == "An account with this email already exists":
					messages.warning(request, 'An account with this email already exists.')
					return HttpResponseRedirect("/users/new")
				else:
					messages.warning(request, 'User sent is invalid')
					return HttpResponseRedirect("/users/new")
			else:
				messages.success(request, 'User created successfully')
				return HttpResponseRedirect('/login')


def login_form(request):
	if user_logged_in(request):
		messages.warning(request, 'You are already logged in')
		return HttpResponseRedirect('/')
	else:
		if request.method == "GET":
			req = urllib.request.Request("http://exp-api:8000/api/loginForm/")
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
			resp = json.loads(resp_json)
			html = resp["html"]

			#return HttpResponse(resp["html"])
			return render(request, 'login.html', {'html': html})
		else:
			f = request.POST
			username = f['username']
			password = f['password']

			url = "http://exp-api:8000/api/userLogin/"

			result = urllib.request.urlopen(url, urllib.parse.urlencode({"username" : username, "password" : password}).encode("utf-8"))
			resp = result.read().decode('utf-8')
			resp = json.loads(resp)
			if(resp["status"] == "FAILED"):
				messages.warning(request, 'Invalid login credentials')
				return HttpResponseRedirect('/login/')
			else:
				authenticator = resp["authenticator"]
				messages.success(request, 'Logged in successfully!')
				if request.COOKIES.get('next') != None:
					response = HttpResponseRedirect(request.COOKIES.get('next'))
					response.delete_cookie("next")
				else:
					response = HttpResponseRedirect('/')
				response.set_cookie("authenticator", authenticator)
				return response

def logout(request):
	if user_logged_in(request):
		response = HttpResponseRedirect("/")
		response.delete_cookie("authenticator")
		url = "http://exp-api:8000/api/getUserId/"
		result = urllib.request.urlopen(url, urllib.parse.urlencode({"authenticator" : request.COOKIES.get('authenticator')}).encode("utf-8"))
		resp = result.read().decode('utf-8')
		resp = json.loads(resp)
		user = resp["user_id"]
		d = request.POST.copy()
		url = "http://exp-api:8000/api/logoutUser/"
		result = urllib.request.urlopen(url, urllib.parse.urlencode({"authenticator" : request.COOKIES.get('authenticator')}).encode("utf-8"))
		resp = result.read().decode('utf-8')
		d["user"] = user
		messages.success(request, 'Logged out successfully!')
		return response
	else:
		response = HttpResponseRedirect("/")
		return response

def search(request):
	url = "http://exp-api:8000/api/search/"
	result = urllib.request.urlopen(url, urllib.parse.urlencode(request.POST).encode("utf-8"))
	resp = result.read().decode('utf-8')
	resp = json.loads(resp)
	count = resp["hits"]["total"]
	logged_in = user_logged_in(request)
	data = []
	if count is 0:
		return render(request, 'searchResults.html', {'data': data, 'logged_in': logged_in, 'count': False})
	resp = resp["hits"]["hits"]
	for d in resp:
		data.append(d["_source"])
	response = render(request, 'searchResults.html', {'data': data, 'logged_in': logged_in, 'count': True})
	return response
