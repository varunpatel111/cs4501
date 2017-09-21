from .models import CustomUser
from .models import Listing
from django.http import Http404
from django.http import HttpResponse
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import datetime


def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__

#Users

#Get all CustomUsers
def all_users(request):
	queryset = CustomUser.objects.all()
	r = serializers.serialize('json', queryset)
	if(len(queryset) > 0):
		return HttpResponse(r)
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
	if request.method == "POST":
		if (isValidUser(request)):
			email = request.POST.get('email')
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			password = request.POST.get('password')

			newUser = CustomUser(email=email, first_name=first_name, password=password, last_name=last_name)
			newUser.save()
			return HttpResponse("SUCCESS")
		else:
			return HttpResponse("FAILED")

	return HttpResponse("This should be a POST method!")

@csrf_exempt
def get_user(request, user):
	if request.method == 'GET':
		user_num = int(user)
		if (len(CustomUser.objects.filter(id=user_num)) != 0):
			user = CustomUser.objects.filter(id=user_num)[0]
			return HttpResponse(json.dumps(user, default=lambda o: o.__dict__,
	            sort_keys=True, indent=4))
		else:
			return HttpResponse("Sorry, that user doesn't exist", status=404)

	if request.method == "POST":
		if (isValidUser(request)):
			user_num = int(user)
			if (len(CustomUser.objects.filter(id=user_num)) != 0):
				user = CustomUser.objects.filter(id=user_num)[0]
				user.first_name = request.POST.get('first_name')
				user.last_name = request.POST.get('last_name')
				user.password = request.POST.get('password')
				user.email = request.POST.get('email')
				user.save()
				return HttpResponse("SUCCESS")
			else:
				return HttpResponse("FAILED", status=404)
		else:
			return HttpResponse("FAILED")










# listings ------







#Get all Listings
def all_listings(request):
	queryset = Listing.objects.all()
	r = serializers.serialize('json', queryset)
	if(len(queryset) > 0):
		return HttpResponse(r)
	else:
		return HttpResponse("No listings!", status=404)

#Get a single Listing (0, 1, 2...)
@csrf_exempt
def get_listing(request, listing):
	if request.method == "GET":
		listing_num = int(listing)
		if (len(Listing.objects.filter(id=listing_num)) != 0):
			listing1 = Listing.objects.filter(id=listing_num)[0]
			return HttpResponse(json.dumps(listing1, default=json_default,
				sort_keys=True, indent=4))
		else:
			return HttpResponse("Sorry, that listing doesn't exist",  status=404)

	if request.method == "POST":
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
				return HttpResponse("SUCCESS")
		else:
			return HttpResponse("FAILED")



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
			return HttpResponse("SUCCESS")
		else:
			return HttpResponse("FAILED")

	return HttpResponse("This should be a POST method!")
