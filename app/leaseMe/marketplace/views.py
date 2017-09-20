from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .models import Listing
from .serializers import CustomUserSerializer
from .serializers import ListingSerializer
from django.shortcuts import render

class CustomUserList(APIView):

	def get(self, request):
		users = CustomUser.objects.all()
		serializer = CustomUserSerializer(users, many=True)
		return Response(serializer.data)

	def post(self):
		pass

class ListingList(APIView):

	def get(self, request):
		listings = Listing.objects.all()
		serializer = ListingSerializer(listings, many=True)
		return Response(serializer.data)

	def post(self):
		pass

