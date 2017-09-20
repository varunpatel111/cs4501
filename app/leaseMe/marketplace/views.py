from .models import CustomUser
from .models import Listing
from django.http import Http404
from django.http import HttpResponse
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
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

def get_user(request, user):
	queryset = CustomUser.objects.all()
	r = list(queryset)
	user = int(user)
	if r[user]:
		return HttpResponse(json.dumps(r[user], default=lambda o: o.__dict__,
            sort_keys=True, indent=4))
	else:
		return None


@csrf_exempt
def users_create(request):
	if request.method == "POST":
		return HttpResponse("got it")
	else:
		return HttpResponse("got it")



def all_listings(request):
	queryset = Listing.objects.all()
	r = serializers.serialize('json', queryset)
	return HttpResponse(r)

def get_listing(request, listing):
	queryset = Listing.objects.all()
	r = list(queryset)
	listing = int(listing)
	if r[listing]:
		return HttpResponse(json.dumps(r[listing], default=lambda o: o.__dict__,
            sort_keys=True, indent=4))
	else:
		return None
