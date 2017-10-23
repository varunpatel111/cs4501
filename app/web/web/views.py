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

def apiInfo(request):
	return render(request, 'index.html')

def homePage(request):
	req = urllib.request.Request('http://exp-api:8000/api/homePage')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)

	data = resp["data"]
	return render(request, 'homepage.html', {'data': data})

def get_listing(request, listing):
	s = "http://exp-api:8000/api/listingPage/" + listing + "/"
	req = urllib.request.Request(s)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp_user = json.loads(resp_json)
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
		return render(request, 'listing.html',  {'data': all_data})
	else:
		return render(request, 'Error.html')

def get_user(request, user):
	req = urllib.request.Request("http://exp-api:8000/api/userPage/" + str(user) + "/")
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	if(resp["status"] == "SUCCESS"):
		data = resp["data"]
		return render(request, 'users.html', {'data': data})
	else:
		return render(request, 'Error.html')

def create_listing_form(request):
	if request.method == "GET":
		if user_logged_in(request):
			req = urllib.request.Request("http://exp-api:8000/api/newListing/")
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
			resp = json.loads(resp_json)
			return HttpResponse(resp["html"])
		else:
			return HttpResponseRedirect('/login/')
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
		content = result.read()
		response = HttpResponseRedirect("/")
		return response

def user_logged_in(request):
	authenticator = request.COOKIES.get('authenticator')
	if not authenticator:
		return False
	else:
		return True


def create_user_form(request):
	if request.method == "GET":
		req = urllib.request.Request("http://exp-api:8000/api/newUser/")
		resp_json = urllib.request.urlopen(req).read().decode('utf-8')
		resp = json.loads(resp_json)
		return HttpResponse(resp["html"])
	else:
		url = "http://exp-api:8000/api/createUser/"
		result = urllib.request.urlopen(url, urllib.parse.urlencode(request.POST).encode("utf-8"))
		content = result.read()
		return HttpResponse(content)

def login_form(request):
	if user_logged_in(request):
		return HttpResponseRedirect('/')
	else:
		if request.method == "GET":
			req = urllib.request.Request("http://exp-api:8000/api/loginForm/")
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
			resp = json.loads(resp_json)
			return HttpResponse(resp["html"])
		else:
			f = request.POST
			username = f['username']
			password = f['password']

			url = "http://exp-api:8000/api/userLogin/"

			result = urllib.request.urlopen(url, urllib.parse.urlencode({"username" : username, "password" : password}).encode("utf-8"))
			resp = result.read().decode('utf-8')
			resp = json.loads(resp)
			if(resp["status"] == "FAILED"):
				return HttpResponseRedirect('/login/')
			else:
				authenticator = resp["authenticator"]
				response = HttpResponseRedirect("/")
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
		return response
	else:
		response = HttpResponseRedirect("/")
		return response


# def login(request):
#     # If we received a GET request instead of a POST request
#     if request.method == 'GET':
#         # display the login form page
#         next = request.GET.get('next') or reverse('home')
#         return render('login.html', ...)
#
#     # Creates a new instance of our login_form and gives it our POST data
#     f = login_form(request.POST)
#
#     # Check if the form instance is invalid
#     if not f.is_valid():
#       # Form was bad -- send them back to login page and show them an error
#       return render('login.html', ...)
#
#     # Sanitize username and password fields
#     username = f.cleaned_data['username']
#     password = f.cleaned_data['password']
#
#     # Get next page
#     next = f.cleaned_data.get('next') or reverse('home')
#
#     # Send validated information to our experience layer
#     resp = login_exp_api(username, password)
#
#     # Check if the experience layer said they gave us incorrect information
#     if not resp or not resp['ok']:
#       # Couldn't log them in, send them back to login page with error
#       return render('login.html', ...)
#
#     """ If we made it here, we can log them in. """
#     # Set their login cookie and redirect to back to wherever they came from
#     authenticator = resp['resp']['authenticator']
#
#     response = HttpResponseRedirect(next)
#     response.set_cookie("auth", authenticator)
#
#     return response
