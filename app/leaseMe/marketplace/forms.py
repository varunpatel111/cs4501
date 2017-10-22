from django import forms

from .models import Listing
from .models import User

class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('address', 'num_bedrooms', 'num_bathrooms', 'price', 'start_date', 'end_date', 'description', 'sold', 'user')

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')
