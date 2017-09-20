from .models import CustomUser
from .models import Listing
from django.http import Http404
from django.http import HttpResponse
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def isValidUser(request):
	if (request.POST.get('email') and request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('password')):
		return True
	else:
		return False

#class CustomUserViewSet(viewsets.ModelViewSet):
#    queryset = CustomUser.objects.all()
#    serializer_class = CustomUserSerializer

#class ListingViewSet(viewsets.ModelViewSet):
#    queryset = Listing.objects.all()
#    serializer_class = ListingSerializer

def all_users(request):
	queryset = CustomUser.objects.all()
	r = serializers.serialize('json', queryset)
	return HttpResponse(r)

@csrf_exempt
def users_create(request):
	if request.method == "POST":
		if (isValidUser(request)):
			email = request.POST.get('email')
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			password = request.POST.get('password')

			newUser = CustomUser(email=email, first_name=first_name, password=password, last_name=last_name)
			# newUser.save()
			return HttpResponse("User saved")
		else:
			return HttpResponse("Sorry, the object passed was not valid")

		return HttpResponse(email)


	return HttpResponse("Working")
