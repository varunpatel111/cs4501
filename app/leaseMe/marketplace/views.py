from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import CustomUser
from .models import Listing
from .serializers import CustomUserSerializer
from .serializers import ListingSerializer
from django.shortcuts import render
from django.http import Http404

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class CustomUserList(APIView):

	def get(self, request):
		users = CustomUser.objects.all()
		serializer = CustomUserSerializer(users, many=True)
		return Response(serializer.data)

	#def post(self, request):
	#		serializer = StockSerializer(data=request.data)
	#	if serializer.is_valid():
	#		serializer.save()
	#		return Response(serializer.data, status=status.HTTP_201_CREATED)
	#	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserDetail(APIView):

	def get_object(self, pk):
		try:
			return CustomUser.objects.get(pk=pk)
		except CustomUser.DoesNotExist:
			raise Http404("User does not exist")

	def get(self, request, pk):
		snippet = self.get_object(pk)
		serializer = CustomUserSerializer(snippet)
		return Response(serializer.data)

	def put(self, request, pk):
		snippet = self.get_object(pk)
		serializer = CustomUserSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class ListingList(APIView):

	def get(self, request):
		listings = Listing.objects.all()
		serializer = ListingSerializer(listings, many=True)
		return Response(serializer.data)

	def post(self):
		pass

