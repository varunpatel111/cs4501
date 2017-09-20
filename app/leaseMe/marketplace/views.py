from .models import CustomUser
from .models import Listing
from django.http import Http404
from django.http import HttpResponse
import json
from django.core import serializers

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
