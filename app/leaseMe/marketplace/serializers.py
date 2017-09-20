from rest_framework import serializers
from .models import CustomUser
from .models import Listing

class CustomUserSerializer(serializers.ModelSerializer):

	class Meta:
		model = CustomUser
		fields = '__all__'

class ListingSerializer(serializers.ModelSerializer):

	class Meta:
		model = Listing
		fields = '__all__'

