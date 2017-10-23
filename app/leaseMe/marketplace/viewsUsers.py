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
from .forms import LoginForm
from .forms import UserForm
from django.template.loader import render_to_string


def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__



#Get all CustomUsers
def all_users(request):
	if request.method != "GET":
		d = dict()
		d["status"] = "FAILED"
		d["message"] = "Request should be a GET request."
		return JsonResponse(d, status=400)

	queryset = CustomUser.objects.all().values()
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
		d["message"] = "No users currently."
		return JsonResponse(d, status=400)

#Check if object is a valid CustomUser
def isValidUser(request):
	if (request.POST.get('email') and request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('password') and request.POST.get('username')):
		return True
	else:
		return False


#Create a new CustomUser
def users_create(request):
    d = dict()
    if request.method != "POST":
        d["status"] = "FAILED"
        d["message"] = "This should be a POST request."
        return JsonResponse(d, status=400)
    if request.method == "POST":
        if (isValidUser(request)):
            if (len(CustomUser.objects.filter(username=request.POST.get('username'))) == 0):
                email = request.POST.get('email')
                username = request.POST.get('username')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                password = request.POST.get('password')
                newUser = CustomUser(username=username, email=email, first_name=first_name, password=password, last_name=last_name)
                newUser.save()
                d["id"] = newUser.id
                d["status"] = "SUCCESS"
                d["message"] = "User created succesfully."
                return JsonResponse(d)
            else:
                d["status"] = "FAILED"
                d["message"] = "This username already exists"
                return JsonResponse(d, status=400)
        else:
            d["status"] = "FAILED"
            d["message"] = "This should be a POST request."
            return JsonResponse(d, status=400)


def get_user(request, user):
	d = dict()

	if request.method == 'GET':
		user_num = int(user)
		if (len(CustomUser.objects.filter(id=user_num)) != 0):
			userset = CustomUser.objects.filter(id=user_num).values()
			arr = []
			arr.append(userset[0])
			d["status"] = "SUCCESS"
			d["data"] = arr
			return JsonResponse(d)
		else:
			d["status"] = "FAILED"
			d["message"] = "Sorry, that user doesn't exist"
			return JsonResponse(d)


	elif request.method == "POST":
		if (isValidUser(request)):
			user_num = int(user)
			if (len(CustomUser.objects.filter(id=user_num)) != 0):
				user = CustomUser.objects.filter(id=user_num)[0]
				user.first_name = request.POST.get('first_name')
				user.last_name = request.POST.get('last_name')
				user.password = request.POST.get('password')
				user.email = request.POST.get('email')
				user.save()
				d["status"] = "SUCCESS"
				d["message"] = "User updated successfully"
				return JsonResponse(d)
			else:
				d["status"] = "FAILED"
				d["message"] = "Sorry, that user does not exist."
				return JsonResponse(d, status=400)
		else:
			d["status"] = "FAILED"
			d["message"] = "Sorry, that user is not valid."
			return JsonResponse(d, status=400)

	elif request.method == "DELETE":
		user_num = int(user)
		if (len(CustomUser.objects.filter(id=user_num)) == 0):
			d["status"] = "FAILED"
			d["message"] = "Sorry, that user does not exist."
			return JsonResponse(d, status=400)

		u = CustomUser.objects.filter(id=user_num)[0]
		u.delete()
		d["status"] = "SUCCESS"
		d["message"] = "User deleted successfully."
		return JsonResponse(d, status=400)

	else:
		d["status"] = "SUCCESS"
		d["message"] = "Request must be a GET/POST/DELETE request."
		return JsonResponse(d, status=400)

def loginUser(request):
	if (request.method == "GET"):
		d = {}
		form = LoginForm()
		html = render_to_string('login.html', { 'form': form })
		d["html"] = html
		return JsonResponse(d)

def login(request):
	#this is arun/varun's function here
	d = {}
	d["message"] = "hello world"
	#return HttpResponse("hello")
	return JsonResponse(d)
	#d = {}
	##username = request.POST.get("username")
	#password = request.POST.get("password")
	#d['username'] = username;
	#d['password'] = password
	#return JsonResponse(d)

def new_user_form(request):
	d = {}
	form = UserForm()
	html = render_to_string('new_user_form.html', { 'form': form })
	d["html"] = html
	return JsonResponse(d)

def logoutUser(request):
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
