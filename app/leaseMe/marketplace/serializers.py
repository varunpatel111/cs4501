from rest_framework import serializers
from .models import CustomUser
from .models import Listing
import json

class CustomUserSerializer():
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

class ListingSerializer(serializers.ModelSerializer):

	class Meta:
		model = Listing
		fields = '__all__'
