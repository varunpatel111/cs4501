from rest_framework import serializers
from .models import User
from .models import Listing

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = '__all__'

class ListingSerializer(serializers.ModelSerializer):

	class Meta:
		model = Listing
		fields = '__all__'

