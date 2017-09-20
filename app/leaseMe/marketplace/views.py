from .models import CustomUser
from .models import Listing
from django.http import Http404
from django.http import HttpResponse
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

#Users

#Get all CustomUsers
def all_users(request):
	queryset = CustomUser.objects.all()
	r = serializers.serialize('json', queryset)
	return HttpResponse(r)

#Get a single CustomUser (0, 1, 2...)
def get_user(request, user):
	queryset = CustomUser.objects.all()
	r = list(queryset)
	user = int(user) - 1
	if r[user]:
		return HttpResponse(json.dumps(r[user], default=lambda o: o.__dict__,
            sort_keys=True, indent=4))
	else:
		return None

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
			return HttpResponse("User saved")
		else:
			return HttpResponse("Sorry, the object passed was not valid")

	return HttpResponse("This is a POST method!")



# listings


#Get all Listings
def all_listings(request):
	queryset = Listing.objects.all()
	r = serializers.serialize('json', queryset)
	return HttpResponse(r)

#Get a single Listing (0, 1, 2...)
def get_listing(request, listing):
	queryset = Listing.objects.all()
	r = list(queryset)
	listing = int(listing)
	if r[listing]:
		return HttpResponse(json.dumps(r[listing], default=lambda o: o.__dict__,
            sort_keys=True, indent=4))
	else:
		return None

#Check if object is a valid Listing
@csrf_exempt
def isValidListing (request):
	if (request.POST.get('address') and request.POST.get('num_bedrooms') and request.POST.get('num_bathrooms') and request.POST.get('price') and request.POST.get('start_date') and request.POST.get('end_date') and request.POST.get('description') and request.POST.get('sold')  and request.POST.get('user') ):
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

			newListing = Listing(address=address, num_bedrooms=num_bedrooms, num_bathrooms=num_bathrooms, price=price, start_date=start_date, end_date=end_date, description=description, sold=sold, user=user)
			newListing.save()
			return HttpResponse("Listing saved")
		else:
			return HttpResponse("Sorry, the object passed was not valid")

	return HttpResponse("This is a POST method!")
