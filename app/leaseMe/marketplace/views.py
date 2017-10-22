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
from django.template.loader import render_to_string

def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__


#Users

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


#Check if object is a valid CustomUser
def isValidUser(request):
	if (request.POST.get('email') and request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('password') and request.POST.get('username')):
		return True
	else:
		return False


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


#Get all Listings
def all_listings(request):
	d = {}
	if request.method != "GET":
		d["status"] = "FAILED"
		d["message"] = "MUST BE A GET REQUEST"
		return JsonResponse(d, status=404)

	queryset = Listing.objects.all().values().order_by('start_date')

	arr = []
	for obj in queryset:
		arr.append(obj)
	if(len(queryset) > 0):
		d["status"] = "SUCCESS"
		d["data"] = arr
		return JsonResponse(d)
	else:
		d["status"] = "FAILED"
		d["message"] = "NO LISTINGS AVAILABLE"
		return JsonResponse(d, status=404)

#Get a single Listing (0, 1, 2...)
def get_listing(request, listing):
	d = {}
	if request.method == "GET":
		listing_num = int(listing)
		if (len(Listing.objects.filter(id=listing_num)) != 0):
			listing1 = Listing.objects.filter(id=listing_num).values()
			arr = []
			arr.append(listing1[0])
			d["status"] = "SUCCESS"
			d["data"] = arr
			return JsonResponse(d)
		else:
			d["status"] = "FAILED"
			d["message"] = "THAT LISTING DOESN'T EXIST"
			return JsonResponse(d)

	elif request.method == "POST":
		if (isValidListing(request)):
			listing_num = int(listing)
			if (len(Listing.objects.filter(id=listing_num)) != 0):
				listing1 = Listing.objects.filter(id=listing_num)[0]
				listing1.address = request.POST.get('address')
				listing1.num_bedrooms = request.POST.get('num_bedrooms')
				listing1.num_bathrooms = request.POST.get('num_bathrooms')
				listing1.price = request.POST.get('price')
				listing1.start_date = request.POST.get('start_date')
				listing1.end_date = request.POST.get('end_date')
				listing1.description = request.POST.get('description')
				listing1.sold = request.POST.get('sold')
				user = request.POST.get('user')
				user_num = int(user)
				user = CustomUser.objects.filter(id=user_num)[0]
				listing1.user = user
				listing1.save()
				d["status"] = "SUCCESS"
				d["message"] = "LISTING UPDATED SUCCESSFULLY"
				return JsonResponse(d)
		else:
			d["status"] = "FAILED"
			d["message"] = "THAT LISTING DOESN'T EXIST"
			return JsonResponse(d,  status=404)

	elif request.method == "DELETE":
		list_num = int(listing)
		if (len(Listing.objects.filter(id=list_num)) == 0):
			d["status"] = "FAILED"
			d["message"] = "THAT LISTING DOESN'T EXIST"
			return JsonResponse(d,  status=404)
		l = Listing.objects.filter(id=list_num)[0]
		l.delete()
		d["status"] = "SUCCESS"
		d["message"] = "LISTING DELETED SUCCESSFULLY"
		return JsonResponse(d)

	else:
		d["status"] = "FAILURE"
		d["message"] = "THE HTTP REQUEST MUST BE GET/POST/DELETE"
		return JsonResponse(d)


#Check if object is a valid Listing
def isValidListing (request):
	if (request.POST.get('address') and request.POST.get('num_bedrooms') and request.POST.get('num_bathrooms') and request.POST.get('price') and request.POST.get('start_date') and request.POST.get('end_date') and request.POST.get('description') and request.POST.get('sold') and request.POST.get('user') ):
		user_num = int(request.POST.get('user'))
		if (len(CustomUser.objects.filter(id=user_num)) != 0):
			return True
	else:
		return False

#Create new Listing
def listings_create(request):
	d = {}
	if request.method != "POST":
		d["status"] = "FAILURE"
		d["message"] = "THE HTTP REQUEST MUST BE POST"
		return JsonResponse(d)

	if request.method == "POST":
		if (isValidListing(request)):
			address = request.POST.get('address')
			num_bedrooms = request.POST.get('num_bedrooms')
			num_bathrooms = request.POST.get('num_bathrooms')
			price = request.POST.get('price')
			start_date = request.POST.get('start_date')
			end_date = request.POST.get('end_date')
			description = request.POST.get('description')
			sold = request.POST.get('sold')
			user = request.POST.get('user')
			user_num = int(user)
			user = CustomUser.objects.filter(id=user_num)[0]

			newListing = Listing(address=address, num_bedrooms=num_bedrooms, num_bathrooms=num_bathrooms, price=price, start_date=start_date, end_date=end_date, description=description, sold=sold, user=user)
			newListing.save()
			d["id"] = newListing.id
			d["status"] = "SUCCESS"
			d["message"] = "LISTING CREATED SUCCESSFULLY"
			return JsonResponse(d)
		else:
			d["status"] = "FAILURE"
			d["message"] = "LISTING SENT IS INVALID"
			return JsonResponse(d)

def new_listing_form(request):
	d = {}
	form = ListingForm()
	#html = render(request, 'form.html', {'form': form})
	html = render_to_string('form.html', { 'form': form })
	d["html"] = html
	return JsonResponse(d)

def loginUser(request):
	d = {}
	form = LoginForm()
	html = render_to_string('login.html', { 'form': form })
	d["html"] = html
	return JsonResponse(d)
