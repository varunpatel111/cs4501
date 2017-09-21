from .models import CustomUser
from .models import Listing
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.shortcuts import render


def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__

def index(request):
	return render(request, 'index.html', {})

#Users

#Get all CustomUsers
@csrf_exempt
def all_users(request):
	if request.method != "GET":
		d = dict()
		d["status"] = "FAILED"
		return JsonResponse(d)

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
		return HttpResponse("No users!", status=404)

#Check if object is a valid CustomUser
@csrf_exempt
def isValidUser(request):
	if (request.POST.get('email') and request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('password')):
		return True
	else:
		return False

#Create a new CustomUser
@csrf_exempt
def users_create(request):

	if request.method != "POST":
		return HttpResponse("Must be a POST request", status=400)

	if request.method == "POST":
		if (isValidUser(request)):
			email = request.POST.get('email')
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			password = request.POST.get('password')

			newUser = CustomUser(email=email, first_name=first_name, password=password, last_name=last_name)
			newUser.save()
			return HttpResponse("User created succesfully")
		else:
			return HttpResponse("The user you are trying to create is invalid", status=404)


@csrf_exempt
def get_user(request, user):
	if request.method == 'GET':
		user_num = int(user)
		if (len(CustomUser.objects.filter(id=user_num)) != 0):
			user = CustomUser.objects.filter(id=user_num)[0]
			return HttpResponse(json.dumps(user, default=lambda o: o.__dict__, sort_keys=True, indent=4))
		else:
			return HttpResponse("Sorry, that user doesn't exist", status=404)

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
				return HttpResponse("User updated successfully")
			else:
				return HttpResponse("Sorry, that user does not exist", status=404)
		else:
			return HttpResponse("The user you are trying to create is not valid", status=400)

	elif request.method == "DELETE":
		user_num = int(user)
		if (len(CustomUser.objects.filter(id=user_num)) == 0):
			return HttpResponse("Sorry, that user does not exist", status=404)

		u = CustomUser.objects.filter(id=user_num)[0]
		u.delete()
		return HttpResponse("User with id " + str(user_num) + " deleted successfully")

	else:
		return HttpResponse("Must be a GET/POST/DELETE request", status=400)


#Get all Listings
def all_listings(request):
	d = {}
	if request.method != "GET":
		d["status"] = "FAILED"
		d["message"] = "MUST BE A GET REQUEST"
		return JsonResponse(d, status=404)

	queryset = Listing.objects.all().values()
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
@csrf_exempt
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
			return JsonResponse(d,  status=404)

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
@csrf_exempt
def isValidListing (request):
	if (request.POST.get('address') and request.POST.get('num_bedrooms') and request.POST.get('num_bathrooms') and request.POST.get('price') and request.POST.get('start_date') and request.POST.get('end_date') and request.POST.get('description') and request.POST.get('sold') and request.POST.get('user') ):
		user_num = int(request.POST.get('user'))
		if (len(CustomUser.objects.filter(id=user_num)) != 0):
			return True
	else:
		return False

#Create new Listing
@csrf_exempt
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
			d["status"] = "SUCCESS"
			d["message"] = "LISTING CREATED SUCCESSFULLY"
			return JsonResponse(d)
		else:
			d["status"] = "FAILURE"
			d["message"] = "LISTING SENT IS INVALID"
			return JsonResponse(d)
